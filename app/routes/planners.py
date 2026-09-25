import json, os, uuid
from pathlib import Path
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from app.models.schemas import HomeRequest, PartyRequest, JewelryRequest
from app.services.recommendations import home_fallback, party_fallback, jewelry_fallback, normalize_ai_json
from app.services.gemini_utils import generate_recommendation, build_home_prompt, build_party_prompt, build_jewelry_prompt
from app.services.database import save_history, get_user_by_id

router=APIRouter()

def user_id(request):
    uid=request.session.get("user_id")
    if not uid: raise HTTPException(401,"Login required")
    return uid

@router.post("/generate-home")
async def generate_home(request: Request, payload: HomeRequest):
    uid=user_id(request)
    ai=generate_recommendation(build_home_prompt(payload))
    data=normalize_ai_json(ai) if ai else None
    source="gemini" if data else "fallback"
    if not data: data=home_fallback(payload)
    save_history(uid,"Home Interior",payload.model_dump_json(),json.dumps(data))
    return {"success":True,"planner":"Home Interior","data":data,"source":source}

@router.post("/generate-party")
async def generate_party(request: Request, payload: PartyRequest):
    uid=user_id(request)
    ai=generate_recommendation(build_party_prompt(payload))
    data=normalize_ai_json(ai) if ai else None
    source="gemini" if data else "fallback"
    if not data: data=party_fallback(payload)
    save_history(uid,"Party Planning",payload.model_dump_json(),json.dumps(data))
    return {"success":True,"planner":"Party Planning","data":data,"source":source}

@router.post("/generate-jewelry")
async def generate_jewelry(request: Request, budget: float=Form(...), occasion: str=Form(...), style_preferences: str=Form(""), outfit_image: UploadFile|None=File(None)):
    uid=user_id(request)
    image_path=None
    if outfit_image and outfit_image.filename:
        ext=Path(outfit_image.filename).suffix.lower()
        if ext not in [".jpg",".jpeg",".png",".webp"]:
            raise HTTPException(400,"Please upload a JPG, PNG, or WEBP image.")
        name=f"{uuid.uuid4().hex}{ext}"
        image_path=str(Path("static/uploads")/name)
        Path("static/uploads").mkdir(parents=True,exist_ok=True)
        Path(image_path).write_bytes(await outfit_image.read())
    payload=JewelryRequest(budget=budget,occasion=occasion,style_preferences=style_preferences,image_path=image_path)
    ai=generate_recommendation(build_jewelry_prompt(payload),image_path)
    data=normalize_ai_json(ai) if ai else None
    source="gemini" if data else "fallback"
    if not data: data=jewelry_fallback(payload)
    save_history(uid,"Jewelry",payload.model_dump_json(),json.dumps(data))
    return {"success":True,"planner":"Jewelry","data":data,"source":source}
