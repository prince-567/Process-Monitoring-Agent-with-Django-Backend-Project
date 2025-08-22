from django.db import models
from django.utils import timezone
import secrets

def generate_api_key():
    return secrets.token_hex(16)

class Agent(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=64, unique=True, default=generate_api_key)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hostname

class Snapshot(models.Model):
    hostname = models.CharField(max_length=255)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

class Process(models.Model):
    snapshot = models.ForeignKey(Snapshot, related_name="processes", on_delete=models.CASCADE)
    pid = models.IntegerField()
    ppid = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    cpu = models.FloatField(null=True, blank=True)
    mem_mb = models.FloatField(null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    cmdline = models.TextField(null=True, blank=True)
