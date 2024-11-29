from extension import db
from datetime import datetime

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_name = db.Column(db.String(20), unique=True, nullable=False,default=f"user{id}")
    player_rank = db.Column(db.String(10), unique=False, nullable=False,default="青铜",check_constraint='check(player_rank in (\'青铜\',\'白银\',\'黄金\',\'铂金\',\'钻石\',\'大师\'))')
    player_kda = db.Column(db.Float, unique=False, nullable=False, default=0)

    @staticmethod
    def init_db():
        pass
        # db.create_all()
        # rets = [
        #
        # ]
        #
        # for ret in rets:
        #     player = Player()
        #     player.id = ret[0]
        #     player.player_name = ret[1]
        #     player.player_rank = ret[2]
        #     player.player_kda = ret[3]
        #     db.session.add(player)
        # db.session.commit()

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_mode = db.Column(db.String(20), unique=False, nullable=False,default='casual',check_constraint='check(match_mode in (\'休闲\',\'排位\'))')
    match_time = db.Column(db.String(20), unique=False, nullable=False ,default=datetime.now())
    match_duration = db.Column(db.Integer, unique=False, nullable=False,default=0)
    match_result = db.Column(db.String(20), unique=False, nullable=False,default="正在进行",check_constraint='check(match_result in (\'胜利\',\'失败\',\'平局\',\'正在进行\')')
    match_map = db.Column(db.String(20), unique=False, nullable=False,default="map1")
    @staticmethod
    def init_db():
        db.create_all()
        rets = [
            (1, '排位', datetime(2021, 8, 1, 10, 0, 0), 180, '胜利', 'map1'),
            (2, '休闲', datetime(2021, 8, 1, 11, 0, 0), 120, '失败', 'map2'),
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


class MatchRecord(db.Model):  #来自比赛服务器
    __tablename__ = 'match_record'
    recordId = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    matchId = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    killerId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    victimId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    killTime = db.Column(db.Integer, nullable=False)
    meansOfDeath = db.Column(db.String(20), nullable=False,default='knife')
    coordinates = db.Column(db.String(20), nullable=False,default='100,100')

    @staticmethod
    def init_db():
        db.create_all()
        rets = [
            (1, 1, 1, 2, 100, 'knife', '100,100'),
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
            (1, 1, 1, 10, 5, 2.5, 100)
        ]
        for ret in rets:
            precord = PlayerRecord()
            precord.pmatchId = ret[0]
            precord.playerId = ret[1]
            precord.matchId = ret[2]
            precord.killCount = ret[3]
            precord.deathCount = ret[4]
            precord.kd = ret[5]
            precord.rankpoints = ret[6]
            db.session.add(precord)
        db.session.commit()

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=True)
    authority = db.Column(db.String(20), unique=False, nullable=True,check_constraint='check(authority in (\'admin\',\'user\'))')
    @staticmethod
    def init_db():
        db.create_all()
        rets = [
            (1, 1,'123456', 'admin', 'admin'),
            (2, 2,'123456', 'user1', 'user'),
            (3, 3,'123456', 'user2', 'user'),
            ]
        for ret in rets:
            account = Account()
            account.id = ret[0]
            account.playerId = ret[1]
            account.password = ret[2]
            account.name = ret[3]
            account.authority = ret[4]
            player = Player()
            player.id = ret[1]
            player.player_name = ret[3]
            player.player_rank = '青铜'
            player.player_kda = 0
            db.session.add(player)
            db.session.add(account)
        db.session.commit()









