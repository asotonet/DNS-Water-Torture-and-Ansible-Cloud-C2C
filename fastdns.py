import csv
import concurrent.futures
import socket

def read_subdomains_from_csv(csv_file):
    subdomains = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # omitir la fila de encabezado
        for row in reader:
            subdomains.append(row[0])
    return subdomains

def create_dns_socket(resolver_address):
    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return sock

def query_dns(sock, domain, subdomains, resolver_address):
    try:
        # Formar y enviar las consultas DNS
        for subdomain in subdomains:
            full_domain = f"{subdomain}.{domain}"
            query = bytearray()
            
            # Encabezado DNS
            query.extend([0, 1])  # Identificación
            query.extend([0, 1])  # Flags
            query.extend([0, 1])  # Número de preguntas
            query.extend([0, 1])  # Número de respuestas
            query.extend([0, 0])  # Número de registros de autoridad
            query.extend([0, 0])  # Número de registros adicionales

            # Nombre de dominio
            for label in full_domain.split('.'):
                query.append(len(label))
                query.extend(map(ord, label))

            query.append(0)  # Terminador de cadena

            # Tipo de registro A (IPv4)
            query.extend([0, 1])

            # Clase IN (Internet)
            query.extend([0, 1])

            # Enviar la consulta
            sock.sendto(query, (resolver_address, 53))

    except Exception as e:
        print(f"Error: {e}")

def send_dns_queries(subdomains, domain, resolver_address, block_size=1000):
    # Crear el socket una vez para reutilizarlo en todas las consultas
    sock = create_dns_socket(resolver_address)

    chunks = [subdomains[i:i + block_size] for i in range(0, len(subdomains), block_size)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(chunks)) as executor:
        futures = [executor.submit(query_dns, sock, domain, chunk, resolver_address) for chunk in chunks]

        # Esperar a que todas las consultas se completen
        concurrent.futures.wait(futures)

    # No cerrar el socket aquí, ya que se seguirá utilizando en otras partes del código

if __name__ == "__main__":
    domain_to_query = ""  # Dominio a consultar
    input_csv_file = "subdomains.csv"  # Nombre del archivo CSV
    resolver_ip = "8.8.8.8"  # Dirección IP del servidor DNS target

    subdomains_to_query = read_subdomains_from_csv(input_csv_file)

    send_dns_queries(subdomains_to_query, domain_to_query, resolver_address=resolver_ip)

    print(f"Se enviaron {len(subdomains_to_query)} consultas.")