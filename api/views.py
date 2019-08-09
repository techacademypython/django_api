from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate
from api.models import News
import json
from api.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

User = get_user_model()


# Create your views here.
@csrf_exempt
def main_index(request):
    if request.method == "GET":
        return JsonResponse({
            "status": "OK"
        })
    else:
        return JsonResponse({
            "type_of_request": request.method
        })


@csrf_exempt
def api_main_news(request):
    if request.method == "GET":
        news_list = News.objects.all()
        arr = []
        for news in news_list:
            arr.append({
                "title": news.title,
                "content": news.content
            })
        return JsonResponse(arr, safe=False)
    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        if "title" in data and "content" in data:
            news = News.objects.create(
                title=data.get("title"),
                content=data.get("content")
            )
            return JsonResponse({
                "id": news.id,
                "title": news.title,
                "content": news.content
            }, status=201)


@csrf_exempt
def api_news_update(request, id):
    news = News.objects.filter(id=id).last()
    if news:
        if request.method == "GET":
            return JsonResponse({
                "id": news.id,
                "title": news.title,
                "content": news.content
            })

        elif request.method == "PUT":
            data = json.loads(request.body.decode("utf-8"))
            news.title = data.get("title", news.title)
            news.content = data.get("content", news.content)
            news.save()
            return JsonResponse({
                "id": news.id,
                "title": news.title,
                "content": news.content
            }, status=201)
        elif request.method == "DELETE":
            old_news = news
            news.delete()
            return JsonResponse({
                "id": old_news.id,
                "title": old_news.title,
                "content": old_news.content
            })
    else:
        return JsonResponse({
            "message": "Not found news"
        })


class LoginApi(APIView):
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )
        if user:
            if user.is_active:
                return JsonResponse({
                    "token": user.auth_token.key
                })
            else:
                return JsonResponse({
                    "message": "User is not active"
                })
        else:
            return JsonResponse({
                "message": "Invalid credentials"
            })


class RegsiterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"]
        )
        serializer = UserSerializer(user)
        return JsonResponse({
            "status": "Created",
            "token": user.auth_token.key,
            "data": serializer.data
        }, status=201)


class PrivateApi(APIView):

    def get(self, *args, **kwargs):
        return JsonResponse({
            "message": "Siz artiq login olmusuz",
            "username": self.request.user.username
        })
