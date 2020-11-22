from flask import Flask
from flask_restful import Resource, Api
import main
import os

app = Flask(__name__)
api = Api(app)

AuthKey1 = os.environ.get("KEY1")
AuthKey2 = os.environ.get("KEY2")
AuthKey3 = os.environ.get("KEY3")
AuthKey4 = os.environ.get("KEY4")

main.SetupApi(AuthKey1, AuthKey2, AuthKey3, AuthKey4)

class Similarity(Resource):
    def get(self, user1, user2):
        sim_cats = main.GetSimilarity(user1, user2)
        return {"categories": sim_cats}

api.add_resource(Similarity, '/similarity/<string:user1>/<string:user2>')

if __name__ == '__main__':
    app.run(debug=True)