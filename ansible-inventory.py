import csv

csv_file_path = "ips_droplets.csv"
inventory_file_path = "inventory.ini"

# Lee el archivo CSV y extrae las direcciones IP
with open(csv_file_path, mode="r") as file:
    reader = csv.DictReader(file)
    ip_addresses = [row["IP Address"] for row in reader]

# Crea el archivo de inventario de Ansible
with open(inventory_file_path, mode="w") as inventory_file:
    inventory_file.write("[droplets]\n")
    for ip in ip_addresses:
        inventory_file.write(f"{ip} ansible_ssh_user=root ansible_ssh_private_key_file=pkey.pem\n")
