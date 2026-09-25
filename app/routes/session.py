from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.database import get_user_by_id, get_history

router=APIRouter()

@router.get("/session-info")
async def session_info(request: Request):
    uid=request.session.get("user_id")
    user=get_user_by_id(uid) if uid else None
    return {"logged_in":bool(user),"user_id":user["id"] if user else None,"username":user["username"] if user else None}

@router.get("/session-data")
async def session_data(request: Request):
    uid=request.session.get("user_id")
    if not uid: return JSONResponse({"detail":"Login required"},status_code=401)
    return {"user":get_user_by_id(uid),"recent_history":get_history(uid,10)}

@router.get("/recommendations-details")
async def recommendation_details(request: Request):
    uid=request.session.get("user_id")
    if not uid: return JSONResponse({"detail":"Login required"},status_code=401)
    return {"history":get_history(uid,50)}
