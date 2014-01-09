from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from tally.models import Archive
import json

def dashboard(request):
    return render(request, 'tally/dashboard.html', {
        'archives': Archive.objects.all(),
    })

def archives(request):
    data = []
    for a in Archive.objects.all():
        info = {f: getattr(a, f) for f in ('name', 'slug', 'pattern', 'resolution', 'retention', 'enabled')}
        info['values_url'] = reverse('tally-values', kwargs={'slug': a.slug})
        info['aggregate_url'] = reverse('tally-aggregate', kwargs={'slug': a.slug})
        data.append(info)
    json_kwargs = {}
    if 'pretty' in request.GET:
        json_kwargs['indent'] = 2
    return HttpResponse(json.dumps(data, **json_kwargs), content_type='application/json')

def data(request, slug, method=None, aggregate=None, by='time'):
    archive = get_object_or_404(Archive, slug=slug)
    data_func = getattr(archive, method)
    q = request.GET.get('q')
    since = int(request.GET['since']) if 'since' in request.GET else None
    until = int(request.GET['until']) if 'until' in request.GET else None
    data = data_func(pattern=q, aggregate=aggregate, by=by, since=since, until=until)
    json_kwargs = {}
    if 'pretty' in request.GET:
        json_kwargs['indent'] = 2
    return HttpResponse(json.dumps(data, **json_kwargs), content_type='application/json')
