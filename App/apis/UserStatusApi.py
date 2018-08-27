from flask_restful import Resource, reqparse

from App.ext import cache
from App.models import User

parse = reqparse.RequestParser()
parse.add_argument("action", type=str, required=True, help="请提供具体操作")
parse.add_argument("u_token")


class UserStatusResource(Resource):

    def get(self):

        data = {}

        parser = parse.parse_args()

        action = parser.get("action")

        if action == "activate":

            u_token = parser.get("u_token")

            user_id = cache.get(u_token)

            cache.delete(u_token)

            if user_id:
                user = User.query.get(user_id)

                user.is_active = True

                user.save()

                data["returnCode"] = "0"
                data["returnValue"] = "user activate success"

                return data
            else:

                data["returnCode"] = "900"
                data["returnValue"] = "激活邮件过期，请重新激活邮件"

                return data
        else:
            pass

