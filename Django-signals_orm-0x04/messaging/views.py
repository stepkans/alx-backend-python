from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect("home")  # or wherever you want to go after deletion

    return render(request, "messaging/confirm_delete.html")
