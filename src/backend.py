import requests, json, time, re
from rapidfuzz import process, fuzz

class Cardinal:
    def topanime():
        return requests.get("https://api.jikan.moe/v4/top/anime").json()
    
    def getinfo_byid(id):
        anime_id = requests.get(f"https://api.jikan.moe/v4/anime/{id}").json()

        url = anime_id["data"]["url"]
        title = anime_id["data"]["title"]
        title_english = anime_id["data"]["title_english"]
        title_japanese = anime_id["data"]["title_japanese"]
        episodes_number = anime_id["data"]["episodes"]
        status = anime_id["data"]["status"]
        rating = anime_id["data"]["rating"]
        rank = anime_id["data"]["rank"]
        popularity = anime_id["data"]["popularity"]
        favorites = anime_id["data"]["favorites"]
        season = anime_id["data"]["season"]
        synopsis = anime_id["data"]["synopsis"]
        background = anime_id["data"]["background"]
        studios_name = [studio["name"] for studio in anime_id["data"]["studios"]]
        genres_name = [genre["name"] for genre in anime_id["data"]["genres"]]
        image_jpg, image_jpg_small, image_jpg_big = Cardinal.extract_images(anime_id["data"]["images"]["jpg"])

        return url, title, title_english, title_japanese, episodes_number, status, rating, rank, popularity, favorites, season, synopsis, background, studios_name, genres_name, image_jpg, image_jpg_small, image_jpg_big
    
    def extract_images(images):
    
        image_jpg = images.get("image_url")
        image_jpg_small = images.get("small_image_url")
        image_jpg_big = images.get("large_image_url")

        return image_jpg, image_jpg_small, image_jpg_big
    
    def AnimeId():
        with open("AllAnimeId.json", "r", encoding="utf-8") as f:
            AnimeId= json.loads(f.read())
        return AnimeId
    
    def requestsAllid():
        anime_list = []
        seen_ids = set()  # pour éviter les doublons
        i = 1
        errors = 0

        while True:
            try:
                response = requests.get(f"https://api.jikan.moe/v4/anime?page={i}")
                if response.status_code == 200:
                    data = response.json()
                    if not data["data"]:
                        print("Aucune donnée restante, arrêt.")
                        break

                    for anime in data["data"]:
                        if anime["mal_id"] not in seen_ids:  # filtrage
                            anime_info = {"id": anime["mal_id"], "title": anime["title"]}
                            anime_list.append(anime_info)
                            seen_ids.add(anime["mal_id"])
                            print(anime_info)

                    i += 1
                    errors = 0  # reset erreurs

                else:
                    print(f"Erreur page {i}: status {response.status_code}")
                    errors += 1
                    if errors >= 10:
                        print("Arrêt après 10 erreurs consécutives.")
                        break
                    i += 1

            except requests.exceptions.RequestException as e:
                print(f"Exception page {i}: {e}")
                errors += 1
                if errors >= 10:
                    print("Arrêt après 10 exceptions consécutives.")
                    break
                i += 1

            time.sleep(0.7)  # limiter à ~60 req/minute

        with open("AllAnimeId.json", "w", encoding="utf-8") as f:
            json.dump(anime_list, f, ensure_ascii=False, indent=4)

        # def getAllid():
    #     return 

    def clean_string(text):
        """Une fonction pour nettoyer et normaliser une chaîne de caractères."""
        if not text:
            return ""
        # Met tout en minuscule
        text = text.lower()
        # Ne garde que les lettres, les chiffres et les espaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Enlève les espaces en trop
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def serchAnime(search, limit):
        clean_string = Cardinal.clean_string
        try:
            animes_data = requests.get("http://127.0.0.1:5000/api/animeSearchAll").json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des animes: {e}")
            return []

        cleaned_search = clean_string(search)
        if not cleaned_search:
            return []

        # Utilisation de dictionnaires pour garantir l'unicité
        cleaned_to_original_map = {clean_string(anime.get("title")): anime.get("title") for anime in animes_data if anime.get("title")}
        cleaned_to_id_map = {clean_string(anime.get("title")): anime.get("id") for anime in animes_data if anime.get("title")}
        
        cleaned_titles = list(cleaned_to_original_map.keys())

        # On prend une marge plus large pour avoir assez de matière pour notre tri intelligent
        matches = process.extract(cleaned_search, cleaned_titles, scorer=fuzz.token_set_ratio, limit=15) 

        temp_results = []
        
        # --- LA CORRECTION EST ICI ---
        # La boucle DOIT accepter 3 valeurs. On ignore l'index avec `_`.
        for cleaned_title, score, _ in matches:
            if score < 75:
                continue

            # Logique de score intelligent
            length_ratio = len(cleaned_title) / len(cleaned_search) if len(cleaned_search) > 0 else 0
            specificity_bonus = 0
            if 0.9 <= length_ratio <= 1.1:
                specificity_bonus = 10
            elif length_ratio < 0.5:
                specificity_bonus = -15
                
            final_score = score + specificity_bonus

            original_title = cleaned_to_original_map.get(cleaned_title)
            anime_id = cleaned_to_id_map.get(cleaned_title)

            if original_title and anime_id:
                temp_results.append({
                    "title": original_title,
                    "id": anime_id,
                    "final_score": final_score
                })

        # Tri sur le score final
        temp_results.sort(key=lambda x: x["final_score"], reverse=True)

        # Logique anti-doublons et application de la limite
        final_results = []
        seen_ids = set()
        for res in temp_results:
            if len(final_results) >= limit:
                break
            if res["id"] not in seen_ids:
                # On peut aussi renommer la clé pour la sortie finale si on le souhaite
                res['score'] = res.pop('final_score')
                final_results.append(res)
                seen_ids.add(res["id"])
                
        return final_results