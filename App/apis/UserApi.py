import uuid

from flask import render_template
from flask_mail import Message
from flask_restful import Resource, reqparse, fields, marshal_with

from App import ModelUtil
from App.ext import mail, cache
from App.models import User

parse = reqparse.RequestParser()
parse.add_argument("uname", type=str, required=True, help="请提供用户名")
parse.add_argument("uemail", type=str, help="请提供邮箱")
parse.add_argument("upassword", type=str, required=True, help="请提供密码")
parse.add_argument("action", type=str, required=True, help="请声明具体操作")

user_fields = {
    "u_name": fields.String,
    "u_email": fields.String
}

result_fields = {
    "u_token": fields.String,
    "returnMsg": fields.String,
    "returnCode": fields.String,
    "returnValue": fields.Nested(user_fields)
}


class UserResource(Resource):

    @marshal_with(result_fields)
    def post(self):
        parser = parse.parse_args()

        action = parser.get("action")

        if action == "register":

            u_name = parser.get("uname")
            u_email = parser.get("uemail")
            u_password = parser.get("upassword")

            user = User()

            user.u_name = u_name
            user.u_email = u_email
            # new_password = generate_password_hash(u_password)
            # user.u_password = new_password
            user.set_password(u_password)

            # db.session.add(user)
            # db.session.commit()
            #
            result = user.save()

            if result == ModelUtil.FAILURE:
                data = {
                    "returnCode": "902",
                    "returnMsg": "用户已经存在"
                }
                return data

            u_token = str(uuid.uuid4())

            cache.set(u_token, user.id, timeout=60 * 60 * 24)

            subject = "淘票票用户激活"

            msg = Message(subject=subject, sender="rongjiawei1204@163.com", recipients=[u_email])

            html = render_template('user_activate.html', username='Tom',
                                   activate_url="http://localhost:5000/userstatus/?action=activate&u_token=%s" % u_token)

            msg.html = html

            mail.send(msg)

            data = {
                "returnCode": "0",
                "returnValue": user
            }

            return data
        elif action == "login":
            u_name = parser.get("uname")
            u_password = parser.get("upassword")

            users = User.query.filter(User.u_name == u_name).all()

            if len(users) == 1:
                user = users[0]
                # if user.u_password == u_password:
                if user.verify_password(u_password):

                    u_token = str(uuid.uuid4())

                    # cache.set(u_token, user.id, timeout=60 * 60 * 24 * 14)
                    cache.set(u_token, user.id)

                    data = {
                        "u_token": u_token,
                        "returnCode": "0",
                        "returnValue": user
                    }

                    return data
                else:
                    data = {
                        "returnCode": "901",
                        "returnMsg": "用户名或密码错误"
                    }
                    return data
            else:
                data = {
                    "returnCode": "901",
                    "returnMsg": "用户名或密码错误"
                }
                return data

    def get(self):
        return {"msg": "get ok"}
