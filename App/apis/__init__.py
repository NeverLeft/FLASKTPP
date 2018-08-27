from flask_restful import Api

from App.apis.CinemasApi import CinemasResource
from App.apis.CityApi import CityResource
from App.apis.HelloApi import HelloResource
from App.apis.MovieApi import MovieResource
from App.apis.OrderApi import OrderResource
from App.apis.SeatApi import SeatResource
from App.apis.UserApi import UserResource
from App.apis.UserStatusApi import UserStatusResource
from App.models import Letter

api = Api()


def init_api(app):
    api.init_app(app=app)


api.add_resource(HelloResource, "/hello/")

api.add_resource(CityResource, "/cities/", methods=["GET", "POST"])

api.add_resource(MovieResource, "/movies/")

api.add_resource(CinemasResource, "/cinemas/")

api.add_resource(UserResource, "/users/", methods=["POST", "GET"])

api.add_resource(UserStatusResource, "/userstatus/")

api.add_resource(OrderResource, "/orders/", methods=["GET", "POST"])

api.add_resource(SeatResource, "/seats/")