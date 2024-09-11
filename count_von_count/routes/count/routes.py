from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import JSONResponse

from count_von_count.counter import Counter

router = APIRouter(
    prefix="/api/v1/count",
    tags=["count"],
    responses={404: {"description": "Not found"}},
)


@router.get("/test", response_class=JSONResponse)
def get_count(request: Request):
    return request.counter.process()

@router.post("/", response_class=JSONResponse)
async def create_upload_file(request: Request, file: UploadFile):
    return Counter(
        nlp=request.nlp,
        pdf_file_obj=file.file,
    ).process()
