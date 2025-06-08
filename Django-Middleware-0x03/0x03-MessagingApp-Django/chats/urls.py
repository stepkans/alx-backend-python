from django.urls import path, include 
from rest_framework import routers  
from rest_framework_nested.routers import NestedDefaultRouter  
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")  # ✅ conversations


nested_router = NestedDefaultRouter(router, r"conversations", lookup="conversation")
nested_router.register(r"messages", MessageViewSet, basename="conversation-messages")  # ✅ nested messages

urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_router.urls)),  
]