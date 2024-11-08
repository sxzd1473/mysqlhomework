from urllib import request

from flask import Flask
from flask.views import MethodView
from extension import db, cors
from models import Player


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
cors.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    Player.init_db()

class PlayerApi(MethodView):
    def get(self, player_id):
        if not player_id:
            players:[Player] = Player.query.all()
            results = [
                {
                    'id': player.id,
                    'player_name': player.player_name,
                    'player_rank': player.player_rank,
                    'player_kda': player.player_kda,
                }for player in players
            ]
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
        player: Player = Player.query.get(player_id)
        return {
            'status': 'success',
            'message': '数据查询成功',
            'result':
                {
                    'id': player.id,
                    'player_name': player.player_id,
                    'player_rank': player.player_rank,
                    'player_kda': player.player_kda,

                }
        }

    def post(self):
        form = request.json
        player = Player()
        player.player_name = form.get('player_name')
        player.player_rank = form.get('player_rank')
        player.player_kda = form.get('player_kda')
        db.session.add(player)
        db.session.commit()


    def put(self, player_id):
        player: Player = Player.query.get(player_id)
        player.player_name = request.json.get('player_name')
        player.player_rank = request.json.get('player_rank')
        player.player_kda = request.json.get('player_kda')
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功'
        }

player_view = PlayerApi.as_view('player_api')
app.add_url_rule('/players/', defaults={'player_id': None},
                 view_func=player_view, methods=['GET',])
app.add_url_rule('/players/<int:player_id>',  view_func=player_view, methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/players/<string:player_name>',  view_func=player_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    create()
    app.run(debug=True)
