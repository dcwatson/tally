import tally
import time

class PageTimingMiddleware (object):

    def process_request(self, request):
        setattr(request, '_tally_start_time', time.time())

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            # Don't include timing metrics for ourself, if we're installed on the same site.
            if view_func.__module__.startswith('tally'):
                delattr(request, '_tally_start_time')
        except:
            pass

    def process_response(self, request, response):
        if hasattr(request, '_tally_start_time'):
            elapsed = time.time() - request._tally_start_time
            path = 'requests.%s.%s' % (request.method.lower(), request.path.replace('/', '.').strip('.'))
            tally.tally(path, elapsed)
        return response
