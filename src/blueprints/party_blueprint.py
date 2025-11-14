from typing import Any

from flask import current_app, request
from flask.views import MethodView
from flask_smorest import Blueprint


party_blp = Blueprint("party", __name__)


@party_blp.route("/parties")
class Party(MethodView):
    @party_blp.response(status_code=201)  # type: ignore[misc]
    def post(self) -> dict[str, Any]:
        party_service = current_app.container.party_service
        return party_service.add_party(request.json)  # type: ignore[no-any-return]
