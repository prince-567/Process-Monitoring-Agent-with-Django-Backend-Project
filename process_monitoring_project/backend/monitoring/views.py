from collections import defaultdict
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Snapshot, Process, Agent
from .auth import ApiKeyAuthentication

# Home view: renders the HTML frontend
def home(request):
    return render(request, "index.html")

# Returns the list of hostnames
@api_view(["GET"])
def hosts(request):
    return Response({
        "hosts": list(Snapshot.objects.values_list("hostname", flat=True).distinct())
    })

# Returns the latest process tree for a host
@api_view(["GET"])
def latest(request):
    hostname = request.GET.get("hostname")
    qs = Snapshot.objects.all()
    if hostname:
        qs = qs.filter(hostname=hostname)
    snap = qs.order_by("-created_at").first()

    if not snap:
        return Response({
            "detail": "No data yet",
            "tree": [],
            "hostname": hostname,
            "timestamp": None
        })

    rows = list(snap.processes.values("pid", "ppid", "name", "cpu", "mem_mb", "username", "cmdline"))

    # Build process tree
    by_ppid, by_pid = defaultdict(list), {}
    for r in rows:
        r["children"] = []
        by_ppid[r["ppid"]].append(r)
        by_pid[r["pid"]] = r

    roots = []
    for r in rows:
        parent = by_pid.get(r["ppid"])
        if parent:
            parent["children"].append(r)
        else:
            roots.append(r)

    return Response({
        "hostname": snap.hostname,
        "timestamp": snap.created_at.isoformat(),
        "tree": roots
    })

# Accepts new data from agents and stores in database
@api_view(["POST"])
@authentication_classes([ApiKeyAuthentication])
@permission_classes([AllowAny])
def ingest(request):
    if not isinstance(request.user, Agent):
        return Response({"detail": "Invalid API key"}, status=401)

    data = request.data
    hostname = data.get("hostname")
    processes = data.get("processes", [])

    if not hostname or not isinstance(processes, list):
        return Response({"detail": "hostname and processes required"}, status=400)

    snap = Snapshot.objects.create(hostname=hostname, agent=request.user)
    objs = [
        Process(snapshot=snap, **{k: v for k, v in p.items() if k in [
            "pid", "ppid", "name", "cpu", "mem_mb", "username", "cmdline"
        ]}) for p in processes
    ]
    Process.objects.bulk_create(objs, batch_size=1000)

    return Response({"status": "ok", "snapshot_id": snap.id})
