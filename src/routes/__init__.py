from fastapi import APIRouter

router = APIRouter()

from . import auth, tickers, questions, analyze

router.include_router(auth.router, prefix="/auth", tags=["Auth & User Management"])
router.include_router(tickers.router, prefix="/tickers", tags=["Tickers API"])
router.include_router(questions.router, prefix="/questions", tags=["User Configured Questions"])
router.include_router(analyze.router, prefix="/analyze", tags=["Processing & History"])
