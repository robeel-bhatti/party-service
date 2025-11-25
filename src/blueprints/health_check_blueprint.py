from flask.views import MethodView
from flask import Blueprint


class HealthCheck(MethodView):
    def get(self) -> tuple[dict[str, str], int]:
        """Health check endpoint to validate the service is up and running normally."""
        return {"message": "Party Service is healthy"}, 200


hc_blp = Blueprint("health_blueprint", __name__)
hc_blp.add_url_rule(rule="/health-check", view_func=HealthCheck.as_view("health_check"))
