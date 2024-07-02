from app import create_app
from app.scheduler import create_scheduler

app = create_app()
scheduler = create_scheduler(app)
app.scheduler = scheduler

if __name__ == '__main__':
    app.run()
