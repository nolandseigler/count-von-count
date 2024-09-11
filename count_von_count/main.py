

from fastapi import Depends, FastAPI
import structlog
from count_von_count.dependencies import get_new_test_counter
from count_von_count.logging import logging_init
from count_von_count.routes.count.routes import router as count_router

logging_init(log_level="DEBUG")
logger: structlog.types.FilteringBoundLogger = structlog.get_logger(__name__)

def create_app() -> FastAPI:
    logger.info("begin application creation")

    app = FastAPI(
        # TODO: for now we will do a new Counter per. spacy model seems thread safe
        # but really once we are streaming files to be used we need to decouple
        # Counter from the PdfReader which is a fully rearch.
        dependencies=[Depends(get_new_test_counter)],
    )

    logger.debug("including routers")
    app.include_router(count_router)

    logger.info("completed application creation")
    return app
