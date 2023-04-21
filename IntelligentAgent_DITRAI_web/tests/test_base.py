from urllib import response
from flask_testing import TestCase
from flask import current_app, url_for
#Se importa la aplicacion de Flask
from app import app

class MainTest(TestCase):
    # Se implementa el metodo create_app que vive en la clase TestCase y tiene que regresar una aplicacion de Flask
    def create_app(self):
        app.config['TESTING'] = True # Se configura la aplicacion para testing
        app.config['WTF_CSRF_ENABLED'] = False # Se indica que no se va a utilizar el CSRF( Cross-site request forgery o falsificación de petición en sitios cruzados) de las formas porque en este caso no existe una sesion activa del usuario
        return app

    # El primer Test es para probar que la app de Flask existe
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    # El segundo Test es para probar que la app se encuentra en modo Testing
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])
        
    # El tercer Test es para probar que index redirige a hello
    def test_index_get(self):
        response = self.client.get(url_for('home.index'))
        self.assert200(response)
    
    # El cuarto test login
    def test_login_get(self):
        response = self.client.get(url_for('users.login'))
        self.assert200(response)
    
    # El quinto test settings
    def test_settings_get(self):
        response = self.client.get(url_for('home.settings'))
        self.assert200(response)
    
    # El sexto test estadisticas
    def test_estadisticas_get(self):
        response = self.client.get(url_for('home.estadisticas'))
        self.assert200(response)

    # El septimo test reglas iptables
    def test_reglas_iptable_get(self):
        response = self.client.get(url_for('home.reglas_iptable'))
        self.assert200(response)    
    






