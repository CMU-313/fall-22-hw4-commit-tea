from flask import Flask
from app.handlers.routes import configure_routes
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


app = Flask(__name__)
configure_routes(app)
swagger = Swagger(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)
