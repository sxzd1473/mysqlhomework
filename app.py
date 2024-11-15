from flask import Flask
from extension import db, cors
from models import Player, Match
from view import PlayerApi, MatchApi

#运行前调用cli命令create创建数据库！！！

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
cors.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def create():
    db.drop_all()
    db.create_all()
    Player.init_db()
    Match.init_db()
    print('Database created successfully')


player_view = PlayerApi.as_view('player_api')
app.add_url_rule('/players/', defaults={'player_id': None},
                 view_func=player_view, methods=['GET',])
app.add_url_rule('/players/<int:player_id>',  view_func=player_view, methods=['GET', 'PUT', 'DELETE'])

match_view = MatchApi.as_view('match_api')
app.add_url_rule('/matches/', defaults={'match_id': None},
                 view_func=match_view, methods=['GET',])
app.add_url_rule('/matches/<int:match_id>',  view_func=match_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    create()
    app.run(debug=True)
