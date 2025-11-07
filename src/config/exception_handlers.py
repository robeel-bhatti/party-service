import logging

from flask import Flask, Response, jsonify
from pydantic import ValidationError

logger = logging.getLogger(__name__)


def handle_validation_error(e: ValidationError) -> tuple[Response, int]:
    errors = e.errors()

    return jsonify({"message": "Validation failed", "errors": errors}), 422


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(ValidationError, handle_validation_error)
