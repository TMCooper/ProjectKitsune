# ProjectKitsune

## Script Opening

Le script pour télécharger les opening de la watchlist de myanimelist est disponible [ici](../opening_downloader/main.py) mais il faut que l'[api](main.py) sois lancer

## Route disponible
    @app.route('/api/topanime')
    # Retourne un json avec le top anime du moment 
    
    @app.route('/api/getinfoByid', methods=["GET"])
    # format : /api/getinfoByid?id=52991
    # Retourne les plein d'information de base de l'animer
    
    @app.route('/api/animeSearchAll')
    # Retourne une liste complete id et nom dans le même json (AllAnimeId.json)
   
    @app.route('/api/getAnimeSearch', methods=["GET"])
    # Récupère la query de l’utilisateur : /api/getAnimeSearch?q=Frieren&l=1
    # Retourne le resultat d'une recherche avec un agument ici q qui contien le nom de l'anime celui ci retourne donc un resultat filtré avec le nom le plus probable en fonction de la querry
    
    @app.route('/api/NameToInfo', methods=["GET"])
    # Récupère la query de l’utilisateur : /api/NameToInfo?q=Frieren
    # retourne les information complete d'un animer mais ici pas besoins de connaitre l'id le system fait la jonction automatiquement entre le nom et l'id de celui ci affin que en une seul requete l'animer le plus probable sois renvoier avec toute ses informations de base


    @app.route('/api/getUserList', methods=["GET"])    
    # Format : /api/getUserList?u={user}
        # u = Nom myanimelist de l'utilisateur obligatoire
        # s = status des animer a récuperer 1 à 7 par défault il est a 2 (complété) regarder (ici)[../doc/ApiDoc.md]

## Coming Soon

[ ] Ajouter une option au démarage du mains de l'opening downloader pour demander se si l'utilisateur désire avoir autre chose que uniquement les animer completé

## Thanks to
[Jikan Api](https://jikan.moe)