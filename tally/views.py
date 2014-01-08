from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from tally.models import Archive
import json

def values(request, slug):
    archive = get_object_or_404(Archive, slug=slug)
    data = archive.values()
    return HttpResponse(json.dumps(data, indent=2), content_type='application/json')
