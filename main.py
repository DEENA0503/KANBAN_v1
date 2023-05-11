from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from application import config
from application.config import LocalDevelopmentConfig
from application.models import db
import os

app = None
api = None


def create_app():
    app=Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)


    CORS(app)
    db.init_app(app)
    api=Api(app)  
    db.create_all(app=app)
    app.app_context().push()
    

    return app,api

app,api=create_app()

from application.controllers import *
from application.api import Userapi, Listapi, Cardapi, Summaryapi
api.add_resource(Userapi, "/api/user/<string:name>/<string:email>/<string:passw>", "/api/user")
api.add_resource(Listapi, "/api/user/<int:u_id>/lists", "/api/user/<int:u_id>/list/<int:l_id>")
api.add_resource(Cardapi, "/api/user/<int:user_id>/list/<int:list_id>/cards", "/api/user/<int:user_id>/list/<int:list_id>/card/<int:card_id>")
api.add_resource(Summaryapi, "/api/user/<int:user_id>/summary")

app.secret_key="hey" ##to create sessions

if __name__=="__main__":

    app.run(debug=False, port=8080)