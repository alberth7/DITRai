import paramiko

from Data.ConnectionRouter import ConnectionRouter

class A_PeticionTablaConexcionesAlRouter(ConnectionRouter):

    def __init__(self):
        super(A_PeticionTablaConexcionesAlRouter, self).__init__()

    def ObtenerTablaEstadoConexionToRouter(self):
        print("Percepcion 1: Peticion tabla de conexciones al router ........")
        '''
        1. Se guardan los datos de conntrack en un archivo xml
        2. Los siguientes datos del router lo guardara en un archivo txt
            root@OpenWrt:~# cat /tmp/dhcp.leases
            1635480422 a8:9c:ed:a4:86:s6 10.0.1.157 MI9-MI9 01:a8:9c:ed:a4:86:46
            1635474839 b6:12:96:f6:62:a3 10.0.1.208 Galaxy-A71-de-Wara 01:b6:12:96:f6:6d:33
        '''

        comando1 = 'conntrack -L -o xml'
        comando2 = 'cat /tmp/dhcp.leases'
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # paramiko.rsakey()
            # client.connect(HOST,port=PORT, username=USER, password=PASSWORD)
            client.connect(hostname=self._hostRouter, port=self._portRouter, username=self._userRouter,
                           key_filename=self._pathSshRouter, password=self._pwdRouter)
            #1
            stdin, stdout, stderr = client.exec_command(comando1)
            result = stdout.read().decode()
            if len(result)==0:
                print("Archivo conntrack vacio.....")
            f = open("BusinessLogic/Files/conntrack.xml", "w")
            f.write(result + "\n")
            f.close()

            #2
            stdin, stdout, stderr = client.exec_command(comando2)
            result = stdout.read().decode()
            f = open("BusinessLogic/Files/dhcp.txt", "w")
            f.write(result + "\n")
            f.close()

            client.close()
            print("Percepcion 1: Peticion tabla de coneciones al router ........Ok")
        except paramiko.ssh_exception.AuthenticationException as e:
            print("Error >>> En la percepción 1: petición estado de conexiones al router")

