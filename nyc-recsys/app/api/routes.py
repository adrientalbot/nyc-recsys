from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "NYC Recsys running"}

@router.get("/recommendations")
def recommendations():
    return {"results": []}