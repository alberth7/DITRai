from config import app
from controllers.home import home
from controllers.user import users
from controllers.settings import settings
import unittest


#register blueprints
app.register_blueprint(users)
app.register_blueprint(home)
app.register_blueprint(settings)

# uncomment this to run 

# if __name__=="__main__":
#     app.run(debug=True,port=5000)
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)