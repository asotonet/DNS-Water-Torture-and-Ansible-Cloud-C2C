import subprocess
import csv
import os
 
def add_host_to_known_hosts(ip_address):
    # Obtener el fingerprint del host
    ssh_keyscan_process = subprocess.Popen(["ssh-keyscan", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = ssh_keyscan_process.communicate()

    if ssh_keyscan_process.returncode == 0:
        # Ruta del archivo known_hosts
        known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")
        
        # Agregar el fingerprint al archivo known_hosts
        with open(known_hosts_path, "a") as known_hosts_file:
            known_hosts_file.write(stdout.decode())
        print(f"Host {ip_address} agregado a {known_hosts_path}.")
    else:
        print(f"Error al obtener el fingerprint del host {ip_address}. Mensaje de error: {stderr.decode()}")

def read_ips_from_csv(csv_file_path):
    ips = []
    with open(csv_file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ips.append(row["IP Address"])
    return ips

if __name__ == "__main__":
    csv_file_path = "ips_droplets.csv"  # Archivo CSV
    ip_addresses = read_ips_from_csv(csv_file_path)

    for ip_address in ip_addresses:
        add_host_to_known_hosts(ip_address)
