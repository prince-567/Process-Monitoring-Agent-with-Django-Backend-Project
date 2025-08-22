from rest_framework import serializers
from .models import Snapshot, Process

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ("pid","ppid","name","cpu","mem_mb","username","cmdline")

class SnapshotSerializer(serializers.ModelSerializer):
    processes = ProcessSerializer(many=True)
    class Meta:
        model = Snapshot
        fields = ("id","hostname","created_at","processes")
