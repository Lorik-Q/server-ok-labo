import platform
import subprocess

keuze_modi = int(input("In welke modus wil je werken: (1) management modus, (2) check modus "))

servers = []

def ping_serv(server):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", server]
    success = subprocess.call(command, stdout=subprocess.PIPE) == 0
    if success:
        status = "Bereikbaar"
    else:
        status = "Onbereikbaar"
    return status

def voeg_serv_toe(server):
    servers.append(server)
    print(f"Server {server} is toegevoegd aan de lijst")

while keuze_modi not in (1, 2):
    keuze_modi = int(input("Ongeldige keuze. Probeer opnieuw: (1) management modus, (2) check modus "))

if keuze_modi == 1:
    print("Management modus geactiveerd")
    keuze = int(input("Kies uit het menu: (1) Server toevoegen, (2) Server verwijderen, (3) Servers in lijst tonen "))
    
    if keuze == 1:
        naam_toe = input("Geef naam van de server die je wil toevoegen: ")
        voeg_serv_toe(naam_toe)
    elif keuze == 2:
        naam_ver = input("Geef naam van de server die je wil verwijderen: ")
    elif keuze == 3:
        print("Servers in lijst tonen")
    else:
        print("Verkeerde keuze.")

elif keuze_modi == 2:
    print("Check modus geactiveerd")
    keuze_ping = input("Welke server wil je pingen? ")
    ping_result = ping_serv(keuze_ping)
    print(f"{keuze_ping} is {ping_result}")
