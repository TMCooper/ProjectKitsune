# mal_scraper.py
import requests, re
from bs4 import BeautifulSoup

def get_opening_themes(anime_id):
    """
    Scrape la page MyAnimeList pour extraire les titres des thèmes d'opening.
    Cette version est conçue pour gérer plusieurs structures HTML (moderne, héritage, etc.).
    
    Renvoie un tuple: (nombre_d_ops, liste_des_titres).
    """
    url = f"https://myanimelist.net/anime/{anime_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        opening_header = soup.find('h2', string=re.compile(r'Opening Theme', re.IGNORECASE))

        if not opening_header:
            # Si même le titre de la section n'existe pas, il n'y a pas d'opening.
            return 0, []

        theme_container = opening_header.find_parent('div').find_next_sibling('div')

        if not theme_container:
            theme_container = opening_header.find_next_sibling('div')
            if not theme_container:
                 return 0, []

        op_titles = []
        
        song_title_spans = theme_container.find_all('span', class_='theme-song-title')
        if song_title_spans:
            for span in song_title_spans:
                title = span.get_text(strip=True).replace('"', '')
                if title:
                    op_titles.append(title)
        
        if not op_titles:
            song_rows = theme_container.find_all('tr')
            for row in song_rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    raw_text = cells[1].get_text(" ", strip=True)
                    
                    title_match = re.search(r'"([^"]+)"', raw_text)
                    if title_match:
                        title = title_match.group(1)
                        op_titles.append(title)

        return len(op_titles), op_titles

    except requests.exceptions.RequestException as e:
        print(f"   -> ERREUR: Impossible de scraper la page MAL pour l'ID {anime_id}: {e}")
        return 0, []
    except Exception as e:
        print(f"   -> ERREUR: Une erreur inattendue est survenue lors du parsing de la page MAL pour l'ID {anime_id}: {e}")
        return 0, []

    except requests.exceptions.RequestException as e:
        print(f"Impossible de scraper la page MAL pour l'ID {anime_id}: {e}")
        return 0, []