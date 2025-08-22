import json,socket,time,sys,configparser,psutil,requests
from datetime import datetime,timezone
from pathlib import Path

def _here():
    return Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).parent

def load_config():
    cfg=configparser.ConfigParser()
    cfg.read(_here()/ "config.ini")
    return cfg.get("agent","endpoint"), cfg.get("agent","api_key")

def collect_processes():
    procs=[]; [p.cpu_percent(None) for p in psutil.process_iter(['pid'])]; time.sleep(0.2)
    for p in psutil.process_iter(['pid','ppid','name','username','cmdline']):
        try:
            d=p.as_dict(attrs=['pid','ppid','name','username','cmdline'])
            d.update(cpu=round(p.cpu_percent(None),2), mem_mb=round(p.memory_info().rss/(1024*1024),2), cmdline=" ".join(d.get("cmdline") or []))
            procs.append(d)
        except: continue
    return procs

def main():
    endpoint,api_key=load_config(); hostname=socket.gethostname()
    payload={"hostname":hostname,"timestamp":datetime.now(timezone.utc).isoformat(),"processes":collect_processes()}
    r=requests.post(endpoint,json=payload,headers={"X-API-KEY":api_key},timeout=15); r.raise_for_status()
    print("Uploaded snapshot:",r.json())

if __name__=="__main__":
    try: main()
    except Exception as e: print("Agent error:",e); sys.exit(1)
