from rest_framework.permissions import BasePermission


class isOrganizer(BasePermission):
    def has_object_permissions(self, request, view, obj):
        return obj.organization==request.user