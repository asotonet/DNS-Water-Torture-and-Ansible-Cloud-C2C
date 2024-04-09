import requests
import csv

# Configura tus credenciales de Digital Ocean
API_TOKEN = "dop_v1_d1b6ec274a64cb9951b57a96511d18df690cea070022edf3a6fa7939f6ad006f"

def destroy_droplet(droplet_name):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    url = f"https://api.digitalocean.com/v2/droplets?name={droplet_name}"

    response = requests.get(url, headers=headers)
    droplet_data = response.json()["droplets"]

    if droplet_data:
        droplet_id = droplet_data[0]["id"]
        delete_url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}"
        delete_response = requests.delete(delete_url, headers=headers)

        if delete_response.status_code == 204:
            print(f"Droplet {droplet_id} ({droplet_name}) destruido con éxito.")
        else:
            print(f"Fallo al destruir el droplet {droplet_id} ({droplet_name}). Código de estado: {delete_response.status_code}")
    else:
        print(f"No se encontró el droplet con nombre {droplet_name}.")

def read_csv(file_path):
    droplets_info = []

    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Salta la primera fila que contiene encabezados
        for row in reader:
            region, droplet_name, droplet_ip = row
            droplets_info.append({
                "region": region,
                "name": droplet_name,
                "ip": droplet_ip
            })

    return droplets_info

def main():
    csv_file_path = "ips_droplets.csv"  # Reemplaza con la ruta de tu archivo CSV
    droplets_info = read_csv(csv_file_path)

    for droplet in droplets_info:
        destroy_droplet(droplet["name"])

if __name__ == "__main__":
    main()