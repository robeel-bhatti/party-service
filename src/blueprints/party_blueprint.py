from typing import Any
import logging

from flask import current_app, Blueprint
from flask.views import MethodView

from src.config.enums import ServiceEntities
from src.dto.request_dtos import PartyRequest
from src.middleware.validation import validate_request
from src.middleware.caching import cache_read

logger = logging.getLogger(__name__)


class PartyBaseView(MethodView):
    def __init__(self) -> None:
        self._party_service = current_app.container.party_service


class PartyListView(PartyBaseView):
    @validate_request(PartyRequest)
    def post(self, party_request: PartyRequest) -> tuple[dict[str, Any], int]:
        """Handles REST requests to create a new party."""
        logger.info("POST /parties endpoint received request to create Party.")
        return self._party_service.add_party(party_request), 201


class PartyDetailView(PartyBaseView):
    @cache_read(ServiceEntities.PARTY)
    def get(self, id: int) -> tuple[dict[str, Any], int]:
        """Handles REST request to retrieve an existing party by ID."""
        logger.info(
            f"GET /parties endpoint received request to retrieve Party with ID {id}."
        )
        return self._party_service.get_party(id), 200


party_blp = Blueprint("party_blueprint", __name__, url_prefix="/api")
party_blp.add_url_rule(
    "/v1/parties", view_func=PartyListView.as_view("party_list_view")
)
party_blp.add_url_rule(
    "/v1/parties/<int:id>", view_func=PartyDetailView.as_view("party_detail_view")
)
