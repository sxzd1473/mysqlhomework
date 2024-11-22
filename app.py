from flask import Flask,render_template,jsonify,request,redirect,url_for
import requests
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
    return render_template("main_page.html")
#player
player_view = PlayerApi.as_view('player_api')
app.add_url_rule('/players/', defaults={'player_id': None},
                 view_func=player_view, methods=['GET', ])
app.add_url_rule('/players/add/', view_func=player_view, methods=['POST', ],)
app.add_url_rule('/players/edit/<int:player_id>/', view_func=player_view, methods=['PUT', ],)
app.add_url_rule('/players/delete/<int:player_id>/', view_func=player_view, methods=[ 'DELETE',])

#playerRecord
playerRecord_view = PlayerApi.as_view('playerRecord_api')
app.add_url_rule('/playerRecords/', defaults={'playerRecord_id': None},
                 view_func=playerRecord_view, methods=['GET', ]
                 )
app.add_url_rule('/playerRecords/<int:player_id>', view_func=playerRecord_view, methods=['GET', 'POST', 'DELETE'])

#match
match_view = MatchApi.as_view('match_api')
app.add_url_rule('/matches/', defaults={'match_id': None},
                 view_func=match_view, methods=['GET', ])
app.add_url_rule('/matches/<int:match_id>', view_func=match_view, methods=['GET', 'POST', 'DELETE'])

#matchRecord
matchRecord_view = MatchRecordApi.as_view('matchRecord_api')
app.add_url_rule('/matchRecords/', defaults={'matchRecord_id': None},
                 view_func=matchRecord_view, methods=['GET', ]
                 )
app.add_url_rule('/matchRecords/<int:match_id>', view_func=matchRecord_view, methods=['GET', 'POST', 'DELETE'])


#路由


@app.route('/Players_view')
def players_view():
    # 发送 HTTP GET 请求到外部 API
    response = requests.get('http://localhost:5000/players/')

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应数据为 Python 对象（假设返回的是 JSON 格式）
        data = response.json()['results']
        print(data)

        # 将数据传递给模板
        return render_template('Player.html', data=data)
    else:
        # 处理错误情况
        return jsonify({'error': 'Failed to fetch data from API'}), response.status_code
    return render_template('Player.html',data = data)

@app.route('/Matches_view')
def matches_view():
    # 发送 HTTP GET 请求到外部 API
    response = requests.get('http://localhost:5000/matches/')

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应数据为 Python 对象（假设返回的是 JSON 格式）
        data = response.json()['results']
        print(data)

        # 将数据传递给模板
        return render_template('Match.html', data=data)
    else:
        # 处理错误情况
        return jsonify({'error': 'Failed to fetch data from API'}), response.status_code
    return render_template('Match.html',data = data)

@app.route('/MatchRecords_view')
def matchRecords_view():
    # 发送 HTTP GET 请求到外部 API
    response = requests.get('http://localhost:5000/matchRecords/')

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应数据为 Python 对象（假设返回的是 JSON 格式）
        data = response.json()['results']
        print(data)

        # 将数据传递给模板
        return render_template('MatchRecord.html', data=data)
    else:
        # 处理错误情况
        return jsonify({'error': 'Failed to fetch data from API'}), response.status_code
    return render_template('MatchRecord.html',data = data)

@app.route('/PlayerRecords_view')
def playerRecords_view():
    # 发送 HTTP GET 请求到外部 API
    response = requests.get('http://localhost:5000/playerRecords/')

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应数据为 Python 对象（假设返回的是 JSON 格式）
        data = response.json()['results']
        print(data)

        # 将数据传递给模板
        return render_template('PlayerRecord.html', data=data)
    else:
        # 处理错误情况
        return jsonify({'error': 'Failed to fetch data from API'}), response.status_code
    return render_template('PlayerRecord.html',data = data)


def create():
    db.drop_all()
    db.create_all()
    Player.init_db()
    Match.init_db()
    print('Database created successfully')

if __name__ == '__main__':
    create()
    app.run(debug=True)
