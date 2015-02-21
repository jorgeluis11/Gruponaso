from django.shortcuts import render, HttpResponse
import requests, ast, urllib, time, simplejson
# from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree



link = [["groopanda","http://www.groopanda.com/todos","li.list_item_product"],
		["oferta","http://www.ofertadeldia.com/puerto-rico-ofertas/oferta","li.other-offer"],
		["ofertones","http://www.ofertones.com/pr","a.js_offer"]]

link = {
	"groopanda":{
		"link"    : "http://www.groopanda.com/todos",
		"element" : "li.list_item_product"
	},
	"oferta":{
		"link"   : "http://www.ofertadeldia.com/puerto-rico-ofertas/oferta",
		"element": "li.other-offer"
	},
	"ofertones":{
		"link"   : "http://www.ofertones.com/pr",
		"element": "a.js_offer"
	}
}
def index(request):
	if request.GET:
		start = int(request.GET.get("start"))
		end = start + 10
		index = int(request.GET.get("index"))
		next  = 0
		company_list = request.GET.get("list").split(",")

		groupon = getGroupon(start, end, index, company_list)
		length = len(groupon)
		print length is not index+1
		if length != 10 and length is not index+1:
			next  = 10 - length
			index = index + 1
			start = 0
			
			nextGroup = getGroupon(0, next, index, company_list)
			if nextGroup:
				groupon = groupon + nextGroup

		data = {
			'start' : start,
			'end'   : end,
			'index' : index,
			"items" : groupon
		}
	else:
		data = {}

	#data = {
	#	"text"  : "text",
	#	"images": [d(item).attr["src"] for item in d("ul.list_products").find("img")],
	#	"links" : [d(item).attr["href"] for item in d("ul.list_products").find("a")]
	#}
	#print d(".list_products").find(".list_item_image")
	return HttpResponse(simplejson.dumps(data), content_type='application/json')

def getGroupon(start,end,index, company_list):
	company = company_list[index]
	items = []

	if company == "groopanda":
		
		website = link.get(company)
		response = requests.get(website.get("link"))
		print website
		d = pq(response.content)
		for item in d(website.get("element"))[start:end]:
			itemEl = d(item)
			items.append({
				'from' : "groopanda",
				"title": itemEl.children(".list_item_merchant").text() ,
				"text" : itemEl.children(".list_item_title").text(),
				"image": itemEl.children(".list_item_image img").attr["src"],
				"link" : itemEl.children(".list_item_image").attr["href"], 
			})
	elif company == "oferta":
		website = link.get(company)
		response = requests.get(website.get("link"))
		d = pq(response.content)

		if start is 0:
			items.append({
				'from' : "oferta",
				"title": d(".name").text() ,
				"text" : d(".description").children("p").text(),
				"image": d(".gallery2-holder").find("li:first").children("img").attr["src"] ,
				"link" : "http://www.ofertadeldia.com" + d(".btn-purchase").attr["href"] ,
			})
			end = end-1
			print items
			
		for item in d(website.get("element"))[start:end]:
			itemEl = d(item)
			items.append({
				'from' : "oferta",
				"title": itemEl.find(".title").text() ,
				"text" : itemEl.find(".desc").text(),
				"image": itemEl.find(".image").children("img").attr["src"],
				"link" : "http://www.ofertadeldia.com" + itemEl.find("a").attr["href"], 
			})
	elif company == "ofertones":
		website = link.get(company)
		response = requests.get(website.get("link"))
		d = pq(response.content)

		for item in d(website.get("element"))[start:end]:
			itemEl = d(item)
			items.append({
				'from' : "ofertones",
				"title": itemEl.find(".desc").text() ,
				"text" : itemEl.find(".pagas").text(),
				"image": "http://www.ofertones.com" + itemEl.children("img").attr["src"],
				"link" : "http://www.ofertones.com" + itemEl.attr["href"], 
			})
	return items 

#use Later
#response = requests.get(link)
#			d2 = pq(response.content)
#							'phone': d2(".product_fine_print").text(),


def my_print(x):
    print x

def groopanda():
	d = pq(url="http://www.groopanda.com/todos", parser="html")
	x = d(".list_products").html()
	return x

from push_notifications.models import APNSDevice, GCMDevice

def registration(request):
	if request.GET:
		name = request.GET.get("name")
		regid = request.GET.get("regID")
		print regid
		try:
			device = GCMDevice.objects.get(registration_id=regid)
		except GCMDevice.DoesNotExist:
			device = None
		if(device == None):
			print "iffff"
			device = GCMDevice(name=name, registration_id=regid).save()
			# The first argument will be sent as "message" to the intent extras Bundle
			# Retrieve it with intent.getExtras().getString("message")
			print "stored"
			return HttpResponse("Si Guardo!!!!!")
		else:
			return HttpResponse("Existe!")
		
	return HttpResponse("Stored!!!")

def pushExample(request):
	if request.GET:
		regid = request.GET.get("regID")
		try:
			device = GCMDevice.objects.get(registration_id=regid)
			time.sleep(10)
			device.send_message("Weeeepaleee")
			print "mail send"
			return HttpResponse("Sendend")
		except GCMDevice.DoesNotExist:
			device = None
			return HttpResponse("Push not send")
 
		# The first argument will be sent as "message" to the intent extras Bundle
		# Retrieve it with intent.getExtras().getString("message")
		
	return HttpResponse("Send!!!")

def pushInstant(request):
	if request.GET:
		regid = request.GET.get("regID")
		try:
			device = GCMDevice.objects.get(registration_id=regid)
			device.send_message("Weeeepaleee")
			print "mail send"
			return HttpResponse("Sendend")
		except GCMDevice.DoesNotExist:
			device = None
			return HttpResponse("Push not send")
 
		# The first argument will be sent as "message" to the intent extras Bundle
		# Retrieve it with intent.getExtras().getString("message")
		
	return HttpResponse("Send!!!")
#index("a")