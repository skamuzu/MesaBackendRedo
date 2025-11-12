# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from svix.webhooks import Webhook, WebhookVerificationError
from django.conf import settings
from rest_framework.decorators import api_view
from .models import User
import environ

CLERK_WEBHOOK_SECRET = environ.Env().get("CLERK_WEBHOOK_SECRET")


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

    if event_type == "user.created":
        User.objects.get_or_create(
            clerk_id=data["id"],
            defaults={
                "email": data["email_addresses"][0]["email_address"],
                "name": f"{data.get('first_name', '')} {data.get('last_name', '')}".strip(),
            },
        )

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
