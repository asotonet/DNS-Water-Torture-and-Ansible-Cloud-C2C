
## 🚀 Acerca de mi
Estoy en la busqueda de ser un experto en telemática, seguridad y automatización.
Considero importante realizar contribuciones para la comunidad que sean de valor.


# Python DNS Water Trottle and Ansible Cloud Instances C2C

Este codigo está completamente hecho en Python, su uso es esclusivamente con fines educativos y demostrativos, para comprender como los atacantes realizan ataques ejecutan ataques DDoS a los servicios DNS.


- El codigo se compone de varios ejecutables, primeramente el generador de los subdominios aleatorios en un archivo csv.

- Un generador de IPs origen aleatorias para insertar en los headers de los DNS requests.

- Un codigo para creación de instancias cloud en Digital Ocean por medio de API SSL

- Templates de Ansible para hacer C2C a las instancias, instalar dependencias y lanzar las ejecuciones de codigo python para DNS requests.
## Como ejecutar este proyecto

Clona el proyecto

```bash
  git clone https://github.com/asotonet/DNS-Water-Trottle-and-Ansible-Cloud-C2C.git
```

Ve al directorio

```bash
  cd DNS-Water-Trottle-and-Ansible-Cloud-C2C
```
Install dependencies

```bash
  sudo apt update
  sudo apt install python3
  sudo apt-add-repository ppa:ansible/ansible
  sudo apt install ansible

```
Crea las instancias y ejecuta los task de Ansible C2C

```bash
  python3 cdroplet.py && python3 ansible-inventory.py && python3 add-fingerprint.py

```

Destruye las instancias droplet creadas en Digital Ocean

```bash
  python3 destroy.py
```


![Logo](https://www.p2linc.com/wp-content/uploads/2021/09/Screen-Shot-2021-09-17-at-1.56.20-PM.png)


## Mis contactos

- [@Github](https://www.github.com/asotonet)
- [@Linkedin](https://www.linkedin.com/in/asoton/)