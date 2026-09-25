from typing import Dict, Any

def _platform_link(platform: str, query: str) -> str:
    from urllib.parse import quote_plus
    q = quote_plus(query)
    links = {
        "Amazon": f"https://www.amazon.in/s?k={q}",
        "Flipkart": f"https://www.flipkart.com/search?q={q}",
        "IKEA": f"https://www.ikea.com/in/en/search/?q={q}",
        "Swiggy": f"https://www.swiggy.com/search?query={q}",
        "Zomato": f"https://www.zomato.com/search?query={q}",
        "OYO": f"https://www.oyorooms.com/search?location={q}",
    }
    return links.get(platform, "#")

def home_fallback(req) -> Dict[str, Any]:
    budget = float(req.budget)
    rooms = req.room_types or ["Living Room"]
    items = [
        {"category":"Lighting","description":"Warm LED ceiling light","price":round(min(budget*0.08, 3500),2),"quantity":req.quantities.get("lights",1),"platform":"Amazon"},
        {"category":"Ceiling Fans","description":"Energy-efficient ceiling fan","price":round(min(budget*0.10, 4500),2),"quantity":req.quantities.get("fans",1),"platform":"Amazon"},
        {"category":"Furniture","description":"Compact modern accent furniture","price":round(min(budget*0.30, 12000),2),"quantity":req.quantities.get("furniture",1),"platform":"IKEA"},
        {"category":"Dining Table","description":"Space-saving dining table","price":round(min(budget*0.20, 10000),2),"quantity":req.quantities.get("dining",1),"platform":"IKEA"},
    ]
    for x in items:
        x["shopping_link"] = _platform_link(x["platform"], x["description"])
    total = sum(x["price"] * x["quantity"] for x in items)
    return {"budget":budget,"remaining":max(0, round(budget-total,2)),"rooms":rooms,"items":items,
            "additional_suggestions":["Compare similar products before buying.","Keep a small buffer for delivery and installation.","Prioritize essential furniture before decorative items."]}

def party_fallback(req) -> Dict[str, Any]:
    budget=float(req.budget); guests=int(req.guests)
    allocation={"Catering":round(budget*0.50,2),"Decoration":round(budget*0.20,2),"Entertainment":round(budget*0.15,2),"Venue":round(budget*0.15,2)}
    return {"budget":budget,"guests":guests,"event_type":req.event_type,"venue_type":req.venue_type,
            "allocation":allocation,
            "options":[
                {"category":"Catering","description":f"Food package for {guests} guests","budget":allocation["Catering"],"platform":"Zomato","shopping_link":_platform_link("Zomato",f"{req.event_type} catering")},
                {"category":"Venue","description":f"{req.venue_type} event venue","budget":allocation["Venue"],"platform":"OYO","shopping_link":_platform_link("OYO",req.venue_type)},
                {"category":"Decoration","description":"Theme decoration package","budget":allocation["Decoration"],"platform":"Amazon","shopping_link":_platform_link("Amazon","party decoration")},
            ],
            "suggestions":["Confirm guest count before final booking.","Reserve part of the budget for last-minute needs."]}

def jewelry_fallback(req) -> Dict[str, Any]:
    budget=float(req.budget)
    style=req.style_preferences or "Elegant"
    options=[
        {"name":"Minimal necklace set","description":f"{style} look suitable for {req.occasion}","price":round(budget*0.35,2),"platform":"Amazon"},
        {"name":"Statement earrings","description":f"Occasion-ready {style} earrings","price":round(budget*0.20,2),"platform":"Flipkart"},
        {"name":"Bracelet / bangle set","description":"Coordinated accessory option","price":round(budget*0.20,2),"platform":"Amazon"},
    ]
    for x in options:
        x["shopping_link"]=_platform_link(x["platform"],x["name"])
    return {"budget":budget,"occasion":req.occasion,"style":style,"image_analyzed":bool(req.image_path),
            "options":options,"suggestions":["Match metals and tones with the outfit.","Choose one statement piece and keep the rest simple."]}

def normalize_ai_json(text: str):
    import json, re
    text=re.sub(r"^```(?:json)?\s*|\s*```$","",text.strip(),flags=re.I)
    try: return json.loads(text)
    except Exception: return None
