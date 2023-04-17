from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


developer_licenses = db.Table('developer_licenses',
                              db.Column('developer_id', db.Integer, db.ForeignKey(
                                  'developer.id'), primary_key=True),
                              db.Column('license_id', db.Integer, db.ForeignKey(
                                  'license.id'), primary_key=True)
                              )

developer_assets = db.Table('developer_assets',
                            db.Column('developer_id', db.Integer, db.ForeignKey(
                                'developer.id'), primary_key=True),
                            db.Column('asset_id', db.Integer, db.ForeignKey(
                                'asset.id'), primary_key=True)
                            )


class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50))
    active = db.Column(db.Boolean)
    licenses = db.relationship(
        'License', secondary=developer_licenses, backref=db.backref('developers', lazy=True))
    assets = db.relationship(
        'Asset', secondary=developer_assets, backref=db.backref('developers', lazy=True))


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    type = db.Column(db.Enum('laptop', 'keyboard',
                     'mouse', 'headset', 'monitor'))


class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    software = db.Column(db.String(50))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    fullname = db.Column(db.String(50))



