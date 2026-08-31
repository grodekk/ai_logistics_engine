from fastapi import Request
from fastapi.responses import JSONResponse
import logging
from src.core.exceptions import InfrastructureError, BusinessLogicError

logger = logging.getLogger(__name__)

def register_exception_handlers(app):
    @app.exception_handler(InfrastructureError)
    async def infra_error_handler(_: Request, exc: InfrastructureError):
        logger.error(f"[{exc.error_id}] {exc.message}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={"message": exc.user_message, "error_id": exc.error_id}
        )

    @app.exception_handler(BusinessLogicError)
    async def business_error_handler(_: Request, exc: BusinessLogicError):
        logger.warning(f"[{exc.error_id}] {exc.message}")
        return JSONResponse(
            status_code=400,
            content={"message": exc.user_message, "error_id": exc.error_id}
        )