import random
from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    message = {"status": False, "msg": "无权访问"}

    def has_permission(self, request, view):
        v1 = random.randint(1, 3)
        if v1 == 2:
            return True
        return False
