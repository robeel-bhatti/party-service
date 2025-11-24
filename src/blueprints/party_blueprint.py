from typing import Any
import logging

from flask import current_app, request, Blueprint
from flask.views import MethodView

party_blp = Blueprint("party_blueprint", __name__, url_prefix="/parties")
logger = logging.getLogger(__name__)


class Party(MethodView):
    def post(self) -> tuple[dict[str, Any], int]:
        """Handles REST requests to create a new party."""

        logger.info("POST /parties endpoint received request to create Party.")
        party_service = current_app.container.party_service
        return party_service.add_party(request.json), 201
