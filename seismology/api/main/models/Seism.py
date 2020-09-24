from .. import db


class Seism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id', ondelete='RESTRICT'), nullable=False)
    sensor = db.relationship("Sensor", back_populates="seisms", uselist=False, single_parent=True)

    def __repr__(self):
        return '<Seism: %r %r %r %r %r %r %r>' % (self.id, self.datetime, self.depth, self.magnitude, self.latitude, self.longitude, self.verified)
