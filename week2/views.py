
# Create your views here.
import json

from django.http import JsonResponse
from django.shortcuts import render

from .ai import get_reply


def chat_api(request):
    """Browser se message leta hai aur AI ka jawab wapas bhejta hai."""
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body)
    user_message = data.get("message", "").strip()

    if not user_message:
        return JsonResponse({"error": "Message khaali hai"}, status=400)

    try:
        reply = get_reply(user_message)
        return JsonResponse({"reply": reply})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
