
class ConnectionRouter(object):
    '''Conexion con el Router'''

    _hostRouter = str
    _userRouter = str
    _pwdRouter = str
    _portRouter = int
    _pathSshRouter = str

    def __init__(self):
        self._hostRouter = '10.0.1.1'
        self._userRouter = 'root'
        self._pwdRouter = 'password'
        self._portRouter = 22
        self._pathSshRouter = '/home/michael/.ssh/openWRT_A7'
        #self._pathSshRouter = 'E:/thesis_2022/ssh/openWRT_C7'
        #self._pathSshRouter = '/home/pi/.ssh/openWRT_C7'

    def __int__(self, hostRouter, userRouter, pwdRouter, portRouter, pathSshRouter):
        self._hostRouter = hostRouter
        self._userRouter = userRouter
        self._pwdRouter = pwdRouter
        self._portRouter = portRouter
        self._pathSshRouter = pathSshRouter

