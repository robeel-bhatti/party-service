from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from src.dto.party_dto import PartyDTO

party_blp = Blueprint("party", __name__)


@party_blp.route("/parties")
class Party(MethodView):
    def post(self) -> None:
        PartyDTO(**request.json)
