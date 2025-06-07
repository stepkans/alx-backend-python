from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming the object has an 'owner' attribute:
        return obj.owner == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants of a conversation can send, view, update, or delete messages in that conversation.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated first
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Assuming obj is a Message or Conversation instance
        # and it has a 'conversation' attribute or directly a list of participants.

        # Example if obj is a message:
        conversation = getattr(obj, 'conversation', None)

        # If obj is a conversation itself, check participants directly
        if conversation is None and hasattr(obj, 'participants'):
            conversation = obj

        if conversation:
            # Check if user is a participant in this conversation
            return request.user in conversation.participants.all()
        return False    