from fastapi import HTTPException
from http import HTTPStatus


class BadRequest(HTTPException):
    def __init__(self, detail: str = 'Bad Request'):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)


class NotFound(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)
