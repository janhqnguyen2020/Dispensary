from ninja import Router, Schema
from .models import StoreSettings

#create collection of API endpoints that belong to core app
router = Router()

#defines structure of data your api is allowed to return
class StoreOut(Schema):
    ordering_mode: str
    store_name: str
    store_address: str
    hours: str

@router.get("/health")
def health(request):
    return {"ok": True}


#GET enspoint
@router.get("/store", response = StoreOut)
def store(request):
    return StoreSettings.load()