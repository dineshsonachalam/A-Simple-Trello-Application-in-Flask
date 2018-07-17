from app import db
from werkzeug.security import generate_password_hash,check_password_hash
class users(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


    def __init__(self, username,password):
        self.username = username
        self.password = password

    def register(self, username, password):

        if db.session.query(users).filter(users.username == str(username)).count() > 0:

            return 0, 'An account already exists for this username'
        else:
            # Create objects
            user = users(str(username), generate_password_hash(password))
            db.session.add(user)
            # commit the record the database
            db.session.commit()
            return 1, 'User created successfully.'

    def login(self, username, password):

        user_in_db = db.session.query(users).filter(users.username == str(username))
        if user_in_db.count() > 0:
            user_in_db_password = user_in_db[0].password
            # If password match
            if check_password_hash(user_in_db_password, password):
                return 1, 'Logged in successfully'
            else:
                return 0, 'Incorrect password'
        else:
            return 0, 'Username not found'

class boards(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    board_name = db.Column(db.String(100))


    def __init__(self, username,board_name):
        self.username = username
        self.board_name = board_name

    def create_new_board(self, username,board_name):

        if db.session.query(boards).filter(boards.username == str(username),boards.board_name == board_name).count() > 0:

            return 0, 'A board already exists for this name'
        else:
            # Create objects
            board = boards(str(username), str(board_name))
            db.session.add(board)
            # commit the record the database
            db.session.commit()
            return 1, 'Board Created Successfully'


    def get_all_user_boards(self,username):
        total_boards =[]
        for board in db.session.query(boards).filter(boards.username == str(username)):
            total_boards.append(board.board_name)
        return total_boards

    def delete_board(self,username,board_name):
        board_delted = db.session.query(boards).filter(boards.username == str(username),boards.board_name == board_name).delete()
        db.session.commit() # save session
        print("Board Delted:",board_delted)

    def update_board_name(self,username,board_name,new_board_name):
        check_duplicate_board =db.session.query(boards).filter(boards.username == str(username),boards.board_name == new_board_name)

        if check_duplicate_board.count() > 0:
            return 0, 'A board already exists for this name'
        else:
            row = db.session.query(boards).filter(boards.username == str(username),boards.board_name == board_name).first()
            print("Row:",row.board_name)
            row.board_name = new_board_name
            # commit the record the database
            db.session.commit()
            return  1,'Updated Successfully'

