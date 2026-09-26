from fastapi import APIRouter, Request

from fastapi.responses import RedirectResponse

from app.services.database import (
    get_user_by_id,
    get_history,
    get_history_item
)

router = APIRouter()


def current_user(request):
    uid = request.session.get("user_id")

    return get_user_by_id(uid) if uid else None


@router.get("/")
async def index(request: Request):

    return request.app.state.templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.get("/dashboard")
async def dashboard(request: Request):

    user = current_user(request)

    if not user:
        return RedirectResponse("/login", 303)

    return request.app.state.templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user
        }
    )


@router.get("/home-planner")
async def home_planner(request: Request):

    user = current_user(request)

    if not user:
        return RedirectResponse("/login", 303)

    return request.app.state.templates.TemplateResponse(
        "home_planner.html",
        {
            "request": request,
            "user": user
        }
    )


@router.get("/party-planner")
async def party_planner(request: Request):

    user = current_user(request)

    if not user:
        return RedirectResponse("/login", 303)

    return request.app.state.templates.TemplateResponse(
        "party_planner.html",
        {
            "request": request,
            "user": user
        }
    )


@router.get("/jewelry-planner")
async def jewelry_planner(request: Request):

    user = current_user(request)

    if not user:
        return RedirectResponse("/login", 303)

    return request.app.state.templates.TemplateResponse(
        "jewelry_planner.html",
        {
            "request": request,
            "user": user
        }
    )


@router.get("/history")
async def history(request: Request):

    user = current_user(request)

    if not user:
        return RedirectResponse("/login", 303)

    rows = get_history(user["id"])

    return request.app.state.templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "user": user,
            "history": rows
        }
    )


@router.get("/history/{history_id}")
async def history_detail(request: Request, history_id: int):

    user = current_user(request)

    if not user:
        return RedirectResponse("/login", 303)

    row = get_history_item(user["id"], history_id)

    if not row:
        return RedirectResponse("/history", 303)

    return request.app.state.templates.TemplateResponse(
        "recommendation_detail.html",
        {
            "request": request,
            "user": user,
            "recommendation": row
        }
    )


@router.get("/recommendations/home")
async def home_recommendations(request: Request):

    return RedirectResponse("/dashboard", 303)


@router.get("/testimonials")
def testimonials(request: Request):

    return request.app.state.templates.TemplateResponse(
        "testimonials.html",
        {
            "request": request
        }
    )