from ninja import Router, Schema

from .pricing import quote

router = Router()#register router

class CartItemIn(Schema):
    variant_id: int
    qty: int

class CartQuoteIn(Schema):
    items: list[CartItemIn]
    mode: str
    zip_code: str = ""

@router.post("/cart/quote", response = {200: dict, 400: dict})
def cart_quote(request, payload: CartQuoteIn):
    try:
        result = quote(
            items = [item.dict() for item in payload.items], mode = payload.mode, zip_code = payload.zip_code,)
    except ValueError as exc:
        return 400, {"error": str(exc)}

    return result