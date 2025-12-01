import logging
from http import HTTPStatus

from flask import Response, jsonify, request
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from pydantic import ValidationError

from src.exception.error_dto import ErrorDTO

logger = logging.getLogger(__name__)


def handle_validation_error(e: ValidationError) -> tuple[Response, int]:
    """Handle validation errors that occur during Pydantic model validation."""

    logger.error(
        f"The request failed due to the following validation error(s): {e.json(indent=4)}"
    )
    validation_errors = [
        {"field": ".".join(str(loc) for loc in error["loc"]), "message": error["msg"]}
        for error in e.errors()
    ]

    error_dto = ErrorDTO(
        status=HTTPStatus.UNPROCESSABLE_ENTITY.value,
        title=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
        detail="Request validation failed",
        instance=request.path,
    ).to_dict(validation_errors=validation_errors)

    return jsonify(error_dto), 422


def handle_database_error(e: SQLAlchemyError) -> tuple[Response, int]:
    """Handle database errors that occur during the request."""

    logger.exception(f"The request failed due to the following database error: {e}")
    error_dto = ErrorDTO(
        status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        title=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        detail="An unexpected error occurred processing request.",
        instance=request.path,
    ).to_dict()

    return jsonify(error_dto), 500


def handle_not_found_error(e: NoResultFound) -> tuple[Response, int]:
    """Handles errors when the entity was not found and one was expected to be there."""
    party_id = request.view_args["id"]
    logger.exception(f"Could not find Party with ID: {party_id} in database: {e}")
    error_dto = ErrorDTO(
        status=HTTPStatus.NOT_FOUND.value,
        title=HTTPStatus.NOT_FOUND.phrase,
        detail=f"Party {party_id} was not found.",
        instance=request.path,
    ).to_dict()

    return jsonify(error_dto), 404
