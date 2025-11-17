from flask.views import MethodView
from flask_smorest import Blueprint

hc_blp = Blueprint("health", "health")


@hc_blp.route("/health-check")
class HealthCheck(MethodView):
    @hc_blp.response(200)  # type: ignore
    def get(self) -> dict[str, str]:
        """Health check endpoint to validate the service is up and running normally."""
        return {"message": "Party Service is healthy"}
