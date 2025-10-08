# 📖 Documentation API Yui

**Interface complète pour récupérer des informations sur les animés**

**URL de base** : Toutes les routes de l'API sont préfixées par `/api`

---

## 📑 Table des Matières

1. [Routes Principales](#-routes-principales)
   - [GET /api/topanime](#get-apitopanime)
   - [GET /api/getinfoByid](#get-apigetinfobyid)
   - [GET /api/getAnimeSearch](#get-apigetanimesearch)
   - [GET /api/getAnimeNameToInfo](#get-apigetanimenametoinfo)
   - [GET /api/getCurrentOut](#get-apigetcurrentout)
   - [GET /api/getSeasonOut](#get-apigetseasonout)
2. [Routes Utilisateur](#-routes-utilisateur)
   - [GET /api/getUserList](#get-apigetuserlist)
3. [Routes Utilitaires](#-routes-utilitaires)
   - [GET /api/botStatus](#get-apibotstatus)
   - [POST /api/translate](#post-apitranslate)
4. [Routes d'Administration](#-routes-dadministration)
   - [POST /admin/verify](#post-adminverify)
   - [POST /admin/update](#post-adminupdate)

---

## 🎯 Routes Principales

### GET `/api/topanime`

Récupère une liste des animés les mieux classés sur MyAnimeList.

**Méthode** : `GET`

**Paramètres** : Aucun

**Exemple de Requête** :
```
GET /api/topanime
```

**Réponse (200 OK)** :
```json
{
  "topanime": [
    {
      "mal_id": 5114,
      "title": "Fullmetal Alchemist: Brotherhood",
      "rank": 1,
      "..."
    }
  ]
}
```

---

### GET `/api/getinfoByid`

Récupère les informations détaillées d'un animé via son ID MyAnimeList.

**Méthode** : `GET`

**Paramètres** :

| Nom | Type    | Requis | Description                            |
|-----|---------|--------|----------------------------------------|
| `id`| entier  | ✅ Oui | L'ID unique de l'animé sur MyAnimeList |

**Exemple de Requête** :
```
GET /api/getinfoByid?id=52991
```

**Réponse (200 OK)** :
```json
{
  "anime_url": "https://myanimelist.net/anime/52991/Sousou_no_Frieren",
  "title": "Sousou no Frieren",
  "title_english": "Frieren: Beyond Journey's End",
  "title_japanese": "葬送のフリーレン",
  "episodes_number": 28,
  "status": "Finished Airing",
  "age_restriction": "PG-13 - Teens 13 or older",
  "rank": 1,
  "popularity": 222,
  "favorites": 59800,
  "season": "fall",
  "synopsis": "The story follows the elven mage Frieren...",
  "background": "Sousou no Frieren was released on Blu-ray...",
  "studios_name": ["Madhouse"],
  "genres_name": ["Adventure", "Drama", "Fantasy"],
  "image_jpg": "https://cdn.myanimelist.net/images/anime/1015/138006.jpg",
  "image_jpg_small": "https://cdn.myanimelist.net/images/anime/1015/138006t.jpg",
  "image_jpg_big": "https://cdn.myanimelist.net/images/anime/1015/138006l.jpg"
}
```

**Réponse d'Erreur (400 Bad Request)** :
```json
{
  "error": "Paramètre 'id' manquant"
}
```

---

### GET `/api/getAnimeSearch`

Recherche des animés par nom avec correspondance floue intelligente utilisant RapidFuzz.

**Méthode** : `GET`

**Paramètres** :

| Nom | Type    | Requis | Description                                    |
|-----|---------|--------|------------------------------------------------|
| `q` | chaîne  | ✅ Oui | Le terme de recherche                          |
| `l` | entier  | ❌ Non | Nombre de résultats à retourner (défaut: 5)    |

**Exemple de Requête** :
```
GET /api/getAnimeSearch?q=Frieren&l=2
```

**Réponse (200 OK)** :
```json
[
  {
    "id": 52991,
    "title": "Sousou no Frieren",
    "image_jpg": "https://cdn.myanimelist.net/images/anime/1015/138006.jpg",
    "score": 95.5
  },
  {
    "id": 56514,
    "title": "Sousou no Frieren: Hito no Kokoro o Shiru Mahou",
    "image_jpg": "https://cdn.myanimelist.net/...",
    "score": 87.3
  }
]
```

**Réponse d'Erreur (400 Bad Request)** :
```json
{
  "error": "Paramètre 'q' manquant"
}
```

**Notes** :
- Utilise un algorithme de correspondance floue avec score de pertinence
- Filtre automatiquement les doublons
- Score ajusté en fonction de la longueur et de la spécificité du titre

---

### GET `/api/getAnimeNameToInfo`

Combine recherche et récupération d'informations pour retourner directement les détails du premier résultat d'une recherche.

**Méthode** : `GET`

**Paramètres** :

| Nom | Type    | Requis | Description                     |
|-----|---------|--------|---------------------------------|
| `q` | chaîne  | ✅ Oui | Le nom de l'animé à rechercher  |

**Exemple de Requête** :
```
GET /api/getAnimeNameToInfo?q=Steins;Gate
```

**Réponse (200 OK)** :
```json
{
  "anime_url": "https://myanimelist.net/anime/9253/Steins_Gate",
  "title": "Steins;Gate",
  "title_english": "Steins;Gate",
  "title_japanese": "STEINS;GATE",
  "episodes_number": 24,
  "status": "Finished Airing",
  "age_restriction": "PG-13 - Teens 13 or older",
  "rank": 2,
  "..."
}
```

**Notes** :
- La réponse est identique à celle de `/api/getinfoByid`
- Effectue une recherche puis récupère automatiquement les détails du premier résultat

---

### GET `/api/getCurrentOut`

Récupère les animés diffusés un jour spécifique de la semaine.

**Méthode** : `GET`

**Paramètres** :

| Nom  | Type    | Requis | Description                                              |
|------|---------|--------|----------------------------------------------------------|
| `day`| chaîne  | ✅ Oui | Jour de la semaine en minuscules (monday, tuesday, etc.) |

**Jours acceptés** :
- En anglais : `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`
- En français : `lundi`, `mardi`, `mercredi`, `jeudi`, `vendredi`, `samedi`, `dimanche`

**Exemple de Requête** :
```
GET /api/getCurrentOut?day=friday
```

**Réponse (200 OK)** :
```json
[
  {
    "mal_id": 12345,
    "title": "Example Anime",
    "url": "https://myanimelist.net/anime/12345/...",
    "studios_name": ["Studio Name"],
    "genres_name": ["Action", "Adventure"],
    "image_jpg": "https://cdn.myanimelist.net/...",
    "image_jpg_small": "https://cdn.myanimelist.net/...t.jpg",
    "image_jpg_big": "https://cdn.myanimelist.net/...l.jpg",
    "episodes_number": 12,
    "status": "Currently Airing",
    "rating": "PG-13",
    "rank": 150
  }
]
```

**Réponse d'Erreur (400 Bad Request)** :
```json
{
  "error": "Paramètre 'day' manquant"
}
```

---

### GET `/api/getSeasonOut`

Récupère les animés d'une saison, d'une année et d'un type spécifiques.

**Méthode** : `GET`

**Paramètres** :

| Nom      | Type    | Requis | Description                                              |
|----------|---------|--------|----------------------------------------------------------|
| `y`      | entier  | ✅ Oui | L'année de diffusion (ex: 2024)                          |
| `seasons`| chaîne  | ✅ Oui | La saison (winter, spring, summer, fall)                 |
| `typage` | chaîne  | ❌ Non | Le type d'animé (tv, movie, ova, special, ona, music)    |

**Saisons acceptées** :
- En anglais : `winter`, `spring`, `summer`, `fall`
- En français : `hiver`, `printemps`, `été`/`ete`, `automne`

**Types disponibles** :
- `tv` (défaut)
- `movie`
- `ova`
- `special`
- `ona`
- `music`

**Exemple de Requête** :
```
GET /api/getSeasonOut?y=2023&seasons=fall&typage=tv
```

**Réponse (200 OK)** :
```json
[
  {
    "mal_id": 52991,
    "title": "Sousou no Frieren",
    "url": "https://myanimelist.net/anime/52991/...",
    "studios_name": ["Madhouse"],
    "genres_name": ["Adventure", "Drama", "Fantasy"],
    "image_jpg": "https://cdn.myanimelist.net/...",
    "image_jpg_small": "https://cdn.myanimelist.net/...t.jpg",
    "image_jpg_big": "https://cdn.myanimelist.net/...l.jpg",
    "episodes_number": 28,
    "status": "Finished Airing",
    "rating": "PG-13",
    "rank": 1
  }
]
```

**Réponses d'Erreur** :
```json
// 400 Bad Request - Saison manquante
{
  "error": "Paramètre 'seasons' manquant"
}

// 400 Bad Request - Année manquante
{
  "error": "Paramètre 'year' manquant"
}
```

---

## 👤 Routes Utilisateur

### GET `/api/getUserList`

Récupère la liste d'animés d'un utilisateur MyAnimeList avec un statut spécifique.

**Méthode** : `GET`

**Paramètres** :

| Nom | Type    | Requis | Description                                    |
|-----|---------|--------|------------------------------------------------|
| `u` | chaîne  | ✅ Oui | Le pseudonyme de l'utilisateur MyAnimeList     |
| `s` | entier  | ❌ Non | Le statut des animés à récupérer (1-7, défaut: 2) |

**Valeurs de Statut** :

| Valeur | Statut         | Description                |
|--------|----------------|----------------------------|
| 1      | Watching       | En cours de visionnage     |
| 2      | Completed      | Complétés (défaut)         |
| 3      | On-Hold        | En pause                   |
| 4      | Dropped        | Abandonnés                 |
| 6      | Plan to Watch  | Prévu de regarder          |
| 7      | All anime      | Tous les animés            |

**Exemple de Requête** :
```
GET /api/getUserList?u=TMCooper&s=1
```

**Réponse (200 OK)** :
```json
[
  {
    "anime_id": 52991,
    "title": "Sousou no Frieren",
    "title_english": "Frieren: Beyond Journey's End",
    "title_japanese": "葬送のフリーレン"
  },
  {
    "anime_id": 9253,
    "title": "Steins;Gate",
    "title_english": "Steins;Gate",
    "title_japanese": "STEINS;GATE"
  }
]
```

**Réponse d'Erreur (400 Bad Request)** :
```json
{
  "error": "Paramètre 'u' manquant"
}
```

---

## 🔧 Routes Utilitaires

### GET `/api/botStatus`

Récupère le statut actuel du bot Discord observé par le script `discordObserver.py`.

**Méthode** : `GET`

**Paramètres** : Aucun

**Exemple de Requête** :
```
GET /api/botStatus
```

**Réponse (200 OK)** :
```json
{
  "id": 123456789012345678,
  "username": "NomDuBot",
  "status": "online",
  "avatar": "https://cdn.discordapp.com/avatars/.../....png",
  "banner": "https://cdn.discordapp.com/banners/.../....png",
  "last_updated": 1678886400.0
}
```

**Réponse d'Erreur - Timeout** :
```json
{
  "error": "Le bot n'a pas répondu à temps (Timeout).",
  "status": "timeout"
}
```

**Notes** :
- Cette route utilise un système de trigger pour demander une mise à jour en temps réel
- Le bot Discord doit être en cours d'exécution et partager un serveur avec le bot cible
- Timeout de 5 secondes maximum
- Les statuts possibles : `online`, `idle`, `dnd`, `offline`

---

### POST `/api/translate`

Traduit un texte donné vers une langue cible en utilisant Google Translate.

**Méthode** : `POST`

**Content-Type** : `application/json`

**Corps de la Requête (JSON)** :

| Clé      | Type    | Requis | Description                                    |
|----------|---------|--------|------------------------------------------------|
| `text`   | chaîne  | ✅ Oui | Le texte à traduire                            |
| `target` | chaîne  | ❌ Non | Code de la langue cible (ex: 'fr', 'en'). Défaut: 'fr' |

**Codes de Langue Courants** :
- `fr` - Français
- `en` - Anglais
- `ja` - Japonais
- `es` - Espagnol
- `de` - Allemand
- `it` - Italien

**Exemple de Requête** :
```bash
POST /api/translate
Content-Type: application/json

{
  "text": "Hello, world!",
  "target": "fr"
}
```

**Réponse (200 OK)** :
```json
{
  "translated_text": "Bonjour, le monde !"
}
```

**Réponse d'Erreur (400 Bad Request)** :
```json
{
  "error": "Paramètre 'text' manquant"
}
```

**Notes** :
- La détection de la langue source est automatique
- Utilise la bibliothèque `deep_translator` avec Google Translate

---

## 🔐 Routes d'Administration

### POST `/admin/verify`

Vérifie le mot de passe administrateur pour accéder aux fonctions d'administration.

**Méthode** : `POST`

**Content-Type** : `application/json`

**Corps de la Requête (JSON)** :

| Clé        | Type    | Requis | Description               |
|------------|---------|--------|---------------------------|
| `password` | chaîne  | ✅ Oui | Mot de passe administrateur |

**Exemple de Requête** :
```bash
POST /admin/verify
Content-Type: application/json

{
  "password": "votre_mot_de_passe"
}
```

**Réponse - Succès (200 OK)** :
```json
{
  "success": true
}
```

**Réponse - Échec (401 Unauthorized)** :
```json
{
  "success": false
}
```

---

### POST `/admin/update`

Exécute un `git pull` pour mettre à jour le site avec les derniers changements du dépôt.

**Méthode** : `POST`

**Content-Type** : `application/json`

**Corps de la Requête (JSON)** :

| Clé        | Type    | Requis | Description               |
|------------|---------|--------|---------------------------|
| `password` | chaîne  | ✅ Oui | Mot de passe administrateur |

**Exemple de Requête** :
```bash
POST /admin/update
Content-Type: application/json

{
  "password": "votre_mot_de_passe"
}
```

**Réponse - Succès (200 OK)** :
```json
{
  "output": "Mise à jour réussie !\n\nAlready up to date."
}
```

**Réponses d'Erreur** :

```json
// 403 Forbidden - Mot de passe invalide
{
  "error": "Mot de passe invalide ou manquant."
}

// 500 Internal Server Error - Git non trouvé
{
  "error": "La commande 'git' n'a pas été trouvée. Git est-il installé sur le serveur ?"
}

// 500 Internal Server Error - Échec du git pull
{
  "error": "La commande git a échoué.\n\n[sortie de l'erreur]"
}
```

**⚠️ Sécurité** :
- Le mot de passe administrateur doit être défini dans la variable d'environnement `ADMIN_PASSWORD`
- Cette route nécessite Git installé sur le serveur
- Peut échouer en cas de conflits de fusion

---

## 📊 Informations Techniques

### Technologies Utilisées

- **Framework** : Flask (Python)
- **API Externe** : Jikan API v4 (MyAnimeList)
- **Traduction** : deep_translator (Google Translate)
- **Recherche Floue** : RapidFuzz
- **Bot Discord** : discord.py
- **Format de Données** : JSON

### Rate Limiting

L'API Jikan impose des limites de requêtes :
- **1 requête par seconde** recommandée
- **3 requêtes par seconde** maximum
- Utilisez la mise en cache locale quand c'est possible

### Variables d'Environnement Requises

```env
HOLO=<votre_token_discord>
BOT_ID=<id_du_bot_discord_à_observer>
ADMIN_PASSWORD=<mot_de_passe_admin>
```

### Fichiers Nécessaires

- `AllAnimeId.json` - Base de données locale des animés (générée via `requestsAllid()`)
- `src/shared_files/bot_status.json` - Statut du bot Discord
- `src/shared_files/refresh.trigger` - Fichier trigger pour le rafraîchissement

---

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/TMCooper/ProjectKitsune.git
cd ProjectKitsune

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs
```

### Lancement

```bash
# Lancer l'API Flask
python main.py

# L'API sera accessible sur http://127.0.0.1:5000
```

---

## 📝 Exemples d'Utilisation

### Python (requests)

```python
import requests

# Rechercher un animé
response = requests.get('http://127.0.0.1:5000/api/getAnimeSearch', params={
    'q': 'Frieren',
    'l': 5
})
animes = response.json()

# Obtenir les détails d'un animé
response = requests.get('http://127.0.0.1:5000/api/getinfoByid', params={
    'id': 52991
})
anime_info = response.json()

# Traduire du texte
response = requests.post('http://127.0.0.1:5000/api/translate', json={
    'text': 'Hello world',
    'target': 'fr'
})
translation = response.json()
```

### JavaScript (fetch)

```javascript
// Rechercher un animé
fetch('http://127.0.0.1:5000/api/getAnimeSearch?q=Frieren&l=5')
  .then(response => response.json())
  .then(data => console.log(data));

// Traduire du texte
fetch('http://127.0.0.1:5000/api/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Hello world',
    target: 'fr'
  })
})
  .then(response => response.json())
  .then(data => console.log(data.translated_text));
```

### cURL

```bash
# Rechercher un animé
curl "http://127.0.0.1:5000/api/getAnimeSearch?q=Frieren&l=5"

# Obtenir les détails d'un animé
curl "http://127.0.0.1:5000/api/getinfoByid?id=52991"

# Traduire du texte
curl -X POST "http://127.0.0.1:5000/api/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target": "fr"}'
```

---

## 🐛 Gestion des Erreurs

Toutes les erreurs suivent un format JSON standardisé :

```json
{
  "error": "Description de l'erreur"
}
```

### Codes de Statut HTTP

| Code | Signification        | Description                                    |
|------|----------------------|------------------------------------------------|
| 200  | OK                   | Requête réussie                                |
| 400  | Bad Request          | Paramètres manquants ou invalides              |
| 401  | Unauthorized         | Authentification échouée                       |
| 403  | Forbidden            | Accès refusé (mot de passe invalide)           |
| 500  | Internal Server Error| Erreur du serveur                              |

---

## 📄 Licence

Ce projet est développé pour les passionnés d'animation.

**Lien du projet** : [ProjectKitsune sur GitHub](https://github.com/TMCooper/ProjectKitsune)

---

## 🙏 Crédits

- **API Anime** : [Jikan API](https://jikan.moe/) - Interface non officielle de MyAnimeList
- **Données** : [MyAnimeList](https://myanimelist.net/)
- **Framework** : [Flask](https://flask.palletsprojects.com/)
- **Discord Bot** : [discord.py](https://discordpy.readthedocs.io/)

---

**Dernière mise à jour** : Octobre 2024 (Ceci a été fais par une ia)