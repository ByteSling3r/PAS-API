from .database import db
from datetime import datetime
import pytz


class DeviceState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), unique=True, nullable=False)
    state = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<DeviceState {self.device_name}: {self.state}>'


def initialize_default_devices():
    default_devices = [
        {"device_name": "Light", "state": "OFF"},
        {"device_name": "air", "state": "OFF"}
    ]

    for device in default_devices:
        if not DeviceState.query.filter_by(device_name=device["device_name"]).first():
            new_device = DeviceState(device_name=device["device_name"], state=device["state"])
            db.session.add(new_device)

    db.session.commit()


def current_date_colombia():
    colombia_tz = pytz.timezone('America/Bogota')
    return datetime.now(colombia_tz).date()


def current_time_colombia():
    colombia_tz = pytz.timezone('America/Bogota')
    return datetime.now(colombia_tz).time()


class DeviceStateChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, default=current_date_colombia)
    time = db.Column(db.Time, default=current_time_colombia)

    def __repr__(self):
        return f'<DeviceStateChange {self.device} {self.state} {self.time} {self.date}>'


class DeviceProgramming(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), nullable=False)
    on_time = db.Column(db.Time, nullable=False)
    off_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<DeviceProgramming {self.device_name} - On: {self.on_time} / Off: {self.off_time}>'
