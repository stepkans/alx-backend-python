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
    Custom permission that:
    - Allows only authenticated users.
    - Allows only participants of a conversation to view (GET) and modify (PUT, PATCH, DELETE) messages.
    """

    def has_permission(self, request, view):
        # Only authenticated users allowed overall
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if user is participant of the conversation associated with the message or conversation

        conversation = getattr(obj, 'conversation', None)
        # If obj itself is a conversation, check participants directly
        if conversation is None and hasattr(obj, 'participants'):
            conversation = obj

        if not conversation:
            return False  # No conversation found, deny access

        is_participant = request.user in conversation.participants.all()

        # For read-only methods, allow only if participant
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return is_participant

        # For write methods (PUT, PATCH, DELETE), allow only if participant
        if request.method in ['PUT', 'PATCH', 'DELETE', 'POST']:
            return is_participant

        # Deny by default
        return False