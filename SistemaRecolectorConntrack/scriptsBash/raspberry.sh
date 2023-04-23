#!/bin/bash
# Intalacion de docker y docker-compose para raspbian

sudo apt-get update && sudo apt-get upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ${USER}

sudo su - ${USER}

sudo apt-get install libffi-dev libssl-dev -y

sudo apt install python3-dev -y

sudo apt-get install -y python3 python3-pip

sudo pip3 install docker-compose

# para la libreria psycopg2
sudo apt-get install libpq-dev



