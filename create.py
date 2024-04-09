import csv
import random
import string

def generate_random_subdomain(length=20):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_subdomains(domain, count):
    subdomains = [generate_random_subdomain() + '.' + domain for _ in range(count)]
    return subdomains

def export_to_csv(subdomains, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Subdomain'])
        csv_writer.writerows(map(lambda s: [s], subdomains))

if __name__ == "__main__":
    domain_to_generate = "aec.lab"  # Cambia esto por el dominio que deseas utilizar
    subdomains_count = 1000000
    output_csv_file = "subdomains.csv"  # Nombre del archivo CSV de salida

    subdomains = generate_subdomains(domain_to_generate, subdomains_count)

    export_to_csv(subdomains, output_csv_file)

    print(f"Se generaron {subdomains_count} subdominios y se exportaron a {output_csv_file}.")


