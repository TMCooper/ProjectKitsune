from flask import Flask, jsonify, request, render_template
import requests
from src.backend import Cardinal

class Yui:
    app = Flask(__name__)

    app.json.ensure_ascii = False

    @app.route('/api/topanime')
    def topanime():
        topanime = Cardinal.topanime()

        return jsonify({
            'topanime': topanime
        })
    
    @app.route('/api/getinfoByid', methods=["GET"])
    def getinfo_byid():
        # format : /api/getinfoByid?id=52991
        anime_id = request.args.get("id", "").strip()
        if not anime_id:
            return jsonify({"error": "Paramètre 'id' manquant"}), 400
        
        url, title, title_english, title_japanese, episodes_number, status, rating, rank, popularity, favorites, season, synopsis, background, studios_name, genres_name, image_jpg, image_jpg_small, image_jpg_big = Cardinal.getinfo_byid(anime_id)

        return jsonify({
            'anime_url' : url,
            'title' : title,
            'title_english' : title_english,
            'title_japanese' : title_japanese,
            'episodes_number' : episodes_number,
            'status' : status,
            'age_restriction' : rating,                     # rating = restriction d'âge
            'rank' : rank,
            'popularity' : popularity,
            'favorites' : favorites,
            'season' : season,                              # Saison a sa sortie printemps, été, autone, hiver
            'synopsis' : synopsis,
            'background' : background,                      # background = histoire de la license
            'studios_name' : studios_name,
            'genres_name' : genres_name,
            'image_jpg' : image_jpg,
            'image_jpg_small' : image_jpg_small,
            'image_jpg_big' : image_jpg_big
        })
    
    @app.route('/api/animeSearchAll')
    def animesearchall():
        return jsonify(Cardinal.AnimeId())
    
    @app.route('/api/getAnimeSearch', methods=["GET"])
    def getAnimeSearch():
        # Récupère la query de l’utilisateur : /api/getAnimeSearch?q=Frieren&l=1
        query = request.args.get("q", "").strip()
        limit = request.args.get("l", "").strip()
        if not query:
            return jsonify({"error": "Paramètre 'q' manquant"}), 400
        try:
            limit = int(limit) if limit else 5   # ✅ convertir en entier
        except ValueError:
            limit = 5  # valeur par défaut si l'argument est invalide
        
        results = Cardinal.serchAnime(query, limit)

        return jsonify(results)
    
    @app.route('/api/getAnimeNameToInfo', methods=["GET"])
    def nametoinfo():
        # Récupère la query de l’utilisateur : /api/NameToInfo?q=Frieren
        query = request.args.get("q", "").strip()
        if not query:
            return jsonify({"error": "Paramètre 'q' manquant"}), 400
        
        reponse = requests.get(f"http://127.0.0.1:5000/api/getAnimeSearch?q={query}&l=1").json()
        anime_id = reponse[0]["id"]

        anime_info = requests.get(f"http://127.0.0.1:5000/api/getinfoByid?id={anime_id}").json()

        return jsonify(anime_info)
    
    @app.route('/api/getUserList', methods=["GET"])    
    def getUserList():
        # u = Nom myanimelist de l'utilisateur obligatoire
        pseudo = request.args.get("u", "").strip()
        # s = status des animer a récuperer 1 à 7 par défault il est a 2 (complété) regarder la fonction getUserList dans la class Cardinal du fichier backend.py
        status = request.args.get("s", "").strip()

        if not pseudo:
            return jsonify({"error": "Paramètre 'u' manquant"})
        
        anime_ids = Cardinal.getUserList(pseudo, status)

        results = Cardinal.NameFinder(anime_ids)

        return jsonify(results)
    
    @app.route('/api/getCurrentOut', methods=["GET"]) # regarde quoi sort quand et a quel heur en fonction du jour choisit
    def getCurrentOut():
        day = request.args.get("day", "").strip().lower()
        
        if not day:
            return jsonify({"error": "Paramètre 'day' manquant"}), 400
        
        results = Cardinal.getCurrentOut(day)

        return jsonify(results)

    
    @app.route('/api/getSeasonOut', methods=["GET"]) # même principe que /api/getCurrentOut mais cette fois avec un system de saison d'année et de typage
    def getSeasonOut():
        year = request.args.get("y", "").strip()
        seasons = request.args.get("seasons", "").strip().lower()
        typage = request.args.get("typage", "").strip().lower()

        if not seasons:
            return jsonify({"error": "Paramètre 'seasons' manquant"}), 400
        if not year:
            return jsonify({"error": "Paramètre 'year' manquant"}), 400
        
        #typage disponible par défaut il est sur tv : "tv" "movie" "ova" "special" "ona" "music"
        
        results = Cardinal.getSeasons(seasons, year, typage )

        return jsonify(results)
    
    @app.route('/home/seasonsRender')
    def seasonsRender():
        return render_template('indexSeasons.html')
    
    @app.route('/home/DailyAnime')
    def DailyAnimeRender():
        return render_template('indexDailyAnime.html')
    
    @app.route('/home') # ou @app.route('/') si vous voulez que ce soit la racine
    def homeRender():
        return render_template('home.html')
    
    @app.route('/home/search')
    def searchRender():
        return render_template('search.html')
    
    @app.route('/api/translate', methods=['POST'])
    def translate_text_route():
        data = request.get_json()
        text_to_translate = data.get('text')
        target_language = data.get('target', 'fr') # 'fr' par défaut

        if not text_to_translate:
            return jsonify({"error": "Paramètre 'text' manquant"}), 400

        translated_text = Cardinal.translate_text(text_to_translate, target_language)

        return jsonify({"translated_text": translated_text})