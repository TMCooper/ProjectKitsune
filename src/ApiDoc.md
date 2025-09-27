# Documentation Api


## getUserList
    @app.route('/api/getUserList', methods=["GET"])

la route getUserList possède deux arguments dans se format : ``/api/getUserList?u={user}&s={status}`` le status que vous préciser sera part défaut a 2 si vous ne préciser rien car c'est une liste ne comprenant uniquement que les animer complété de celle ci dans le cas ou vous souhaité autre chose voici la liste

### Status variation de 1 a 7
        1 = Watching
        2 = Completed
        3 = On-Hold
        4 = Dropped
        6 = Plan to Watch
        7 = All anime

Donc si vous souhaité que le downloader d'opening par exemple ne prenne que se que vous regarder en se moment hé bien la requette il vous faudra préciser 3 pour le status pour l'instant cela se passera [ici](../opening_downloader/api_client.py) a la ligne 12