import paramiko
from Data.PathFiles import PathFiles
from Data.ConnectionRouter import ConnectionRouter

class C_Enviar_regla_iptable(ConnectionRouter):
    def __init__(self):
        super(C_Enviar_regla_iptable, self).__init__()

    def procesadorGenerarReglas(self, results_list):
        print("Rol 3: Procesador generar ip sospechosas (firewall.user).............")
        path = PathFiles()
        firewallUser = path.firewallUser

        index = '''
# This file is interpreted as shell script.
# Put your custom iptables rules here, they will
# be executed with each firewall (re-)start.

# Internal uci firewall chains are flushed and recreated on reload, so
# put custom rules into the root chains e.g. INPUT or FORWARD or into the
# special user chains, e.g. input_wan_rule or postrouting_lan_rule. 

# port redirect port coming in on wan to lan 
'''
        with open(firewallUser, "w") as archivo:
            archivo.write(index)
            for ip in results_list:
                ip = str(ip[0]).replace('[', '').replace(']', '')
                reglaTCP = "iptables -I FORWARD  -p tcp -s " + str(ip) + " --dport 0:65535  -j DROP\n"
                reglaUDP = "iptables -I FORWARD  -p udp -s " + str(ip) + " --dport 0:65535  -j DROP\n"
                regla =  reglaTCP + reglaUDP
                archivo.write(regla)

        print("Rol 3: Procesador generar ip sospechosas (firewall.user).............OK")

    def EnviarReglas(self):
        print("Accion 3: Enviar reglas al router.............")
        path = PathFiles()
        self._hostRouter

        # Variables de conexión
        host = self._hostRouter
        port = self._portRouter
        username = self._userRouter
        private_key_path = self._pathSshRouter
        password = self._pwdRouter

        remote_path = "/etc/firewall.user"
        local_path = path.firewallUser

        try:
            # Crear una instancia de SSHClient
            ssh = paramiko.SSHClient()

            # Configurar la política de host key
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Cargar la clave privada
            key = paramiko.RSAKey.from_private_key_file(private_key_path, password)

            # Conectarse al servidor remoto
            ssh.connect(hostname=host, port=port, username=username, pkey=key)

            # Crear un SFTP client
            sftp = ssh.open_sftp()

            # Cargar el archivo local en el servidor remoto
            sftp.put(local_path, remote_path)

            # Cerrar la conexión SFTP
            sftp.close()

            # Ejecutar el comando para reiniciar el firewall
            command = "/etc/init.d/firewall restart"
            stdin, stdout, stderr = ssh.exec_command(command)

            # Imprimir la salida del comando
            print(stdout.read().decode())

            # Cerrar la conexión SSH
            ssh.close()
            print("Accion 3: Enviar reglas al router.............OK")
        except Exception as e:
            print(f"Error: Accion 3: Enviar reglas al router. {e}")

        finally:
            # Cerrar la conexión SSH
            ssh.close()
