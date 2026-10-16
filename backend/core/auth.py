from django.core import signing

from django.contrib.auth import get_user_model
from ninja.security import HttpBearer


#receives django user obj, creates signed token 
def make_token(user):
    return signing.dumps(
        {"uid": user.id},
        salt = "staff-token",
    )

#reusable authentication checker for endpoints that require bearer token
class StaffAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            #verify token signature, limit age to 12 hours
            data = signing.loads(
                token, 
                salt="staff-token",
                max_age = 12 * 60 * 60,
            )
            #tampered, bad tokens
        except signing.BadSignature:
            return None

        #get django user model configured for project
        User = get_user_model()

        try:
            #look up user id embedded in token, is staff, is active
            user = User.objects.get(
                pk=data["uid"],
                is_active = True,
                is_staff = True,
            )

        except (User.DoesNotExist, KeyError, TypeError):
            return None

        return user

def is_owner(user):
    return user.is_superuser or user.groups.filter(name = "Owner").exists()