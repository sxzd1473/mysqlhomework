from urllib import request

from flask import Flask
from flask.views import MethodView
from extension import db, cors
from models import Player, Match

#运行前调用cli命令create创建数据库！！！

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
    Match.init_db()
    print('Database created successfully')

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
        return {
        'status': 'success',
        'message': '数据添加成功'
        }


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

    def delete(self, player_id):
        if not player_id:
            return {
                'status': 'fail',
                'message': '请指定要删除的玩家ID'
            }
        player:Player = Player.query.get(player_id)
        db.session.delete(player)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功'
        }

player_view = PlayerApi.as_view('player_api')
app.add_url_rule('/players/', defaults={'player_id': None},
                 view_func=player_view, methods=['GET',])
app.add_url_rule('/players/<int:player_id>',  view_func=player_view, methods=['GET', 'PUT', 'DELETE'])

class MatchApi(MethodView):
    def get(self, match_id):
        if not match_id:
            match:[Match] = Match.query.all()
            results = [
                {
                    'id': match.id,
                    'match_mode': match.match_mode,
                    'match_time': match.match_time,
                    'match_result': match.match_result,
                    'match_duration': match.match_duration,
                    'match_map': match.match_map
                }for match in match
            ]
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
        match: Match = Match.query.get(match_id)
        return {
            'status': 'success',
            'message': '数据查询成功',
            'result':
                {
                    'id': match.id,
                   'match_mode': match.match_mode,
                   'match_time': match.match_time,
                   'match_result': match.match_result,
                   'match_duration': match.match_duration,
                   'match_map': match.match_map
                }
        }
    def post(self):
        form = request.json
        match = Match()
        match.match_mode = form.get('match_mode')
        match.match_time = form.get('match_time')
        match.match_result = form.get('match_result')
        match.match_duration = form.get('match_duration')
        match.match_map = form.get('match_map')
        db.session.add(match)
        db.session.commit()
    def put(self, match_id):
        match: Match = Match.query.get(match_id)
        match.match_mode = request.json.get('match_mode')
        match.match_time = request.json.get('match_time')
        match.match_result = request.json.get('match_result')
        match.match_duration = request.json.get('match_duration')
        match.match_map = request.json.get('match_map')
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功'
        }
    def delete(self, match_id):
        if not match_id:
            return {
                'status': 'fail',
                'message': '请指定要删除的比赛ID'
                }
        match: Match = Match.query.get(match_id)
        db.session.delete(match)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功'
        }

match_view = MatchApi.as_view('match_api')
app.add_url_rule('/matches/', defaults={'match_id': None},
                 view_func=match_view, methods=['GET',])
app.add_url_rule('/matches/<int:match_id>',  view_func=match_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    create()
    app.run(debug=True)
