from time import sleep

from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")


@app.task
def add(a ,b):

    print("准备开始计算")

    print( a + b)

    sleep(5)

    return a + b


if __name__ == '__main__':

    print("啦啦啦德玛西亚")

    add.delay(2, 3)

    print("今天是个好天气")



