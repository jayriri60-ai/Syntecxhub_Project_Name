import socket

import sys

from datetime import datetime

from concurrent.futures import ThreadPoolExecutor

def scan_port(target_ip, port):

    """

    Tente de se connecter à un port spécifique sur l'adresse IP cible.

    Retourne le port s'il est ouvert, sinon None.

    """

    try:

        # Création d'un socket TCP/IP

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(1.0) # Délai d'attente de 1 seconde

        result = s.connect_ex((target_ip, port))

        s.close()

        

        if result == 0:

            return port

    except socket.error:

        pass

    return None

def main():

    print("-" * 50)

    print("  SYNTECXHUB - PROJET 1 : SCANNER DE PORTS TCP")

    print("-" * 50)

    

    # Saisie de la cible

    target_input = input("Entrez l'adresse IP ou le nom de domaine de la cible (ex: 127.0.0.1 ou scanme.nmap.org) : ").strip()

    

    try:

        target_ip = socket.gethostbyname(target_input)

    except socket.gaierror:

        print("[-] Erreur : Impossible de résoudre le nom d'hôte.")

        sys.exit()

    # Saisie de la plage de ports

    try:

        start_port = int(input("Port de début (ex: 1) : "))

        end_port = int(input("Port de fin (ex: 1024) : "))

    except ValueError:

        print("[-] Erreur : Veuillez entrer des numéros de ports valides.")

        sys.exit()

    print(f"\n[+] Démarrage du scan sur la cible : {target_ip}")

    print(f"[+] Plage de ports : {start_port} à {end_port}")

    print(f"[+] Heure de début : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("-" * 50)

    open_ports = []

    start_time = datetime.now()

    # Utilisation d'un ThreadPoolExecutor pour accélérer le scan (concurrence)

    with ThreadPoolExecutor(max_workers=100) as executor:

        futures = {executor.submit(scan_port, target_ip, port): port for port in range(start_port, end_port + 1)}

        

        for future in futures:

            port = futures[future]

            try:

                res = future.result()

                if res:

                    print(f"[+] Port {port} : OUVERT")

                    open_ports.append(port)

            except Exception as e:

                pass

    end_time = datetime.now()

    duration = end_time - start_time

    print("-" * 50)

    print(f"[+] Scan terminé en {duration}")

    print(f"[+] Ports ouverts trouvés : {open_ports if open_ports else 'Aucun'}")

    

    # Journalisation (Logging) des résultats dans un fichier texte

    log_filename = f"scan_report_{target_ip.replace('.', '_')}.txt"

    with open(log_filename, "w") as log_file:

        log_file.write(f"Rapport de Scan de Ports - Syntecxhub\\n")

        log_file.write(f"Cible : {target_ip} ({target_input})\\n")

        log_file.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")

        log_file.write(f"Plage analysée : {start_port} - {end_port}\\n")

        log_file.write(f"Ports ouverts : {open_ports}\\n")

    

    print(f"[+] Résultats enregistrés dans le fichier : {log_filename}")

    print("-" * 50)

if __name__ == "__main__":

    main()
