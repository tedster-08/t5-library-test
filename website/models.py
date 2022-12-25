from . import db


class MeritBadgePamphlet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512))
    is_eagle_required = db.Column(db.Boolean())
    is_up_to_date = db.Column(db.Boolean())
    is_checked_out = db.Column(db.Boolean())
