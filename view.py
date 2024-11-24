from flask import request

from flask.views import MethodView

from extension import db
from models import Player, Match, MatchRecord, PlayerRecord



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


class MatchApi(MethodView):
    def get(self, match_id):
        if not match_id:
            matches:[Match] = Match.query.all()
            results = [
                {
                    'id': match.id,
                    'match_mode': match.match_mode,
                    'match_time': match.match_time,
                    'match_result': match.match_result,
                    'match_duration': match.match_duration,
                    'match_map': match.match_map
                }for match in matches
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
        return {
            'status': 'success',
            'message': '数据添加成功'
        }
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
            self.deleteExpire()
        match: Match = Match.query.get(match_id)
        db.session.delete(match)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功'
        }
    def deleteExpire(self):
        from datetime import datetime, timedelta
        # 计算三个月前的日期
        three_months_ago = datetime.now() - timedelta(days=90)

        # 获取所有比赛记录
        matches = Match.query.all()

        # 记录需要删除的比赛
        matches_to_delete = []

        for match in matches:
            date_object = datetime.strptime(match.match_time, "%Y-%m-%d %H:%M:%S")
            match_time = date_object  # 假设 match_time 是一个 datetime 对象
            if match_time < three_months_ago:
                matches_to_delete.append(match)
        if not matches_to_delete:
            return {
                'status': 'success',
                'message': '没有过期比赛'
            }
        # 删除过期比赛
        for match in matches_to_delete:
            db.session.delete(match)

        # 提交更改
        db.session.commit()
        return {
        'status': 'success',
        'message': '数据删除成功'
        }


class MatchRecordApi(MethodView):
    def get(self, match_id):
        if not match_id:
            match: [MatchRecord] = MatchRecord.query.all()
            results = [
                {
                    'id': record.recordId,
                    'matchId': record.matchId,
                    'killerId': record.killerId,
                    'victimId': record.victimId,
                    'killTime': record.killTime,
                    'meansOFDeath': record.meansOFDeath,
                    'coordinates': record.coordinates
                } for record in match
            ]
            return {
                'status': 'success',
                'message': '所有的比赛记录',
                'results': results
            }
        match: [MatchRecord] = MatchRecord.query.filter(match_id=match_id).all()
        results = [
            {
                'matchId': record.matchId,
                'killerId': record.killerId,
                'victimId': record.victimId,
                'killTime': record.killTime,
                'meansOFDeath': record.meansOFDeath,
                'coordinates': record.coordinates
                }for record in match
            ]
        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': results
        }

    def post(self):
        form = request.json
        record = MatchRecord()
        record.recordId = form.get('recordId')
        record.matchId = form.get('match_id')
        record.killerId = form.get('killerId')
        record.victimId = form.get('victimId')
        record.killTime = form.get('killTime')
        record.meansOfDeath = form.get('meansOFDeath')
        record.coordinates = form.get('coordinates')
        db.session.add(record)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据添加成功'
        }

    def delete(self,   match_id):
        if not match_id:
            return {
                'status': 'fail',
                'message': '请指定要删除的比赛ID'
            }
        else: #删除比赛记录
            record: [MatchRecord] = MatchRecord.query.filter_by(match_id = match_id).all()
            db.session.delete(record)
            db.session.commit()
            return {
                'status': 'success',
                'message': '数据删除成功'
            }

class PlayerRecordApi(MethodView):
    def get(self, player_id):
        if not player_id:
            return {
                'status': 'fail',
                'message' : '请指定playerid'
            }
        records = PlayerRecord.query.filter_by(matchId=player_id).all()
        records_data = []
        for record in records:
            records_data.append(
            {
                'pmatchId': record.recordId,
                'playerId': record.playerId,
                'matchId': record.matchId,
                'killCount': record.killCount,
                'deathCount': record.deathCount,
                'kd' : record.kd,
                'rankpoints' : record.rankpoints,
            }
            )
        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': records_data
        }
    def post(self):
        form = request.json
        playerrecord = PlayerRecord()
        playerrecord.pmatchId = form.get('pmatchId')
        playerrecord.playerId = form.get('playerId')
        playerrecord.matchId = form.get('matchId')
        playerrecord.killCount = form.get('killCount')
        playerrecord.deathCount = form.get('deathCount')
        playerrecord.kd = form.get('kd')
        playerrecord.rankpoints = form.get('rankpoints')
        db.session.add(playerrecord)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据添加成功'
        }
    def delete(self, player_id):
        if not player_id:
            return {
                'status': 'fail',
                'message' : '请指定playerid'
            }
        else:
            playerR: [PlayerRecord] = PlayerRecord.query.filter_by(player_id = player_id).all()
            db.session.delete(playerR)
            db.session.commit()
            return {
                'status': 'success',
                'message': '数据删除成功'
            }














