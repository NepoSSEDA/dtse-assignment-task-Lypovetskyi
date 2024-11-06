from fastapi import APIRouter
from api_server.preprocess_data import router as preprocess_router
from api_server.get_prediction import router as get_prediction_router

router = APIRouter()
router.include_router(preprocess_router)
router.include_router(get_prediction_router)