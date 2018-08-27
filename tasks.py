from time import sleep

from celery import Celery

app = Celery("app", broker="redis://localhost:6379/0")


@app.task
def add(a ,b):

    print("准备开始计算")

    print( a + b)

    sleep(5)

    return a + b