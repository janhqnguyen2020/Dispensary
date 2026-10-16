from ninja import NinjaAPI

from core.api import router as core_router

api = NinjaAPI(title="Dispensary API", version="1")

#registers router with main api
api.add_router("", core_router)