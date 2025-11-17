import os
import sys
from typing import Optional
import logging

from flask import Flask
from flask_smorest import Api
from pydantic import ValidationError
from redis import Redis
from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.blueprints.health_check_blueprint import hc_blp
from src.blueprints.party_blueprint import party_blp
from src.config.container import Container
from src.exception.exception_handlers import handle_validation_error


class Config:
    DEBUG = True
    API_TITLE = "My API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"


def create_app() -> Flask:
    """Application factory pattern."""
    init_logger()
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    init_cache(app)
    init_di(app)
    init_exception_handlers(app)

    api = Api(app)
    api.register_blueprint(hc_blp)
    api.register_blueprint(party_blp)

    return app


def init_logger() -> None:
    """Customize the root level logger.
    These settings will then propagate down to the child loggers (flask, blueprint, service loggers etc).
    """
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
        handlers=[logging.StreamHandler(stream=sys.stdout)],
    )


def init_di(app: Flask) -> None:
    container = Container(app.session())
    app.container = container


def init_db(app: Flask) -> None:
    options = {
        "poolclass": QueuePool,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }

    url = os.getenv("DATABASE_URL")
    if url is None:
        raise Exception(
            "App failed to start because the environment variable 'DATABASE_URL' is not set"
        )

    engine = create_engine(url, **options)
    session_factory = sessionmaker(bind=engine)
    app.session = scoped_session(session_factory)

    @app.teardown_appcontext
    def close_session(exc: Optional[Exception] = None) -> None:
        if hasattr(app, "session"):
            app.session.remove()


def init_cache(app: Flask) -> None:
    url = os.getenv("CACHE_URL")
    if url is None:
        raise Exception(
            "App failed to start because the environment variable 'REDIS_URL' is not set"
        )

    cache = Redis.from_url(url)
    app.cache = cache


def init_exception_handlers(app: Flask) -> None:
    app.register_error_handler(ValidationError, handle_validation_error)
