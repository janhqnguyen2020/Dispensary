from ninja import Router, Schema
from .models import StoreSettings

from django.contrib.auth import authenticate
from ninja.errors import HttpError
from .auth import make_token, StaffAuth

#create collection of API endpoints that belong to core app
router = Router()

#defines structure of data your api is allowed to return
class StoreOut(Schema):
    ordering_mode: str
    store_name: str
    store_address: str
    hours: str

class LoginIn(Schema):
    username: str
    password: str

@router.get("/health")
def health(request):
    return {"ok": True}


#GET endpoint
@router.get("/store", response = StoreOut)
def store(request):
    return StoreSettings.load()

#post request. check login credentials
@router.post("/auth/login")
def login(request, payload: LoginIn):

    #django checks username and password againsts configured authenticated system
    user = authenticate(
        request,
        username = payload.username,
        password = payload.password,
    )

    #rejection: none, disabled or no access account
    if user is None or not user.is_active or not user.is_staff:
        raise HttpError(401, "Invalid credentials or staff access needed")

    return {"token": make_token(user)}

#require staff authentication
@router.get("/auth/me", auth = StaffAuth())
def me(request):
    user = request.auth
    return {
        "id": user.id,
        "username": user.username,
    }