# main.py - Version Générateur de Liens
import os
import asyncio
import random
import sys
import subprocess
import webbrowser
from api_client import get_user_anime_list
from function.mal_scraper import get_opening_themes
from function.youtube_finder import find_opening_on_youtube

PATH = os.path.dirname(os.path.abspath(__file__))
ERROR_LOG_FILE = os.path.join(PATH, "search_error.txt")
RESULTS_FILE = os.path.join(PATH, "playlist_results.html")
I = 1

def log_error(message):
    """Écrit un message dans le fichier de log."""
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def generate_html_file(openings_list, username):
    """Génère un fichier HTML avec la liste des liens des openings trouvés."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Playlist d'Openings pour {username}</title>
        <style>
            body {{ font-family: sans-serif; background-color: #121212; color: #e0e0e0; line-height: 1.6; padding: 20px; }}
            h1, h2 {{ color: #ffffff; border-bottom: 2px solid #333; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ background-color: #1e1e1e; margin-bottom: 10px; padding: 15px; border-radius: 5px; border-left: 5px solid #c4302b; }}
            a {{ color: #3ea6ff; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
            .anime-title {{ display: block; font-size: 1.2em; color: #fff; margin-bottom: 5px; }}
            .op-title {{ display: block; font-size: 0.9em; color: #aaa; }}
        </style>
    </head>
    <body>
        <h1>Playlist d'Openings pour {username}</h1>
        <hr>
        <ul>
    """
    
    for op in openings_list:
        html_content += f"""
            <li>
                <p>Animé N°{I}</p>
                <strong class="anime-title">{op['anime_title']} - OP{op['op_number']}</strong>
                <a href="{op['url']}" target="_blank">{op['youtube_title']}</a>
                <span class="op-title">Titre MAL : {op['op_title_from_mal']}</span>
            </li>
        """
        I += 1
        
    html_content += """
        </ul>
    </body>
    </html>
    """
    
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\n✅ Fichier '{os.path.basename(RESULTS_FILE)}' généré avec succès !")

async def main():
    with open(ERROR_LOG_FILE, "w", encoding="utf-8") as f:
        f.write("Log des échecs de recherche :\n" + "="*50 + "\n")

    username = input("Entrez votre pseudo MyAnimeList : ")
    if not username:
        print("Pseudo invalide.")
        return

    print(f"Récupération de la liste pour '{username}' via l'API...")
    anime_list = get_user_anime_list(username, status=2)
    
    if not anime_list:
        print("Impossible de récupérer la liste d'animes. Arrêt.")
        return

    print(f"{len(anime_list)} animes trouvés. Début du traitement...")
    total_animes = len(anime_list)
    
    found_openings = [] # Liste pour stocker tous les résultats

    for anime_index, anime in enumerate(anime_list):
        if anime_index > 0:
            sleep_duration = random.uniform(5, 8)
            print(f"\n[INFO] Pause de {sleep_duration:.1f} secondes...")
            await asyncio.sleep(sleep_duration)

        anime_title = anime["title"]
        print(f"\n--- [{anime_index + 1}/{total_animes}] Traitement de : {anime_title} ---")

        op_count, op_titles = get_opening_themes(anime["anime_id"])
        
        if not op_titles:
            print("Aucun titre d'opening trouvé sur MyAnimeList.")
            continue

        print(f"{len(op_titles)} opening(s) trouvé(s) sur MAL.")

        for i, op_title_from_mal in enumerate(op_titles):
            op_number = i + 1
            print(f"-> Recherche de l'Opening n°{op_number}: '{op_title_from_mal}'...")
            
            query = f"{anime_title} Opening {op_title_from_mal}"
            # L'appel à youtube_finder reste simple et anonyme
            youtube_link, youtube_title = await find_opening_on_youtube(query)

            if youtube_link:
                print(f"   -> Trouvé : {youtube_title}")
                # On ajoute le résultat à notre liste
                found_openings.append({
                    'anime_title': anime_title,
                    'op_number': op_number,
                    'op_title_from_mal': op_title_from_mal,
                    'youtube_title': youtube_title,
                    'url': youtube_link
                })
            else:
                log_error(f"Échec Recherche : {anime_title} - OP{op_number} ({op_title_from_mal})")

    # Une fois toutes les recherches terminées
    if found_openings:
        generate_html_file(found_openings, username)
        webbrowser.open('file://' + os.path.realpath(RESULTS_FILE))

        print("\nLancement du script de téléchargement des openings...")
        try:
            subprocess.run([sys.executable, "youtube_downloader.py"], check=True)
        except FileNotFoundError:
            print("\n[ERREUR] youtube_downloader.py non trouvé. Le téléchargement ne peut pas commencer.")
        except subprocess.CalledProcessError as e:
            print(f"\n[ERREUR] Le script de téléchargement a rencontré une erreur : {e}")

    else:
        print("\nAucun opening n'a pu être trouvé sur YouTube.")

    print("\nTraitement terminé.")
    
if __name__ == "__main__":
    asyncio.run(main())