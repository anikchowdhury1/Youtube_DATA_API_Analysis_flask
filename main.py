from flask import Flask
from blueprints.endpoints import blueprint as endpoint

app = Flask(__name__)

app.config['RESTPLUS_MASK_SWAGGER'] = False


app.register_blueprint(endpoint)

if __name__ == "__main__":
    app.run()
