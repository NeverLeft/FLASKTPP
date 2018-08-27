from flask import request
from flask_restful import Resource, abort

from App import models
from App.ext import cache
from App.models import User, Order, Ticket


def login_required(fun):

    def f(*args, **kwargs):
        u_token = request.args.get("u_token")
        print(u_token)
        if u_token:

            user_id = cache.get(u_token)

            if user_id:

                return fun(*args, **kwargs)
            else:
                abort(401, message="用户状态失效")
        else:
            # 未认证
            abort(401, message="您还未登录")
    return f


def check_permission(dest_permission):

    def check(fun):

        def f(*args, **kwargs):

            u_token = request.form.get("u_token")

            if not u_token:
                abort(401, message="用户未登录")
            else:
                user_id = cache.get(u_token)

                if not user_id:
                    abort(401, message="用户状态失效")
                else:
                    user = User.query.get(user_id)

                    if user.check_permission(dest_permission):
                        return fun(*args, **kwargs)
                    else:
                        abort(403, message="您没有权限访问此模块")
        return f
    return check


class OrderResource(Resource):

    @login_required
    def get(self):

        # u_token = request.args.get("u_token")
        #
        # if u_token:
        #     #
        #     #
        #     #
        #     id = cache.get(u_token)
        #
        #     if id:
        #         user = User.query.get(id)
        #
        #     else:
        #         pass
        #
        #     return {"msg": "order ok"}
        # else:
        #
        #     return {"msg": "你还未登录"}
        return {'msg': "get ok"}

    @check_permission(models.PERMISSION_ORDERED)
    def post(self):

        # 只要能进来的，就代表用户登录状态有效，并且用户有权限进行次操作
        # 直接书写操作即可

        # u_token = request.form.get("u_token")
        #
        # if u_token:
        #
        #     user_id = cache.get(u_token)
        #
        #     if user_id:
        #
        #         user = User.query.get(user_id)
        #
        #         if user.check_permission(models.PERMISSION_MODIFCATION):
        #             return {"msg": "post ok"}
        #         else:
        #             abort(403, message="你没有权限访问此模块")
        #     else:
        #         abort(401, message="用户状态失效")
        # else:
        #     abort(401, message="用户未登录")

        """
            下单
                用户
                排挡（目前还没有）
                    电影
                    大厅   没有
                        定义一个表
                             大厅类型
                             座位
                             （0,0） （0,1)
                              1 - 16

                              一排就是五个位置
                              0   1  2  3   4
                                  6  7  8   9
                                  11 12 13  14




        """

        u_token = request.form.get("u_token")
        mp = request.form.get("mp")
        seats = request.form.get("seats")

        order = Order()
        order.o_user = cache.get(u_token)
        order.o_movie_plan = mp

        order.save()

        seat_list = seats.split("#")

        for seat_position in seat_list:

            ticket = Ticket()
            ticket.t_order = order.id
            ticket.t_seat = int(seat_position)
            ticket.save()

        order_list = cache.get(mp)

        if not order_list:
            order_list.append(order.id)
            # 将订单放到缓存中
            cache.set(mp,order_list)

        data = {
            "returnCode": "0",
            "returnValue": order.id
        }


        return data
