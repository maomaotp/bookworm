from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse

def index(request):
    if request.method == 'GET':
        responseData = {
            "errcode": -1,
            "errmsg": "error",
        }

        return JsonResponse(responseData)
    elif request.method == 'POST':
        auth_login(request)


def auth_login(request):
    """
    user login
    """
    try:
        params = request.POST
        username = params['username']
        password = params["password"]
        #user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                csrf_token = request.META["CSRF_COOKIE"]
                serializer = UserSerializer(user)
                data = serializer.data
                data.update({
                    "csrf_token":csrf_token,
                })
            else:
                responseData = {
                    "errcode": -1,
                    "errmsg": "error",
                }

                return JsonResponse(responseData)
        else:
            return HttpResponse(e)

    except Exception as e:
        return HttpResponse(e)

    return HttpResponse("Hello,user .")
