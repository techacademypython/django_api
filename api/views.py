from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import News
import json


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


