from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/v1/count",
    tags=["count"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=JSONResponse)
def get_count(request: Request):
    return request.counter.process()
