from django.shortcuts import render, HttpResponse
import requests
import ast
import urllib
import time
import simplejson
import cookielib
# from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree
import mechanize

link = {
    "groopanda": {
        "link": "http://www.groopanda.com/todos",
        "element": "li.list_item_product"
    },
    "oferta": {
        "link": "http://www.ofertadeldia.com/puerto-rico-ofertas/oferta",
        "element": "li.other-offer"
    },
    "ofertones": {
        "link": "http://www.ofertones.com/pr",
        "element": "a.js_offer"
    },
    "groupon": {
        "link": "http://www.groupon.com.pr/descuentos/local/all",
        "element": "div.deal-box"
    },
    "gustazos": {
        "link": "http://www.gustazos.com/?utm_source= \
        splashpage&utm_medium=website&utm_campaign=2012-10-SplashPageCity-PR",
        "element": "div.boxContent"
    }
}


def index(request):
    if request.GET:
        start = int(request.GET.get("start"))
        end = start + 10
        index = int(request.GET.get("index"))
        next = 0
        company_list = request.GET.get("list").split(",")

        groupon = getGroupon(start, end, index, company_list)
        length = len(groupon)
        print length
        print length is not index+1
        if length != 10 and length is not index+1:
            next = 10 - length
            index = index + 1
            start = 0
            nextGroup = getGroupon(0, next, index, company_list)
            if nextGroup:
                groupon = groupon + nextGroup

        data = {
            'start': start,
            'end': end,
            'index': index,
            "items": groupon
        }
    else:
        data = {}
    return HttpResponse(simplejson.dumps(data), content_type=
                        'application/json')


def getGroupon(start, end, index, company_list):
    company = company_list[index]
    items = []

    if company == "groopanda":
        website = link.get(company)
        response = requests.get(website.get("link"))
        d = pq(response.content)
        for item in d(website.get("element"))[start:end]:
            itemEl = d(item)
            items.append({
                'from': "groopanda",
                "title": itemEl.children(".list_item_merchant").text(),
                "text": itemEl.children(".list_item_title").text(),
                "image": itemEl.children(".list_item_image img").attr["src"],
                "link": itemEl.children(".list_item_image").attr["href"],
                "price": itemEl.find(".button_price").text(),
            })
    elif company == "oferta":
        website = link.get(company)
        response = requests.get(website.get("link"))
        d = pq(response.content)

        if start is 0:
            price = d(".price-section").find(".price").text()
            s = price.find('$')

            items.append(
                {
                    'from': "oferta",
                    "title": d(".name").text(),
                    "text":  d(".description").children("p").text(),
                    "image": d(".gallery2-holder").find("li:first").
                    children("img").attr["src"],
                    "link":  "http://www.ofertadeldia.com" +
                             d(".btn-purchase").attr["href"],
                    "price": price[s:len(price)].replace(" ", ""),
                })
            end = end-1

        for item in d(website.get("element"))[start:end]:
            itemEl = d(item)
            items.append(
                {
                    'from': "oferta",
                    "title": itemEl.find(".title").text(),
                    "text": itemEl.find(".desc").text(),
                    "image": itemEl.find(".image").children("img").attr["src"],
                    "link": "http://www.ofertadeldia.com" + itemEl.
                    find("a").attr["href"],
                    "price":  itemEl.find(".price").children(".amount").text(),
                })
    elif company == "ofertones":
        website = link.get(company)
        response = requests.get(website.get("link"))
        d = pq(response.content)

        for item in d(website.get("element"))[start:end]:
            itemEl = d(item)
            price = itemEl.find(".pagas").text()
            items.append(
                {
                    'from': "ofertones",
                    "title": itemEl.find(".desc").text(),
                    "text": "",
                    "image": "http://www.ofertones.com" + itemEl.
                    children("img").attr["src"],
                    "link": "http://www.ofertones.com" + itemEl.attr["href"],
                    "price": price[0:len(price)-5].replace(" ", "")
                })
    elif company == "gustazos":
        br = mechanize.Browser()
        website = link.get(company)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; \
            Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 \
            Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        r = br.open(website.get("link"))
        r = br.open(website.get("link"))
        html = r.read()
        d = pq(html)
        elements = d(website.get("element"))

        if start is 0:
            first = d(elements[0])
            face = d(elements[0]).find("a").attr["href"]
            if face is None:
                elements.pop(1)
            items.append(
                {
                    'from': "gustazos",
                    "title": first(".summary").children("h1").text(),
                    "text": first(".description").children("p").text(),
                    "image": first(".slideshow").find("img").attr["src"],
                    "link": "http://www.gustazos.com" + d(".summary").
                    find("a").attr["href"],
                    "price": first.find(".price").text(),
                })
            start = start + 1
            end = end - 1

        face = d(elements[1]).find("a").attr["href"]
        if face is None:
            elements.pop(1)

        for item in elements[start:end]:
            itemEl = d(item)
            title = itemEl.find(".name").text()
            price = title.find("$")
            items.append({
                'from': "gustazos",
                "title": title,
                "text": itemEl.find(".name").text(),
                "image": itemEl.find("img").attr["src"],
                "link": "http://www.gustazos.com%s" % (itemEl.
                find(".company").attr["href"]),
                "price":  title[price:price+4],
            })
    elif company == "groupon":
        br = mechanize.Browser()
        website = link.get(company)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; \
            en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 \
            Firefox/3.0.1')]
        r = br.open(website.get("link"))
        r = br.open(website.get("link"))
        html = r.read()
        d = pq(html)

        if start is 0:
            first = d(".first-deal")
            items.append({
                'from': "groupon",
                "title": first(".title").text(),
                "text": first(".description").text(),
                "image": first.find("img").attr["src"],
                "link": "http://www.groupon.com.pr%s" % (first(".title")
                .attr["href"]),
                "price": d(first.find(".price").children("span")[1]).text(),
            })
            end = end - 1

        elements = d(website.get("element"))

        for item in elements[start:end]:
            itemEl = d(item)
            try:
                prices = itemEl.find(".price").find("span")[1]
            except Exception, e:
                prices = itemEl.find(".price").find("span")[0]
            print prices
            items.append({
                'from': "groupon",
                "title": itemEl(".deal-title").text(),
                "text": itemEl(".merchant-name").text(),
                "image": itemEl.find("img").attr["src"],
                "link": "http://www.groupon.com.pr%s" % (itemEl(".title").
                attr["href"]),
                "price": d(prices).text(),
            })
    return items


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
        if(device is None):
            print "iffff"
            device = GCMDevice(name=name, registration_id=regid).save()
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
    return HttpResponse("Send!!!")
