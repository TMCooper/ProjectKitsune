# api_client.py
import requests

API_BASE_URL = "http://127.0.0.1:5000/api"

def get_user_anime_list(username, status=2):
    """
    Interroge ton API pour récupérer la liste d'animes d'un utilisateur.
    Renvoie une liste de dictionnaires ou None en cas d'erreur.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/getUserList?u={username}&s={status}")
        response.raise_for_status()  # Lève une erreur si le statut n'est pas 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la communication avec l'API : {e}")
        return None