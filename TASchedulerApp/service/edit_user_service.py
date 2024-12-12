from django.contrib.auth import update_session_auth_hash
from TASchedulerApp.models import MyUser

def update_user_profile(request, user, name, home_address, phone_number, password):
    # Update fields only if they were changed
    if name != user.name:
        user.name = name
    if home_address != user.home_address:
        user.home_address = home_address
    if phone_number != user.phone_number:
        user.phone_number = phone_number
    if password:
        user.set_password(password)

    user.save()

    # Keep the user logged in after password change
    if password:
        update_session_auth_hash(request, user)