from datetime import datetime

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask, current_app
from .models import DeviceState
from .database import db
from .socketio import socketio
from .models import DeviceStateChange

app = None


def current_date_colombia():
    colombia_tz = pytz.timezone('America/Bogota')
    return datetime.now(colombia_tz).date()


def current_time_colombia():
    colombia_tz = pytz.timezone('America/Bogota')
    return datetime.now(colombia_tz).time().strftime("%I:%M:%S %p")


def set_device_state(device_name, state):
    with current_app.app_context():
        device = DeviceState.query.filter_by(device_name=device_name).first()
        if device:
            device.state = state
            db.session.commit()
            state_change = DeviceStateChange(device=device_name,
                                             state=state,
                                             time=current_time_colombia(),
                                             date=current_date_colombia())
            db.session.add(state_change)
            db.session.commit()
            socketio.emit('state_updated', {device_name: state})


def job_wrapper(device_name, state):
    global app
    with app.app_context():
        set_device_state(device_name, state)


def create_scheduler(flask_app: Flask):
    global app
    app = flask_app
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI']), 'default')
    scheduler.start()
    return scheduler
