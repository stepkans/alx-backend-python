from .views import delete_user

urlpatterns = [
    path('delete-user/', delete_user, name='delete-user'),
]