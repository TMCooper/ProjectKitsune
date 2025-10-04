# Si vous souhaité observer un bot en particulier il vous faut partager un serveur discord

import discord, os, threading, asyncio, json, time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('HOLO')
BOT_ID_STR = os.getenv('BOT_ID')
TARGET_BOT_ID = int(BOT_ID_STR) if BOT_ID_STR else None # Conversion obligatoire pour l'id target (str a int)

# --- DÉFINITION DES CHEMINS DES FICHIERS PARTAGÉS ---
BASE_DIR = os.getcwd()
SRC = os.path.join(BASE_DIR, "src")
PATH = os.path.join(SRC, "shared_files")
os.makedirs(PATH, exist_ok=True) # Verification de l'existance du PATH
STATUS_FILE_PATH = os.path.join(PATH, 'bot_status.json') # Le fichier de résultat
TRIGGER_FILE_PATH = os.path.join(PATH, 'refresh.trigger') # La "sonnette"

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

# Fonction helper pour faire la mise à jour (extraite pour la clarté)
async def perform_update():
    print("Demande de rafraîchissement reçue. Mise à jour...")
    status_data = {}
    target_member = None

    if not TARGET_BOT_ID:
        status_data = {"error": "ID cible non configuré.", "status": "unknown"}
    else:
        found = False
        for guild in client.guilds:
            try:
                # On utilise fetch_member pour avoir les données les plus FRAÎCHES possibles
                member = await guild.fetch_member(TARGET_BOT_ID)
                if member:
                    target_member = member
                    found = True
                    break # Trouvé sur un serveur, pas besoin de chercher ailleurs
            except discord.NotFound:
                continue
            except Exception as e:
                print(f"Erreur lors du fetch sur {guild.name}: {e}")
        
        if not found:
             status_data = {"error": "Bot cible introuvable.", "id": TARGET_BOT_ID, "status": "not_found"}
        else:
            user_profile = await client.fetch_user(target_member.id)

            # Astuce : on ajoute un timestamp unique pour que l'API détecte le changement
            status_data = {
                "id": target_member.id,
                "username": target_member.name,
                "status": str(target_member.status),
                "avatar": str(target_member.avatar.url) if target_member.avatar else None,
                "banner": str(user_profile.banner.url) if user_profile.banner else None,
                "last_updated": time.time() # Timestamp actuel
            }

    # Écriture du résultat
    try:
        # On écrit d'abord dans un fichier temporaire puis on renomme pour éviter une lecture partielle
        temp_path = STATUS_FILE_PATH + ".tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, ensure_ascii=False, indent=4)
        os.replace(temp_path, STATUS_FILE_PATH) # Remplacement atomique
    except Exception as e:
        print(f"Erreur écriture JSON: {e}")

# --- LA NOUVELLE TÂCHE DE SURVEILLANCE ---
async def trigger_watcher_task():
    await client.wait_until_ready()
    print("Le bot écoute les demandes de rafraîchissement...")
    
    # On fait une première mise à jour au démarrage pour avoir des données
    await perform_update()

    while not client.is_closed():
        # On regarde si le fichier "sonnette" existe
        if os.path.exists(TRIGGER_FILE_PATH):
            try:
                # 1. On fait la mise à jour
                await perform_update()
                # 2. On supprime la sonnette pour dire qu'on a fini
                os.remove(TRIGGER_FILE_PATH)
            except OSError as e:
                print(f"Erreur lors de la gestion du trigger: {e}")
        
        # On vérifie souvent (toutes les 0.5 secondes max)
        await asyncio.sleep(0.5)

@client.event
async def on_ready():
    print("="*30)
    print(f"Bot OBSERVATEUR connecté : {client.user.name}")
    client.loop.create_task(trigger_watcher_task())
    print("="*30)

# ... (run_discord et runChecker restent identiques) ...
def run_discord():
    if not TOKEN: return
    client.run(TOKEN)

def runChecker():
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        discord_thread = threading.Thread(target=run_discord)
        discord_thread.daemon = True
        discord_thread.start()
