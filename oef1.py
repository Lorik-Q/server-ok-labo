import platform
import subprocess
import json
import os
import socket
import sys

SERVERS_BESTAND = "servers.json"
PING_LOG_BESTAND = "ping-log.json"

servers = []

if len(sys.argv) != 2:
    print("Gebruik: python oef1.py <modus>")
    print("Modus: 1 (management modus) of 2 (check modus)")
    sys.exit(1)

keuze_modi = int(sys.argv[1])

def laad_servers():
    if os.path.exists(SERVERS_BESTAND):
        try:
            with open(SERVERS_BESTAND, "r") as f:
                return json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"Fout bij het laden van {SERVERS_BESTAND}. Het bestand is mogelijk leeg of ongeldig.")
            return []
    else:
        return []

def verwijder_server(server_naam):
    global servers
    for server in servers:
        if server['naam'] == server_naam:
            servers.remove(server)
            sla_server_op(servers)
            print(f"Server {server_naam} is verwijderd uit de lijst.")
            return
    print(f"Server {server_naam} niet gevonden in de lijst.")

def sla_server_op(servers):
    with open(SERVERS_BESTAND, "w") as f:
        json.dump(servers, f, indent=3)

def ping_serv(server):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", server]
    success = subprocess.call(command, stdout=subprocess.PIPE) == 0
    if success:
        status = "Bereikbaar"
    else:
        status = "Onbereikbaar"

    # Log de ping-status naar ping-log.json
    log_entry = {"server": server, "status": status}
    ping_log = []

    # Lees bestaande logbestand als het bestaat
    if os.path.exists(PING_LOG_BESTAND):
        with open(PING_LOG_BESTAND, "r") as log_file:
            ping_log = json.load(log_file)

    ping_log.append(log_entry)

    # Schrijf de bijgewerkte ping-log naar het bestand
    with open(PING_LOG_BESTAND, "w") as log_file:
        json.dump(ping_log, log_file, indent=2)
    return status

def voeg_serv_toe(server_naam):
    try:
        ip_adres = socket.gethostbyname(server_naam)
        servers.append({"naam": server_naam, "ip_adres": ip_adres})
        sla_server_op(servers)
        print(f"Server {server_naam} met IP-adres {ip_adres} is toegevoegd aan de lijst")
    except socket.gaierror:
        print(f"Kan geen IP-adres vinden voor server {server_naam}")

while keuze_modi not in (1, 2):
    keuze_modi = int(input("Ongeldige keuze. Probeer opnieuw: (1) management modus, (2) check modus "))

servers = laad_servers()

if keuze_modi == 1:
    print("Management modus geactiveerd")
    keuze = int(input("Kies uit het menu: (1) Server toevoegen, (2) Server verwijderen, (3) Servers in lijst tonen "))

    if keuze == 1:
        naam_toe = input("Geef naam van de server die je wil toevoegen: ")
        voeg_serv_toe(naam_toe)
    elif keuze == 2:
        naam_ver = input("Geef naam van de server die je wil verwijderen: ")
        verwijder_server(naam_ver)
    elif keuze == 3:
        print("Servers in lijst tonen:")
        for server in servers:
            print(server['naam'])
    else:
        print("Verkeerde keuze.")

elif keuze_modi == 2:
    print("Check modus geactiveerd")
    keuze_ping = input("Welke server wil je pingen? ")
    ping_result = ping_serv(keuze_ping)
    print(f"{keuze_ping} is {ping_result}")