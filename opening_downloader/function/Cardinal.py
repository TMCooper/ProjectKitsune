from function.Yui import *
import yt_dlp as youtube_dl
import os
import json

class Cardinal:
    def Playlist_downloader(yt_play_videos, mp_v, lang, languages, PATH_PLAY, PATH_MP3):
        for i in yt_play_videos:
                Yui.set_proxy('https://218.155.31.188:8080')
                
                if mp_v == "mp4" : 
                    link_vid = i.watch_url
                    yt = youtube_dl.YoutubeDL({'outtmpl': os.path.join(PATH_PLAY, '%(title)s.%(ext)s'),
                                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                            })
                    dl_vid = yt.extract_info(link_vid, download=True)
                    title = dl_vid["title"]
                    
                    print(languages[lang]["success_download"].format(title=title, path=PATH_PLAY))
                    
                    subprocess.run("cls", shell=True)

                if mp_v == "mp3":
                    link_vid = i.watch_url
                    yt = youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': os.path.join(PATH_MP3, '%(title)s.%(ext)s'),
                                            'postprocessors': [{
                                                'key': 'FFmpegExtractAudio',
                                                'preferredcodec': 'mp3',
                                                'preferredquality': '192',
                                                }]
                                                })
                    dl_vid = yt.extract_info(link_vid, download=True)
                    title = dl_vid["title"]
                    
                    print(languages[lang]["success_download"].format(title=title, path=PATH_PLAY))
                    
                    subprocess.run("cls", shell=True)
        
    def Video_downloader(video, mp_v, lang, languages, PATH_VID, PATH_MP3):
        try:
            if mp_v == "mp4":
                # Utilisation d'options plus flexibles pour le format
                yt = youtube_dl.YoutubeDL({
                    'outtmpl': os.path.join(PATH_VID, '%(title)s.%(ext)s'),
                    'format': 'best[ext=mp4]/bestvideo[ext=mp4]+bestaudio/best',  # Format plus flexible
                    'ignoreerrors': True,  # Ignorer certaines erreurs non critiques
                    'verbose': True  # Afficher plus d'informations
                })
                ytv = yt.extract_info(video, download=True)
                if ytv:
                    title = ytv.get("title", "Video") 
                    print(languages[lang]["success_download"].format(title=title, path=PATH_VID))
                else:
                    print(languages[lang].get("download_failed", "Téléchargement échoué"))
                
            elif mp_v == "mp3":
                yt = youtube_dl.YoutubeDL({
                    'format': 'bestaudio/best', 
                    'outtmpl': os.path.join(PATH_MP3, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'ignoreerrors': True,
                    'verbose': True
                })
                ytv = yt.extract_info(video, download=True)
                if ytv:
                    title = ytv.get("title", "Audio") 
                    print(languages[lang]["success_download"].format(title=title, path=PATH_MP3))  # Correction du chemin ici
                else:
                    print(languages[lang].get("download_failed", "Téléchargement échoué"))
            else:
                print(languages[lang].get("invalid_format", "Format non valide. Utilisez mp3 ou mp4."))
        
        except Exception as e:
            print(f"Erreur lors du téléchargement: {str(e)}")
            print("Essai avec les formats disponibles...")
            
            # Afficher les formats disponibles
            with youtube_dl.YoutubeDL({'listformats': True}) as ydl:
                ydl.download([video])
            
            print("Veuillez réessayer en choisissant un format disponible ou en utilisant 'best' comme format.")

    
    def basic():
        valid_languages = ["en", "fr"]

        with open('languages.json', 'r') as lang_file:
            languages = json.load(lang_file)

        print(f"Available languages: {', '.join(valid_languages).upper()}")
        lang = input("What is your language ? : ").lower()

        while lang not in valid_languages:
            print(f"Available languages: {', '.join(valid_languages).upper()}")
            lang = input("Please select your language: ").lower()

        choix = input(languages[lang]["User_request_P_V"]).lower()

        # Condition corrigée pour vérifier l'entrée utilisateur
        while choix not in ["p", "v", "q"]:
            choix = input(languages[lang]["Force_user_request_P_V"]).lower()

        mp_v = input(languages[lang]["check_extention"]).lower()
        
        while mp_v not in ["mp3", "mp4"]:
            mp_v = input(languages[lang]["error_mp_v"])
        
        return lang, languages, choix, mp_v