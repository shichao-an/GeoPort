import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Group


@login_required
@require_POST
def admins(request, slug):
    """Querying admins"""
    query_type = request.POST.get("type")
    data = {
        "success": False,
        "code": 1,
        "message": "This group does not exist.",
    }
    try:
        group = Group.objects.get(slug=slug)
    except:
        return HttpResponse(json.dumps(data), content_type="application/json")

    if request.user not in group.staff:
        data["code"] = 2
        data["message"] = "Permission denied."
        return HttpResponse(json.dumps(data), content_type="application/json")

    if query_type == "get_admins":
        admins = group.admins
        data = [
            {
                "name": admin.name,
                "username": admin.username,
            }
            for admin in admins
        ]
        return HttpResponse(json.dumps(data), content_type="application/json")

    elif query_type == "add_admin":
        admin_username = request.POST.get("admin")
        try:
            admin = User.objects.get(username=admin_username)
        except:
            data["code"] = 3
            data["message"] = "This user does not exist."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        if admin == group.creator:
            data["code"] = 4
            data["message"] = "This user is already the creator of this group."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        if admin in group.admins:
            data["code"] = 5
            data["message"] = "This user is already an admin of this group."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        # Successful action
        if admin in group.regular_members:
            group.edit_member(admin, 'admin')
        else:
            group.add_member(admin, 'admin')
        data["success"] = True
        data["code"] = 0
        del data["message"]
        return HttpResponse(
            json.dumps(data), content_type="application/json")

    # `remove_admin' simply makes this user a regular member
    elif query_type == "remove_admin":
        admin_username = request.POST.get("admin")
        try:
            admin = User.objects.get(username=admin_username)
        except:
            data["code"] = 3
            data["message"] = "This user does not exist."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        if admin not in group.admins:
            data["code"] = 6
            data["message"] = "This user is not an admin of this group."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        if admin == group.creator:
            data["code"] = 7
            data["message"] = "You cannot remove creator."
            return HttpResponse(
                json.dumps(data), content_type="application/json")

        # Successful action
        group.edit_member(admin, None)
        data["success"] = True
        data["code"] = 0
        del data["message"]
        print data
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@require_POST
def join(request, slug):
    """Join a group"""
    data = {
        "success": False,
        "code": 1,
        "message": "This group does not exist.",
    }
    try:
        group = Group.objects.get(slug=slug)
    except:
        return HttpResponse(json.dumps(data), content_type="application/json")

    if request.user in group.staff:
        data["code"] = 2
        data["message"] = "You cannot join your created/moderated group."
        return HttpResponse(json.dumps(data), content_type="application/json")

    group.add_member(request.user)
    data["code"] = 0
    data["success"] = True
    del data["message"]
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@require_POST
def quit(request, slug):
    """Quit a group"""
    data = {
        "success": False,
        "code": 1,
        "message": "This group does not exist.",
    }

    try:
        group = Group.objects.get(slug=slug)
    except:
        return HttpResponse(json.dumps(data), content_type="application/json")

    if request.user in group.staff:
        data["code"] = 3
        data["message"] = "You cannot quit your created/moderated group."
        return HttpResponse(json.dumps(data), content_type="application/json")

    if request.user not in group.regular_members:
        data["code"] = 4
        data["message"] = "You haven't joined this group yet."
        return HttpResponse(json.dumps(data), content_type="application/json")

    group.remove_member(request.user)
    data["code"] = 0
    data["success"] = True
    del data["message"]
    return HttpResponse(json.dumps(data), content_type="application/json")
