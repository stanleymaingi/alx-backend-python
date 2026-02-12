from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Allows access only to participants of a conversation or message.
    Checks authentication and HTTP methods for unsafe operations.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Unsafe HTTP methods
        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Conversation object
            if hasattr(obj, "participants"):
                return obj.participants.filter(id=request.user.id).exists()
            # Message object
            if hasattr(obj, "conversation"):
                return obj.conversation.participants.filter(id=request.user.id).exists()

        # Safe methods (GET, HEAD, OPTIONS)
        return True
