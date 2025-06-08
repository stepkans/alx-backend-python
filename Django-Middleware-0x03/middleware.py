import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict
from django.http import HttpResponseTooManyRequests

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        return self.get_response(request)
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Only allow access between 18:00 (6 PM) and 21:00 (9 PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to the messaging app is restricted at this time.")

        return self.get_response(request)    
 
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = defaultdict(list)  # {ip: [timestamp1, timestamp2, ...]}
        self.message_limit = 5  # messages
        self.time_window = 60  # seconds

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chats/'):
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Remove timestamps older than time_window
            self.ip_message_log[ip] = [
                ts for ts in self.ip_message_log[ip]
                if current_time - ts < self.time_window
            ]

            if len(self.ip_message_log[ip]) >= self.message_limit:
                return HttpResponseTooManyRequests("Rate limit exceeded. Only 5 messages allowed per minute.")

            self.ip_message_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip    
