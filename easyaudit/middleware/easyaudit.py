try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # not required in <= 1.9
    MiddlewareMixin = object

# makes easy-audit thread-safe
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, 'user', None)

class EasyAuditMiddleware(MiddlewareMixin):
    """Makes request available to this app signals."""
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        return self.get_response(request)

    def process_request(self, request):
        _thread_locals.request = request
        return None

    def process_response(self, request, response):
        try:
            del _thread_locals.request
        except AttributeError:
            pass
        return response

    def process_exception(self, request, exception):
        try:
            del _thread_locals.request
        except AttributeError:
            pass
        return None
