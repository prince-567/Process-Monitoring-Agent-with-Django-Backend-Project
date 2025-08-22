from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import Agent

class ApiKeyAuthentication(BaseAuthentication):
    keyword = "X-API-KEY"
    def authenticate(self, request):
        key = request.headers.get(self.keyword)
        if not key: return None
        try:
            agent = Agent.objects.get(api_key=key)
            return (agent, None)
        except Agent.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid API key")
