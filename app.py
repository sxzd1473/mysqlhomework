from flask import Flask
from extension import db, cors
from models import Player, Match
from view import PlayerApi, MatchApi, MatchRecordApi

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

playerRecord_view = PlayerApi.as_view('playerRecord_api')
app.add_url_rule('/playerRecords/', defaults={'playerRecord_id': None},
                 view_func=playerRecord_view, methods=['GET',]
                 )
app.add_url_rule('/playerRecords/<int:playerRecord_id>',  view_func=playerRecord_view, methods=['GET', 'POST', 'DELETE'])
app.add_url_rule('/playerRecords/<int:player_id>',  view_func=playerRecord_view, methods=['GET', 'POST', 'DELETE'])

match_view = MatchApi.as_view('match_api')
app.add_url_rule('/matches/', defaults={'match_id': None},
                 view_func=match_view, methods=['GET',])
app.add_url_rule('/matches/<int:match_id>',  view_func=match_view, methods=['GET', 'PUT', 'DELETE'])

matchRecord_view = MatchRecordApi.as_view('matchRecord_api')
app.add_url_rule('/matchRecords/', defaults={'matchRecord_id': None},
                 view_func=matchRecord_view, methods=['GET',]
                 )
app.add_url_rule('/matchRecords/<int:matchRecord_id>',  view_func=matchRecord_view, methods=['GET', 'POST', 'DELETE'])
app.add_url_rule('/matchRecords/<int:match_id>',  view_func=matchRecord_view, methods=['GET', 'POST', 'DELETE'])

if __name__ == '__main__':
    create()
    app.run(debug=True)
