from flask import Flask, g
from flask import render_template
from models.player import Player
from models.item import Item
from models.clan import Clan
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import jsonify
from flask import request


app = Flask(__name__)

app.config['DEBUG'] = True
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

    # data = session.query(Player).all()
    data = []
    return render_template('players.html', name=name, data=data)


@app.route('/players_json')
def make_players_json():
    page_size = int(request.args.get('length'))
    page_number = int(request.args.get('start'))

    order_array = {}
    for x in range(12):
        order_column_number = 'order[{}][column]'.format(x)
        order_column = request.args.get(order_column_number)
        print('------>>>',order_column)

        order_direction_number = 'order[{}][dir]'.format(x)
        order_direction = request.args.get(order_direction_number)

        if order_column is not None:
            order_name = request.args.get('columns[{}][data]'.format(order_column))
            print('--------->>>>', order_name)
            order_array[order_name] = order_direction
            # order_columns.append(order_column)
            # order_directions.append(order_direction)
    print('-------->>>>>', order_array)

    data = session.query(Player)

    for item in order_array:
        print ('------->>>>', order_array[item])
        if order_array[item] == 'desc':
            data = data.order_by(desc(item))
        else:
            data = data.order_by(asc(item))

    data = data.limit(page_size).offset(page_number).all()

    return jsonify([x.to_dict() for x in data])


if __name__ == '__main__':
    app.run()
