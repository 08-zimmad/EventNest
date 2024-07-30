from rest_framework.permissions import BasePermission


class OrganizerPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == "organizer"
        )

    def has_object_permission(self, request, view, obj):
        return obj.organization == request.user


class AttendeePermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == "attendee"
        )

    def has_object_permission(self, request, view, obj):
        if obj.exists():
            return True
        return False
