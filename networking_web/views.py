from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from pytz import UTC

from networking_base.models import Contact, Touchpoint


def index(request):
    contacts = Contact.objects.prefetch_related("touchpoint_set").all()
    contacts_by_urgency = sorted(contacts, key=lambda c: c.get_urgency(), reverse=True)
    return render(request, "web/index.html", {"contacts": contacts_by_urgency})


def add_touchpoint(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)
    Touchpoint.objects.create(when=datetime.now(tz=UTC), contact=contact)
    referer = request.META.get("HTTP_REFERER")
    return HttpResponseRedirect(referer)