import requests
import csv
#import getpass
import time
import uuid  # Agregamos la importación de uuid
from concurrent.futures import ThreadPoolExecutor

# Configura tus credenciales de Digital Ocean
API_TOKEN = "dop_v1_d1b6ec274a64cb9951b57a96511d18df690cea070022edf3a6fa7939f6"
CSV_FILE_PATH = "ips_droplets.csv"
SSH_KEY_ID = 40837199
# Configura otros parámetros
DROPLET_COUNT = 2
DROPLET_SIZE = "s-2vcpu-4gb-120gb-intel"
REGIONS = ["nyc3"]  # Puedes agregar más regiones según tus preferencias
#REGIONS = ["nyc3", "sfo2", "lon1"]  # Puedes agregar más regiones según tus preferencias

def create_droplet(region):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    # Utilizamos UUID para generar nombres de droplets aleatorios
    droplet_name = f"ddos-droplet-{region}-{str(uuid.uuid4())[:8]}"

    data = {
        "name": droplet_name,
        "region": region,
        "size": DROPLET_SIZE,
        "image": "ubuntu-20-04-x64",
        "ssh_keys": [SSH_KEY_ID],
        "backups": False,
        "ipv6": True,
        "private_networking": None,
        "user_data": None,
        "private_networking": None,
        "volumes": None,
        "tags": ["DDOS"],
    }

    response = requests.post(
        "https://api.digitalocean.com/v2/droplets", headers=headers, json=data
    )
    droplet_id = response.json()["droplet"]["id"]
    print(f"creando {droplet_name}")
    return droplet_id, droplet_name  # Devolvemos también el nombre del droplet
    
def get_droplet_ip(droplet_id):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}"

    while True:
        response = requests.get(url, headers=headers)
        droplet_data = response.json().get("droplet")

        if droplet_data and droplet_data.get("networks") and droplet_data["networks"].get("v4"):
            droplet_ip = droplet_data["networks"]["v4"][0].get("ip_address")
            if droplet_ip:
                return droplet_ip

	
        time.sleep(10)  # Espera 10 segundos antes de volver a intentar

def write_to_csv(data):
    with open(CSV_FILE_PATH, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Region", "Droplet Name", "IP Address"])
        writer.writerows(data)

def main():
    droplets_info = []

    with ThreadPoolExecutor(max_workers=DROPLET_COUNT * len(REGIONS)) as executor:
        droplet_ids_and_names = list(executor.map(create_droplet, REGIONS * DROPLET_COUNT))

    for (droplet_id, droplet_name), region in zip(droplet_ids_and_names, REGIONS * DROPLET_COUNT):
        droplet_ip = get_droplet_ip(droplet_id)
        droplets_info.append([region, droplet_name, droplet_ip])

    print("Droplets creados:")
    for info in droplets_info:
        print(f"Region: {info[0]}, Droplet Name: {info[1]}, IP Address: {info[2]}")

    write_to_csv(droplets_info)
    print(f"Datos de droplets escritos en {CSV_FILE_PATH}")

if __name__ == "__main__":
    main()
