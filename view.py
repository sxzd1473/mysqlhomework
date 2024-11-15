from urllib import request

from flask.views import MethodView
from sqlalchemy.dialects.mysql import match

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
        return {
            'status': 'success',
            'message': '数据添加成功'
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
class MatchRecordApi(MethodView):
    def get(self, match_id):
        if not match_id:
            match: [MatchRecord] = MatchRecord.query.all()
            results = [
                {
                    'id': record.id,
                    'killerId': record.killerid,
                    'victimId': record.victimid,
                    'killTime': record.killtime,
                    'meansOFDeath': record.meansofdeath,
                    'coordinates': record.cordinates
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
                'killerId': record.killerid,
                'victimId': record.victimid,
                'killTime': record.killtime,
                'meansOFDeath': record.meansofdeath,
                'coordinates': record.cordinates
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
        record.recordId = form.get('id')
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

