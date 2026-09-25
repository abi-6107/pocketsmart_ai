from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from app.services.database import create_user, get_user_by_username
from app.services.auth import hash_password, verify_password, create_access_token

router=APIRouter()

@router.get("/register")
async def register_page(request: Request):
    return request.app.state.templates.TemplateResponse("register.html", {"request":request})

@router.post("/register")
async def register(request: Request, username: str=Form(...), email: str=Form(...), password: str=Form(...), confirm_password: str=Form(...)):
    if password != confirm_password:
        return request.app.state.templates.TemplateResponse("register.html", {"request":request,"error":"Passwords do not match."})
    user_id=create_user(username,email,hash_password(password))
    if not user_id:
        return request.app.state.templates.TemplateResponse("register.html", {"request":request,"error":"Username or email already exists."})
    return RedirectResponse("/login?registered=1", status_code=303)

@router.get("/login")
async def login_page(request: Request):
    return request.app.state.templates.TemplateResponse("login.html", {"request":request})

@router.post("/login")
async def login(request: Request, username: str=Form(...), password: str=Form(...)):
    user=get_user_by_username(username)
    if not user or not verify_password(password,user["password_hash"]):
        return request.app.state.templates.TemplateResponse("login.html", {"request":request,"error":"Invalid username or password."})
    request.session["user_id"]=user["id"]
    request.session["username"]=user["username"]
    return RedirectResponse("/dashboard", status_code=303)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)

@router.post("/token")
async def token(username: str=Form(...), password: str=Form(...)):
    user=get_user_by_username(username)
    if not user or not verify_password(password,user["password_hash"]):
        return JSONResponse({"detail":"Invalid credentials"},status_code=401)
    return {"access_token":create_access_token(user["id"]),"token_type":"bearer"}
