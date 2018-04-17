from flask import Flask
from flask import render_template
from models.player import Player
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:new_password@localhost/roswar?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


base = declarative_base()
engine = create_engine('mysql+pymysql://root:new_password@localhost/roswar?charset=utf8')
base.metadata.bind = engine
db_session = sessionmaker(bind=engine)
session = db_session()
base.metadata.create_all(engine)

@app.route('/')
def index():
    return 'Hello!'

@app.route('/players')
def players_table(name=None):

    data = session.query(Player).all()
    return render_template('players.html', name=name, data=data)


if __name__ == '__main__':
    app.run()