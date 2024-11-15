from extension import db
from datetime import datetime

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_name = db.Column(db.String(20), unique=False, nullable=False)
    player_rank = db.Column(db.String(10), unique=False, nullable=True)
    player_kda = db.Column(db.Float, unique=False, nullable=True)

    @staticmethod
    def init_db():
        db.create_all()
        rets = [
            (1, 'ace', '白银', 2.3),
            (2, 'mkk', '黄金', 3),
        ]

        for ret in rets:
            player = Player()
            player.id = ret[0]
            player.player_name = ret[1]
            player.player_rank = ret[2]
            player.player_kda = ret[3]
            db.session.add(player)
        db.session.commit()

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_mode = db.Column(db.String(20), unique=False, nullable=False)
    match_time = db.Column(db.DateTime, unique=False, nullable=True )
    match_duration = db.Column(db.Integer, unique=False, nullable=True)
    match_result = db.Column(db.String(20), unique=False, nullable=True)
    match_map = db.Column(db.String(20), unique=False, nullable=True)
    @staticmethod
    def init_db():
        db.create_all()
        rets = [
            (1, 'ranked', datetime(2021, 8, 1, 10, 0, 0), 180, 'win', 'map1'),
            (2, 'normal', datetime(2021, 8, 1, 11, 0, 0), 120, 'lose', 'map2'),
        ]
        for ret in rets:
            match = Match()
            match.id = ret[0]
            match.match_mode = ret[1]
            match.match_time = ret[2]
            match.match_duration = ret[3]
            match.match_result = ret[4]
            match.match_map = ret[5]
            db.session.add(match)
        db.session.commit()


class MatchRecord(db.Model):#来自比赛服务器
    __tablename__ = 'match_record'
    recordId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    matchId = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    killerId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    victimId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    killTime = db.Column(db.Integer, nullable=False)
    meansOfDeath = db.Column(db.String(20), nullable=False)
    coordinates = db.Column(db.String(20), nullable=False)

    @staticmethod
    def init_db():
        db.create_all()
        rets = [
            (1, 1, 1, 2, 100, 'knife', '100,100'),
            (2, 1, 2, 1, 200, 'grenade', '200,200'),
        ]
        for ret in rets:
            record = MatchRecord()
            record.recordId = ret[0]
            record.matchId = ret[1]
            record.killerId = ret[2]
            record.victimId = ret[3]
            record.killTime = ret[4]
            record.meansOfDeath = ret[5]
            record.coordinates = ret[6]
            db.session.add(record)
        db.session.commit()

class PlayerRecord(db.Model):
    __tablename__ = 'player_record'
    pmatchId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    matchId = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    killCount = db.Column(db.Integer, nullable=False)
    kd = db.Column(db.Float, nullable=False)
    deathCount = db.Column(db.Integer, nullable=False)
    rankpoints = db.Column(db.Integer, nullable=False)
    @staticmethod
    def init_db():
        db.create_all()
        rets = [
            (1, 1, 1, 10, 5, 2.5, 1000),
            (2, 2, 1, 8, 4, 2.0, 800),
        ]
        for ret in rets:
            record = PlayerRecord()
            record.pmatchId = ret[0]
            record.playerId = ret[1]
            record.matchId = ret[2]
            record.killCount = ret[3]
            record.deathCount = ret[4]
            record.kd = ret[5]
            record.rankpoints = ret[6]
            db.session.add(record)
        db.session.commit()












