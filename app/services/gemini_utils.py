import os, json, mimetypes
from dotenv import load_dotenv
load_dotenv()

def _client():
    key=os.getenv("GEMINI_API_KEY","").strip()
    if not key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        return genai
    except Exception:
        return None

def generate_recommendation(prompt: str, image_path: str | None = None):
    genai=_client()
    if not genai:
        return None
    model_name=os.getenv("GEMINI_MODEL","gemini-1.5-flash")
    try:
        model=genai.GenerativeModel(model_name)
        parts=[prompt]
        if image_path:
            mime=mimetypes.guess_type(image_path)[0] or "image/jpeg"
            parts.append({"mime_type":mime,"data":open(image_path,"rb").read()})
        response=model.generate_content(parts)
        return getattr(response,"text",None)
    except Exception:
        return None

def build_home_prompt(req):
    return f'''You are PocketSmart AI, a budget recommendation assistant.
Return ONLY valid JSON with keys budget, remaining, rooms, items, additional_suggestions.
User budget: {req.budget}. Rooms: {req.room_types}. Quantities: {req.quantities}.
Additional information: {req.additional_information}.
Recommend practical options and platform names such as Amazon and IKEA. Keep the total within budget.'''
def build_party_prompt(req):
    return f'''You are PocketSmart AI. Return ONLY valid JSON with keys budget, guests, event_type,
venue_type, allocation, options, suggestions. Budget={req.budget}; guests={req.guests};
event={req.event_type}; venue={req.venue_type}; needs={req.needs}; notes={req.additional_information}.
Allocate the budget across catering, decoration, entertainment and venue.'''
def build_jewelry_prompt(req):
    return f'''You are PocketSmart AI. Return ONLY valid JSON with keys budget, occasion, style,
image_analyzed, options, suggestions. Budget={req.budget}; occasion={req.occasion};
style={req.style_preferences}. Recommend jewelry that coordinates with the supplied outfit image if present.'''
