from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Import Blueprints Defined in the routes
from routes.authentication import authentication_blueprint
from routes.boards import boards_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_details.sqlite3' # uri -> Uniform Resource Identifier
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# Blueprints
app.register_blueprint(authentication_blueprint)
app.register_blueprint(boards_blueprint)


if __name__ == '__main__':
    app_host = os.environ.get('APP_HOST') or 'localhost'
    app_port = os.environ.get('APP_PORT') or 8026
    app.run(host=app_host, port=app_port, debug=True, threaded=True)
    app.run(debug=True)