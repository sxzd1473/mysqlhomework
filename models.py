from extension import db

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











