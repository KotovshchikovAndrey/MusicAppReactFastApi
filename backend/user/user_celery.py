from celery import Celery

app = Celery('token', broker='redis://localhost:6379', include=['user.user_tasks'])


if __name__ == '__main__':
    app.start()