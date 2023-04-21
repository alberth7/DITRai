
class ConnectionRouter(object):
    '''Conexion con el Router'''

    _hostRouter = str
    _userRouter = str
    _pwdRouter = str
    _portRouter = int
    _pathSshRouter = str

    def __init__(self):
        self._hostRouter = ''
        self._userRouter = ''
        self._pwdRouter = ''
        self._portRouter = 22
        self._pathSshRouter = ''

    def __int__(self, hostRouter, userRouter, pwdRouter, portRouter, pathSshRouter):
        self._hostRouter = hostRouter
        self._userRouter = userRouter
        self._pwdRouter = pwdRouter
        self._portRouter = portRouter
        self._pathSshRouter = pathSshRouter

