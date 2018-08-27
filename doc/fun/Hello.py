import random
import time


def total_time(fun):
    def f():
        before_time = time.time()
        fun()
        after_time = time.time()
        total = after_time - before_time
        print(total)

    return f


# 带参数的装饰器
def total_time_params(fun):

    def f(*args, **kwargs):
        before_time = time.time()
        fun(*args, **kwargs)
        after_time = time.time()
        total = after_time - before_time
        print(total)
    return f



@total_time
def add():
    time.sleep(1)
    return 3


@total_time_params
def sub(a, b):
    print("打不到，打不到")
    time.sleep(2)
    print("你怎么又睡着了")
    return a - b


def check_permission(permission):
    def can_play(fun):

        def f(*args, **kwargs):
            if permission > 90:
                fun(*args, **kwargs)
            else:
                print("小伙子，作业没写完，不能游戏，写完作业，洗洗睡吧")
        return f
    return can_play


@check_permission(80)
def play_game():

    print("贪吃蛇一小时")


if __name__ == '__main__':
    # before_time = time.time()
    # add(1, 2)
    # after_time = time.time()
    # total = after_time - before_time
    # print(total)

    # add()

    # sub(5, 3)

    play_game()
