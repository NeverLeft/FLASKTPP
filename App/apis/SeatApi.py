from flask import request
from flask_restful import Resource

from App.ext import cache
from App.models import MoviePlan, Hall, Ticket


class SeatResource(Resource):

    def get(self):
        # 获取排挡id
        planid = request.args.get("planid")
        # 获取排挡信息
        movie_plan = MoviePlan.query.get(planid)
        # 根据排挡获取大厅
        hall = Hall.query.get(movie_plan.mp_hall)
        # 从大厅中获取作为信息

        order_list = cache.get(planid)

        if not order_list:

            hall_data = {
                "h_count": hall.h_count,
                "h_seats": hall.seats
            }
        else:

            hall_seats = hall.seats

            hall_seat_list = hall_seats.split("#")

            for order_id in order_list:
                tickets = Ticket.query.filter(Ticket.t_order == order_id)

                for ticket in tickets:
                    # 移除大厅对应的位置
                    hall_seat_list.remove(ticket.t_seat)

            hall_data = {
                "h_count": hall.h_count,
                "h_seats": hall_seat_list.join("#")
            }

        data = {
            "returnCode": "0",
            "returnValue": hall_data
        }

        return data
