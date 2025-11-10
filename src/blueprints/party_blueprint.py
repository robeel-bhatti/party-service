from flask import current_app, request
from flask.views import MethodView
from flask_smorest import Blueprint

party_blp = Blueprint("party", __name__)


@party_blp.route("/parties")
class Party(MethodView):
    def post(self) -> str:
        party_service = current_app.container.party_service
        party_service.add_party(request.json)
        return "Success"
