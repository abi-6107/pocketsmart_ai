from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    username: str
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    room_types: List[str] = []
    quantities: Dict[str, int] = {}
    additional_information: str = ""

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0)
    event_type: str = "Birthday"
    venue_type: str = "Home"
    needs: List[str] = []
    additional_information: str = ""

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str = "Birthday"
    style_preferences: str = ""
    image_path: Optional[str] = None

class RecommendationResponse(BaseModel):
    success: bool
    planner: str
    data: Dict[str, Any]
    source: str = "fallback"
    message: Optional[str] = None
