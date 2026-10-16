from ninja import NinjaAPI

api = NinjaAPI(title="Dispensary API", version="1")

@api.get("/health")
def health(request):
    return {"ok": True}