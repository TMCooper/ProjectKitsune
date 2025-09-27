import ctypes
import sys
import subprocess
import os

class Yui:
    def is_admin():
    # Vérifie si le script est exécuté avec les droits administratifs
        try:
            # Pour windows
            return ctypes.windll.shell32.IsUserAnAdmin()
        except AttributeError:
            # Pour Linux/Unix
            return os.geteuid() == 0
        
    def reset_proxy():
        """
        Réinitialise le proxy système.
        """
        if sys.platform == 'win32':
            subprocess.run('netsh winhttp reset proxy', shell=True, check=True)
        else:
            # Sous Linux, la réinitialisation se fait souvent en supprimant les variables d'environnement
            for var in ['http_proxy', 'https_proxy', 'ftp_proxy']:
                if var in os.environ:
                    del os.environ[var]
            # Pour une configuration à l'échelle du système (nécessite les droits root)
            # Cette partie peut varier selon la distribution Linux
            # Exemple pour les systèmes basés sur Debian/Ubuntu :
            if os.path.exists('/etc/environment'):
                with open('/etc/environment', 'r') as f:
                    lines = f.readlines()
                with open('/etc/environment', 'w') as f:
                    for line in lines:
                        if not any(proxy_var in line.lower() for proxy_var in ['http_proxy', 'https_proxy', 'ftp_proxy']):
                            f.write(line)

    def set_proxy(proxy_url):
        """
        Définit le proxy système.
        """
        if sys.platform == 'win32':
            command = f'netsh winhttp set proxy proxy-server="{proxy_url}"'
            subprocess.run(command, shell=True, check=True)
        else:
            # Définit les variables d'environnement pour la session actuelle
            os.environ['http_proxy'] = f'http://{proxy_url}'
            os.environ['https_proxy'] = f'https://{proxy_url}'
            os.environ['ftp_proxy'] = f'ftp://{proxy_url}'
            # Pour une configuration persistante (nécessite les droits root)
            # Exemple pour les systèmes basés sur Debian/Ubuntu :
            if os.path.exists('/etc/environment'):
                 with open('/etc/environment', 'a') as f:
                    f.write(f'\nhttp_proxy="http://{proxy_url}"\n')
                    f.write(f'https_proxy="https://{proxy_url}"\n')

    def run_as_admin():
        """
        Relance le script avec des privilèges administratifs.
        """
        if sys.platform == 'win32':
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
            # Relance le script avec sudo sous Linux
            subprocess.run(['sudo', 'python3'] + sys.argv)