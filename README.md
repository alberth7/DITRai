# Install router 
opkg install conntrack
opkg install openssh-sftp-server

#Preparar servivios demonio
En la carpeta /etc/systemd/system crear ditrai.service con el siguiente codigo

'''
[Unit]
Description=Agente inteligente DITRai
After=network.target

[Service]
Type=simple
User=michael
WorkingDirectory=/home/michael/Documents/thesis/DITRai_private/IntelligentAgent_DITRAI
ExecStart=/usr/bin/python3.7 /home/michael/Documents/thesis/DITRai_private/IntelligentAgent_DITRAI/app.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
'''

También crear un archivo ditrai_web.service con el siguiente código:

'''
[Unit]
Description=Gunicorn instance to serve ditrai_web
After=network.target

[Service]
Type=simple
User=michael
WorkingDirectory=/home/michael/Documents/thesis/DITRai_private/IntelligentAgent_DITRAI_web
ExecStart=/usr/bin/gunicorn3 --workers 3 app:app
Restart=always

[Install]
WantedBy=multi-user.target

'''

recargar los servicios

'''
sudo systemctl daemon-reload
'''

Nota. En el parámetro WorkingDirectory  cololar el path donde se encuentra el softare es dicir el repositorio.

Para ditrai.service adicionar que no se ejecute automaticamente cada vez que inicie el sistema operativo ejecutar:
'''
sudo systemctl disable ditrai.service
'''

Para ditrai_web.service debe ejetarse despues que inicie el sistema operativo
'''
sudo systemctl enable  ditrai_web.service
'''

Para ver la ejecición de los servicios:
'''
sudo systemctl status ditrai.service
'''

# Configuración para el servidor web nginx

En la ruta /etc/nginx/sites-avaible/default cambiar por

'''
server {
    listen 80;
    server_name ditrai.com www.ditrai.com;
    #server_name _;
    location / {
        #proxy_pass http://127.0.0.1:5000;
        proxy_pass http://127.0.0.1:8000;
	proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

'''

Recargamos el servicio de nginx:
'''
systemctl reload nginx
'''

# Configuracion del  demonio ditrai
En el archivo /etc/sudoers adicionar al final este comando
'''
michael ALL=NOPASSWD: /bin/systemctl restart ditrai.service
michael ALL=NOPASSWD: /bin/systemctl stop ditrai.service
'''

para que ditrai puede ser ejecutado sin  el password de sudo

