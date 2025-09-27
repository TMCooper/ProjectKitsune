import os
import json
import re

PATH = os.path.dirname(os.path.join(os.path.dirname(__file__))) 
PATH_VID = os.path.join(PATH, "Vidéo")
PATH_PLAY = os.path.join(PATH, "Playlist")
PATH_MP3 = os.path.join(PATH, "Musique")

class Holo:
    @staticmethod
    def index_dir(PATH_PLAY, PATH_MP3, PATH_VID):
        # travailler sur un system qui enregistrerait les noms de tous les éléments dans une liste json et pourquoi pas effectuer une comparaison a chaque itération et renvoier True ou False en 
        # fonction de si la liste contient le titre de la video afin d'allez plus vite encore qu'avec la biblyothèque
        # Récupère tous les noms de fichiers et dossiers dans le répertoire PATH
        
        # Charger ou initialiser le fichier JSON
        if os.path.exists("index.json"):
            with open("index.json", "r", encoding="utf-8") as index_file:
                try:
                    indexed_files = json.load(index_file)
                except json.JSONDecodeError:
                    indexed_files = {"files": []}
        else:
            indexed_files = {"files": []}

        # Récupérer tous les fichiers dans le répertoire
        new_files = []

        # Liste des répertoires à parcourir
        directories = [PATH_PLAY, PATH_MP3, PATH_VID]

        for directory in directories:
            if not os.path.exists(directory):  # Vérifier si le répertoire existe
                print(f"Répertoire non trouvé : {directory}")
                continue

            # Récupérer les fichiers du répertoire
            for file in os.listdir(directory):
                if file.endswith(".mp4") or file.endswith(".mp3"):
                    if file not in indexed_files["files"]:  # Vérifier si le fichier est déjà indexé
                        indexed_files["files"].append(file)
                        new_files.append(file)

        # Mettre à jour le fichier JSON
        with open("index.json", "w", encoding="utf-8") as index_file:
            json.dump(indexed_files, index_file, ensure_ascii=False, indent=4)

        # Retourner True si de nouveaux fichiers ont été ajoutés, sinon False
        return len(new_files) > 0
    
    def index_read(choix, mp_v, titre):
        
        # LOCAL_PATH = Holo.verification(choix, mp_v)   
        titre = Holo.extract_info(titre)

        with open("index.json", "r", encoding="utf-8") as index_file:
            titre_json = json.load(index_file)
        
        if titre in titre_json["files"]:
            return True

        else:
            print(f"Le titre : {titre} n'est pas dans la liste.")
            print(titre_json["files"])
            return False
    
    def verification(choix, mp_v):
        if choix == "v":
            if mp_v == "mp4":
                LOCAL_PATH =  PATH_VID
            elif mp_v == "mp3":
                LOCAL_PATH =  PATH_MP3
        
        if choix == "p":
            if mp_v == "mp4":
                LOCAL_PATH =  PATH_PLAY
            elif mp_v == "mp3":
                LOCAL_PATH =  PATH_MP3
        
        return LOCAL_PATH

    def extract_info(file_name):
        # Enlever l'extension pour travailler uniquement avec le nom de fichier
        base_name = re.sub(r"\.[a-zA-Z0-9]+$", "", file_name)
        # Diviser le nom en parties basées sur certains séparateurs
        parts = re.split(r" - | \| |\｜｜|⧸", base_name)
        return {
            "original_name": file_name,
            "title": parts[0].strip() if parts else "Unknown",
            "details": [part.strip() for part in parts[1:]] if len(parts) > 1 else []
        }