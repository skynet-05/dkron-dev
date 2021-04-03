from django.shortcuts import render
from pydkron.client import DkronClient


# Create your views here.

def index(request):
    return render(request,"index.html")

def status(request):
    return render(request,"status.html")
def schedule(request):
    dc=DkronClient(hosts=["192.168.0.159:8080","192.168.0.152:8080",])
    if request.POST.get("pre",False)=='1':
        schedule="@at "+request.POST.get("Date",False)+"T"+request.POST.get("Time",False)+":00+05:30"
    elif request.POST.get("pre",False)=='2':
        schedule="0 0-59/"+request.POST.get('mins',False)+" * * * *"
    elif request.POST.get("pre",False)=='3':
        schedule="0 "+request.POST.get("Time",False)[3:4]+" "+request.POST.get("Time",False)[0:1]+"/"+request.POST.get("hours",False)+" * * *"
    elif request.POST.get("pre",False)=='4':
        schedule="0 "+request.POST.get("Time",False)[3:4]+" "+request.POST.get("Time",False)[0:1]+"/"+"24"+" * * *"
    elif request.POST.get("pre",False)=='5':
        schedule="0 "+request.POST.get("Time",False)[3:4]+" "+request.POST.get("Time",False)[0:1]+" * * "+request.POST.get("day_week",False)
    elif request.POST.get("pre",False)=='6':
        schedule="0 "+request.POST.get("Time",False)[3:4]+" "+request.POST.get("Time",False)[0:1]+" "+request.POST.get("day_month",False)+" * *"
    jd={
        "name":request.POST.get('jobname',False),
        "schedule":schedule,
        "tags":{
            "role":"dkron:1",
        },
        "executor":"shell",
        "executor_config":{
            "command":"python3 sendmail.py"
        }
    }
    job=dc.create_job(jd)
    job.save()
    return render(request,"dummy.html", jd)
def create(request):
    return render(request,"create.html")
