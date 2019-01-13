from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_details.sqlite3' # uri -> Uniform Resource Identifier
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# Import Blueprints Defined in the routes
from routes.authentication import authentication_blueprint
from routes.boards import boards_blueprint

# Blueprints
app.register_blueprint(authentication_blueprint)
app.register_blueprint(boards_blueprint)


if __name__ == '__main__':
    app_host = os.environ.get('APP_HOST') or '0.0.0.0'
    app_port = os.environ.get('APP_PORT') or 8002
    app.run(host=app_host, port=app_port, debug=False, threaded=True)
