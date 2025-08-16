import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django.request')

class LogRequestHeadersMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info('Request Headers: %s', dict(request.headers))
        return None
