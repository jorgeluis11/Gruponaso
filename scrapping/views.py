from django.shortcuts import render, HttpResponse
import requests
# from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree
import urllib
 

def index(request):
	d = pq(url="http://www.groopanda.com/todos", parser="html")
	x = d(".list_products").html()
	print x
	return render(request, "index.html", {"products":x})

def groopanda():
	d = pq(url="http://www.groopanda.com/todos", parser="html")
	x = d(".list_products").html()
	return x

from push_notifications.models import APNSDevice, GCMDevice

def registration(request):
	if request.GET:
		name = request.GET.get("name")
		gmc_reg_id = request.GET.get("regID")
		device = GCMDevice(name=name, registration_id=gmc_reg_id).save()
		# The first argument will be sent as "message" to the intent extras Bundle
		# Retrieve it with intent.getExtras().getString("message")
		print "stored"
	return HttpResponse("Stored!!!")

def pushExample(request):
	if request.GET:
		gcm_reg_id = request.GET.get("registration_id")
		device = GCMDevice.objects.get(registration_id=gcm_reg_id)
		# The first argument will be sent as "message" to the intent extras Bundle
		# Retrieve it with intent.getExtras().getString("message")
		device.send_message("Weeeepaleee")
		print "mail send"
	return HttpResponse("Send!!!")
#index("a")