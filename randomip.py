import csv
import random

def generate_random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def create_ip_csv(output_csv_file, num_ips):
    with open(output_csv_file, 'w', newline='') as csvfile:
        fieldnames = ['source_ip']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(num_ips):
            writer.writerow({'source_ip': generate_random_ip()})

if __name__ == "__main__":
    output_csv_file = "source_ips.csv"  # Nombre del archivo CSV de salida
    num_ips_to_generate = 500  # Número de direcciones IP a generar

    create_ip_csv(output_csv_file, num_ips_to_generate)

    print(f"Se generaron {num_ips_to_generate} direcciones IP y se guardaron en {output_csv_file}.")

