from flask import Blueprint
from flask import Blueprint,request, jsonify, render_template, session,Markup,redirect,Flask,flash

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import datetime
from sqlalchemy.orm import sessionmaker
from werkzeug.contrib.cache import SimpleCache


# Creating a blueprint class
authentication_blueprint = Blueprint('authentication',__name__,template_folder='templates')
from utility.sqlalchemy_orm import users
from app import db


@authentication_blueprint.route('/',methods=['GET','POST'],endpoint='ui')
def ui():
    if request.method == 'GET':
        return render_template('ui/index.html')


@authentication_blueprint.route('/logout',methods=['GET','POST'],endpoint='authentication_logout')
def authentication_logout():
    session['email'] = ''
    return redirect('/')


@authentication_blueprint.route('/authentication/register',methods=['GET','POST'],endpoint='register')
def register():
    if request.method == 'GET':
        db.create_all()
        return render_template('authentication/register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print("Username:",username)
        print("Password:",password)
        user = users(username,password)
        code,msg = user.register(username,password)
        if code == 0:
            msg = '<div class="alert alert-danger"><strong>Error</strong> ' + msg + '</div>'
            return render_template('authentication/register.html', msg=Markup(msg))
        elif code == 1:
            msg = '<div class="alert alert-success"><strong>Success</strong> ' + msg + '</div>'
            return render_template('authentication/register.html', msg=Markup(msg))

@authentication_blueprint.route('/authentication/login',methods=['GET','POST'],endpoint='login')
def login():
    if request.method == 'GET':
        return render_template('authentication/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users(username, password)
        code, msg = user.login(username, password)
        if code == 0:
            msg = '<div class="alert alert-danger"><strong>Error</strong> ' + msg + '</div>'
            return render_template('authentication/login.html', msg=Markup(msg))
        elif code == 1:
            session['email'] = username
            return redirect('/dashboard')


# @authentication_blueprint.route('/dashboard',methods=['GET','POST'],endpoint='dashboard')
# def dashboard():
#     if request.method == 'GET':
#         return render_template('dashboard/index.html')
#     elif request.method == 'POST':
#         pass
