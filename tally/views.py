from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from tally.models import Archive
import json

def archives(request):
    data = []
    for a in Archive.objects.all():
        info = {f: getattr(a, f) for f in ('name', 'slug', 'pattern', 'resolution', 'retention')}
        info['url'] = a.get_absolute_url()
        data.append(info)
    json_kwargs = {}
    if 'pretty' in request.GET:
        json_kwargs['indent'] = 2
    return HttpResponse(json.dumps(data, **json_kwargs), content_type='application/json')

def archive(request, slug, aggregate=None, by='time'):
    archive = get_object_or_404(Archive, slug=slug)
    q = request.GET.get('q')
    since = int(request.GET['since']) if 'since' in request.GET else None
    until = int(request.GET['until']) if 'until' in request.GET else None
    data = archive.values(pattern=q, aggregate=aggregate, by=by, since=since, until=until)
    json_kwargs = {}
    if 'pretty' in request.GET:
        json_kwargs['indent'] = 2
    return HttpResponse(json.dumps(data, **json_kwargs), content_type='application/json')
