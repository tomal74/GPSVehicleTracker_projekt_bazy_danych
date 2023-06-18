from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Trips
import urllib

def index(request):
    all_trips = Trips.objects.all().values()
    
    template = loader.get_template('index.html')
    
    uri_path = urllib.parse.quote('', safe='')  
    
    context = {
      'mytrip':    uri_path,
      'all_trips': all_trips,
    }
    
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def index_no(request, id):
    trip = Trips.objects.get(id=id)
    all_trips = Trips.objects.all().values()
    
    template = loader.get_template('index.html')
    uri_path = urllib.parse.quote(trip.gpx_files, safe='')  
    
    context = {
      'mymember': trip,
      'mytrip':   uri_path,
      'all_trips': all_trips,
    }
    
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))



def index_redirect(request):
    return HttpResponseRedirect('/index.html/')
  


  
# Create your views here.

