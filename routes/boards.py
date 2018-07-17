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
boards_blueprint = Blueprint('boards',__name__,template_folder='templates')
# from utility.sqlalchemy_orm import boards
# from app import db

@boards_blueprint.route('/dashboard',methods=['GET','POST'],endpoint='dashboard')
def dashboard():
    from utility.sqlalchemy_orm import boards
    from app import db
    if request.method == 'GET':
        db.create_all()
        board = boards(session['email'],"sample")
        all_boards = board.get_all_user_boards(session['email'])
        count = 1  # For serial no in HTML Table -> Iterating it by 1
        # html_table : Initializing HTML Table as a Python String
        html_table = """<table class="table">
                                          <thead>
                                            <tr>
                                              <th scope="col">S.no</th> 
                                              <th scope="col">Board Name</th> 
                                              <th scope="col">Updae Name</th>
                                              <th scope="col">Delete Board</th>
                                            </tr>
                                          </thead>
                                          <tbody>"""
        # Setting table data values from query_result list
        for i in range(0, len(all_boards)):
            html_table = html_table + """ <tr> <th scope="row">  """ + str(count) + """</th>"""
            html_table = html_table + """<td><button type="button" class="btn btn-link" value  = " """ +str(all_boards[i]) + """ id=" "> """+str(all_boards[i])+"""</button></td>"""
            html_table = html_table + """<td><button   class="btn btn-info update" value  = " """ + str(all_boards[i]) + """ "> UPDATE """+"""</button></td>"""
            html_table = html_table + """<td><button   class="btn btn-danger delete" value = " """ + str(all_boards[i]) + """ "> DELETE """+"""</button></td>"""


            html_table = html_table + """</tr>"""
            count = count + 1

        html_table = html_table + """  </tbody>
                                </table>"""
        return render_template('dashboard/index.html',html_table = Markup(html_table))
    elif request.method == 'POST':
        board_name = request.form.get('board_name')
        username = session['email']
        print("Board Name:", board_name)
        board = boards(username,board_name)
        code,msg = board.create_new_board(username,board_name)
        if code == 0:
            msg = '<div class="alert alert-danger"><strong>Error</strong> ' + msg + '</div>'
            return redirect('/dashboard')
        elif code == 1:
            msg = '<div class="alert alert-success"><strong>Success</strong> ' + msg + '</div>'
            return redirect('/dashboard')


# Route for deleting the board
@boards_blueprint.route('/delete/<board_name>', methods=['GET','POST'],endpoint='delete_board')
def delete_board(board_name):
    from utility.sqlalchemy_orm import boards
    from app import db
    if request.method == 'GET':
        print("Request Method:",request.method)
        print("Delete Board:",board_name)
        board = boards(session['email'],board_name)
        board.delete_board(session['email'],board_name)
        return redirect('/dashboard')

# Route for updating the board name
@boards_blueprint.route('/update/<board_name>/<new_board_name>', methods=['GET','POST'],endpoint='update_board')
def update_board(board_name,new_board_name):
    from utility.sqlalchemy_orm import boards
    from app import db
    if request.method == 'GET':
        print("Request Method:",request.method)
        board = boards(session['email'],board_name)
        code,msg = board.update_board_name(session['email'],board_name,new_board_name)
        return redirect('/dashboard')


# # Board page
# @boards_blueprint.route('/dashboard/<board_name>', methods=['GET','POST'],endpoint='board_page')
# def board_page(board_name):
#     from utility.sqlalchemy_orm import boards
#     from app import db
#     if request.method == 'GET':




