# youtube_finder.py - Version améliorée
from playwright.async_api import async_playwright # type: ignore
from bs4 import BeautifulSoup
import re
import yt_dlp # type: ignore

async def find_opening_on_youtube(search_query):
    """
    Cherche une requête sur YouTube et renvoie le meilleur résultat
    basé sur des filtres stricts (durée, mots-clés).
    """
    # ... (la partie playwright de connexion ne change pas)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0...")
        page = await context.new_page()
        
        url = f'https://www.youtube.com/results?search_query={search_query.replace(" ", "+")}'
        
        try:
            await page.goto(url, wait_until="networkidle")
            try:
                await page.locator("button[aria-label*='Accept']").click(timeout=3000)
            except Exception:
                pass
            await page.wait_for_selector('ytd-video-renderer', timeout=10000)
            page_content = await page.content()
        except Exception as e:
            print(f"   Erreur Playwright : {e}")
            await browser.close()
            return None, None
        finally:
            await browser.close()

    soup = BeautifulSoup(page_content, 'lxml')

    for video in soup.find_all('ytd-video-renderer'):
        title_tag = video.find('a', id='video-title')
        duration_tag = video.find('span', class_='style-scope ytd-thumbnail-overlay-time-status-renderer')

        if not title_tag or not duration_tag or not ':' in duration_tag.text:
            continue
            
        title = title_tag.get('title', '')
        duration_text = duration_tag.text.strip()
        
        # Filtre sur les mots-clés indésirables (inchangé)
        if re.search(r'Cover|Piano|Lofi|Nightcore|Instrumental|Lyrics|Full|Extended|8-bit|Remix|AMV', title, re.IGNORECASE):
            continue
            
        parts = list(map(int, duration_text.split(':')))
        seconds = sum(p * 60**i for i, p in enumerate(reversed(parts)))
        # Filtre de durée : entre 1m20s (80s) et 2m30s (150s)
        if not (80 <= seconds <= 110):
            continue
        # -------------------------------------------
        
        link = "https://www.youtube.com" + title_tag['href']
        return link, title

    return None, None