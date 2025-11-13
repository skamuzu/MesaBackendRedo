# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from svix.webhooks import Webhook, WebhookVerificationError
from django.conf import settings
from rest_framework.decorators import api_view
from .models import User
from actstream import action




@csrf_exempt
@api_view(["POST"])
def clerk_webhook(request):

    payload = request.body
    headers = request.headers

    try:
        # Verify webhook signature (important!)
        webhook = Webhook(settings.CLERK_WEBHOOK_SECRET)
        event = webhook.verify(payload, headers)
    except WebhookVerificationError:
        return HttpResponse("Invalid signature", status=400)

    event_type = event["type"]
    data = event["data"]
    
    if len(data["email_addresses"]) == 0:
        email = None
    else:
        email =  data["email_addresses"][0]["email_address"]

    if event_type == "user.created":
        user, created = User.objects.get_or_create(
            clerk_id=data["id"],
            defaults={
                "email": email,
                "first_name": data.get("first_name"),
                "last_name":data.get("last_name")
            },
        )
        if created:
            action.send(user, verb="just joined the platform")

    elif event_type == "user.updated":
        try:
            user = User.objects.get(clerk_id=data["id"])
            user.email = data["email_addresses"][0]["email_address"]
            user.name = (
                f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
            )
            user.save()
        except User.DoesNotExist:
            pass

    elif event_type == "user.deleted":
        User.objects.filter(clerk_id=data["id"]).delete()

    return HttpResponse(status=200)
