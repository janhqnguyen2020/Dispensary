from django.core import signing


#receives django user obj, creates signed token 
def make_token(user):
    return signing.dumps(
        {"uid": user.id},
        salt = "staff-token",
    )