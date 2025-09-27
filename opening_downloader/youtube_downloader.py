import platform
from pytubefix import Playlist # type: ignore
from function.Cardinal import *
from function.Yui import *
from function.Holo import *
import os
import re
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_VID = os.path.join(PATH, "Opening")
PATH_PLAY = os.path.join(PATH, "Playlist")
PATH_MP3 = os.path.join(PATH, "Opening Musique")
RESULTS_FILE = os.path.join(PATH, "playlist_results.html")
PROXY = 'http://218.155.31.188:8080'

def extract_youtube_links_from_html(html_file_path):
    """
    Extrait tous les liens YouTube du fichier HTML et les nettoie
    """
    if not os.path.exists(html_file_path):
        print(f"Fichier HTML non trouvé : {html_file_path}")
        return []
    
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        links = []
        
        # Trouve tous les liens YouTube dans le HTML
        for link in soup.find_all('a', href=True):
            url = link['href']
            if 'youtube.com/watch' in url or 'youtu.be/' in url:
                # Nettoie le lien pour ne garder que l'URL de base
                clean_url = clean_youtube_url(url)
                if clean_url:
                    # Récupère aussi le titre pour l'affichage
                    title = link.get_text(strip=True)
                    links.append({'url': clean_url, 'title': title})
        
        return links
    
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier HTML : {e}")
        return []

def clean_youtube_url(url):
    """
    Nettoie l'URL YouTube pour ne garder que le format de base
    """
    try:
        # Pattern pour extraire l'ID de la vidéo
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'v=([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                return f'https://www.youtube.com/watch?v={video_id}'
        
        return None
    except Exception as e:
        print(f"Erreur lors du nettoyage de l'URL : {e}")
        return None

def download_from_html():
    """
    Télécharge tous les openings depuis le fichier HTML généré par main.py
    """
    try:
        if Yui.is_admin():
            Yui.set_proxy(PROXY)
        else:
            Yui.run_as_admin()
            return

        # Extraction des liens depuis le fichier HTML
        print("Extraction des liens depuis playlist_results.html...")
        youtube_links = extract_youtube_links_from_html(RESULTS_FILE)
        
        if not youtube_links:
            print("Aucun lien YouTube trouvé dans le fichier HTML.")
            return

        print(f"{len(youtube_links)} liens trouvés. Début du téléchargement...")
        
        # Demande du format de téléchargement
        print("\nFormat de téléchargement :")
        print("- mp3 : Audio seulement")
        print("- mp4 : Vidéo complète")
        
        mp_v = input("Choisissez le format (mp3/mp4) : ").lower()
        while mp_v not in ["mp3", "mp4"]:
            mp_v = input("Format invalide. Choisissez mp3 ou mp4 : ").lower()

        # Création des dossiers nécessaires
        if mp_v == "mp4":
            if not os.path.exists(PATH_VID):
                os.mkdir(PATH_VID)
            download_path = PATH_VID
        else:
            if not os.path.exists(PATH_MP3):
                os.mkdir(PATH_MP3)
            download_path = PATH_MP3

        # Téléchargement de chaque vidéo
        successful_downloads = 0
        failed_downloads = 0
        
        for i, link_info in enumerate(youtube_links, 1):
            try:
                url = link_info['url']
                title = link_info['title']
                
                print(f"\n[{i}/{len(youtube_links)}] Téléchargement : {title}")
                print(f"URL : {url}")
                
                # Utilisation de la fonction Cardinal existante
                Cardinal.Video_downloader(url, mp_v, "fr", {
                    "fr": {
                        "success_download": "✅ Téléchargement réussi : {title} dans {path}",
                        "download_failed": "❌ Téléchargement échoué"
                    }
                }, PATH_VID, PATH_MP3)
                
                successful_downloads += 1
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Interruption par l'utilisateur (Ctrl+C)")
                print(f"Téléchargements réussis : {successful_downloads}")
                print(f"Téléchargements échoués : {failed_downloads}")
                break
                
            except Exception as e:
                print(f"❌ Erreur lors du téléchargement de '{title}' : {e}")
                failed_downloads += 1
                continue

        # Affichage du résumé
        print("\n" + "="*50)
        print("RÉSUMÉ DU TÉLÉCHARGEMENT")
        print("="*50)
        print(f"✅ Téléchargements réussis : {successful_downloads}")
        print(f"❌ Téléchargements échoués : {failed_downloads}")
        print(f"📁 Dossier de destination : {download_path}")
        
        # Suppression du fichier HTML après téléchargement réussi
        if successful_downloads > 0:
            try:
                if os.path.exists(RESULTS_FILE):
                    os.remove(RESULTS_FILE)
                    print(f"🗑️ Fichier {os.path.basename(RESULTS_FILE)} supprimé.")
            except Exception as e:
                print(f"⚠️ Impossible de supprimer le fichier HTML : {e}")
        
        subprocess.run("cls", shell=True)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interruption par l'utilisateur")
    
    except Exception as e:
        print(f"❌ Erreur générale : {e}")
    
    finally:
        Yui.reset_proxy()

def main():
    """
    Point d'entrée principal - peut être utilisé en mode interactif ou automatique
    """
    try:
        # Vérifie s'il y a un fichier HTML de résultats
        if os.path.exists(RESULTS_FILE):
            print("📄 Fichier de résultats détecté : playlist_results.html")
            response = input("Voulez-vous télécharger automatiquement tous les openings ? (o/n) : ").lower()
            
            if response in ['o', 'oui', 'y', 'yes', '']:
                download_from_html()
                return
        
        # Mode interactif classique si pas de fichier HTML ou si l'utilisateur refuse
        if Yui.is_admin():
            Yui.set_proxy(PROXY)
        else:
            Yui.run_as_admin()
            return

        lang, languages, choix, mp_v = Cardinal.basic()
        
        if choix in ["v"]:
            if not os.path.exists(PATH_VID):
                os.mkdir(PATH_VID)

            Link = input(languages[lang]["Requests_user_link"])
            
            # Nettoyage de l'URL
            clean_link = clean_youtube_url(Link)
            if not clean_link:
                print("URL YouTube invalide.")
                return
                
            Cardinal.Video_downloader(clean_link, mp_v, lang, languages, PATH_VID, PATH_MP3)
            subprocess.run("cls", shell=True)
            
        elif choix in ["p"]:
            if not os.path.exists(PATH_PLAY):
                os.mkdir(PATH_PLAY)

            Link = input(languages[lang]["Requests_user_playlist"])
            yt_play = Playlist(Link)
            Cardinal.Playlist_downloader(yt_play.videos, mp_v, lang, languages, PATH_PLAY, PATH_MP3)
            subprocess.run("cls", shell=True)
        
        elif choix in ["q"]:
            print(languages[lang]["Exit_q"])
            exit()
    
    except KeyboardInterrupt:
        print("\n⚠️ Interruption par l'utilisateur")
    
    except KeyError as e:
        print(f"❌ Erreur de clé : {e}")
    
    finally:
        Yui.reset_proxy()

if __name__ == "__main__":
    main()
    Yui.reset_proxy()
    subprocess.run("cls", shell=True)