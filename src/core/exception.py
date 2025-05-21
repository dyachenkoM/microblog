from fastapi import status
from fastapi.responses import JSONResponse
import logging


class APIError(Exception):
    """Базовый класс для всех API исключений"""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_type: str = "internal_error"
    error_message: str = "Internal server error"

    def __init__(self, error_message: str | None = None):
        if error_message:
            self.error_message = error_message
        super().__init__(self.error_message)


class UserNotFoundError(APIError):
    status_code = status.HTTP_404_NOT_FOUND
    error_type = "not_found"
    error_message = "User not found"


class AlreadyFollowingError(APIError):
    status_code = status.HTTP_400_BAD_REQUEST
    error_type = "already_following"
    error_message = "Already following this user"


class SelfFollowError(APIError):
    status_code = status.HTTP_400_BAD_REQUEST
    error_type = "self_follow"
    error_message = "Cannot follow yourself"


class SubscriptionNotFoundError(APIError):
    status_code = status.HTTP_404_NOT_FOUND
    error_type = "subscription_not_found"
    error_message = "Subscription not found"


def handle_error(e: Exception, logger: logging.Logger) -> JSONResponse:
    """Унифицированный обработчик ошибок"""
    if isinstance(e, APIError):
        status_code = e.status_code
        error_type = e.error_type
        error_message = e.error_message
    else:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_type = "internal_error"
        error_message = "Internal server error"

    return JSONResponse(
        status_code=status_code,
        content={
            "result": False,
            "error_type": error_type,
            "error_message": error_message
        }
    )
