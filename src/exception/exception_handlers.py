import logging
from http import HTTPStatus

from flask import Response, jsonify, request
from pydantic import ValidationError

from src.exception.error_dto import ErrorDTO

logger = logging.getLogger(__name__)


def handle_validation_error(e: ValidationError) -> tuple[Response, int]:
    if e.errors():
        validation_errors = []

        for error in e.errors():
            bad_field = ".".join(str(error["loc"]))
            validation_errors.append(
                f"Invalid value: {error['input']} for field '{bad_field}'. {error['msg']}."
            )

        error_dto = ErrorDTO(
            status=HTTPStatus.UNPROCESSABLE_ENTITY.value,
            title=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
            detail=f"Validation failed with ({len(validation_errors)}) errors",
            instance=request.path,
        ).to_dict(validation_errors=validation_errors)

        return jsonify(error_dto), 422

    logger.error(
        f"Could not process ValidationError because of invalid handler input: {e.errors}"
    )
    return jsonify({"message": "An unexpected error occurred processing request"}), 500
