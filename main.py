import os, json, platform
from src.api import Yui
from src.backend import Cardinal

PATH = os.getcwd()

if platform.system() == "Windows":
    PATH_ID = PATH + "\AllAnimeId.json"
else:
    PATH_ID = PATH + "/AllAnimeId.json"


def main():
    print(PATH)
    print(PATH_ID)

    if os.path.exists(PATH_ID): # Vérification si le fichier AllAnimeId.json est disponible si oui alors il lance l'api sinon il crée et remplit le fichier
        Yui.app.run(debug=True)

    else:
        print("Fichier non trouvée... créeation...")
        Cardinal.requestsAllid()
        main()

if __name__ == "__main__":
    main()