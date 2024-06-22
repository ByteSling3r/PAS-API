from .database import db


class DeviceState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), unique=True, nullable=False)
    state = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<DeviceState {self.device_name}: {self.state}>'