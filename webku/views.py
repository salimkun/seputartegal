# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, TemplateView
from django.views.generic import ListView
from django.http import HttpResponse
from hitcount.views import HitCountDetailView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.core.mail import send_mail, BadHeaderError

from webku import forms
from django.contrib.gis import geos
from django.contrib.gis import measure
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis import measure
from pure_pagination.mixins import PaginationMixin
from django.views import generic
import requests, json

requests.packages.urllib3.disable_warnings()

class PostMixinDetailView(object):
    model = Informasi
    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)
        """ id = 1 """		
		
        context['info'] = Informasi.objects.filter(key__kategori__in=["wisata air","wisata alam","wisata alternatif","wisata budaya","wisata edukasi",
			"wisata kuliner","wisata religi","wisata sejarah","wisata ziarah","public area"], status='p').order_by('-date')[:3]
        context['info_dua'] = Informasi.objects.filter(~Q(key__kategori__in=["wisata air","wisata alam","wisata alternatif"])).order_by('-date')[:3]
        context['belanja'] = Informasi.objects.filter(key__kategori__in=["tempat belanja"], status='p').order_by('-date')[:5]
        context['akomodasi'] = Informasi.objects.filter(key__kategori__in=["akomodasi"], status='p').order_by('-date')[:5]	
        context['transport'] = Informasi.objects.filter(key__kategori__in=["transportasi"], status='p').order_by('-date')[:5]		
        context['tips'] = Informasi.objects.filter(key__kategori__in=["tips wisata"], status='p').order_by('-date')[:5]			
        context['budaya'] = Informasi.objects.filter(key__kategori__in=["budaya"], status='p').order_by('-date')[:5]
        context['wisata'] = Informasi.objects.filter(key__kategori__in=["wisata air","wisata alam","wisata alternatif","wisata budaya","wisata edukasi",
			"wisata kuliner","wisata religi","wisata sejarah","wisata ziarah","public area"], status='p').order_by('-date')
        context['kuliner'] = Informasi.objects.filter(key__kategori__in=["tempat kuliner"], status='p').order_by('-date')[:5]
 
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]
        context['testimon'] = Testimonial.objects.order_by('-date')[:6]
        context['item'] = Vidio.objects.order_by('-date')[:6]	
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class IndexView(PostMixinDetailView, TemplateView):
    template_name = 'index.html'

class PostDetailJSONView(PostMixinDetailView, DetailView):
    template_name = 'detail.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PostDetailJSONView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)
    count_hit = True
	
	

class DetailView(generic.DetailView):
    template_name = 'detail.html'
    model = Informasi
	
    def api_view(self, location):
        requests.packages.urllib3.disable_warnings()
        url  = 'https://api.tripadvisor.com/api/partner/2.0/map/{}/hotels?key=4c3f4e7957b444ce9ffa0d9b420fab8b&distance=10ss.03'.format(location)
        resp = requests.get(url=url)
        data = json.loads(resp.text)
 
        return data
		
    def api1_view(self, location):
        requests.packages.urllib3.disable_warnings()
        url  = 'https://api.tripadvisor.com/api/partner/2.0/map/{}/attractions?key=4c3f4e7957b444ce9ffa0d9b420fab8b&distance=10.03'.format(location)
        resp = requests.get(url=url)
        data1 = json.loads(resp.text)
 
        return data1

    def api2_view(self, location):
        requests.packages.urllib3.disable_warnings()
        url  = 'https://api.tripadvisor.com/api/partner/2.0/map/{}/restaurants?key=4c3f4e7957b444ce9ffa0d9b420fab8b&distance=10.03'.format(location)
        resp = requests.get(url=url)
        data2 = json.loads(resp.text)
 
        return data2
		
    def api3_view(self, title):
        requests.packages.urllib3.disable_warnings()
        url  = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyDOntlUJpq21wPpALcwgARqk5fg_jYL-wo&cx=002636883463055877544:gc6qpludt7m&q={}&filter=0&searchType=image&alt=json'.format(title)
        resp = requests.get(url=url)
        data3 = json.loads(resp.text)
 
        return data3
		
 
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['data_json'] = self.api_view(self.object.location)
        context['data_json1'] = self.api1_view(self.object.location)
        context['data_json2'] = self.api2_view(self.object.location)
        context['data_json3'] = self.api3_view(self.object.title)
        context['twc'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.0067019*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.0067019*pi()/180))'
			'* cos((`Latitude`*pi()/180)) * cos(((109.1836086- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (1, 14, 17,18, 20, 21) HAVING distance ORDER BY distance ASC ')[:5]
        """ distance hotel """	
        context['twc1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.0067019*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.0067019*pi()/180))'
			'* cos((`Latitude`*pi()/180)) * cos(((109.1836086- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC ')[:5]
        """ distance lain """
        context['twc2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.0067019*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.0067019*pi()/180))'
			'* cos((`Latitude`*pi()/180)) * cos(((109.1836086- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC ')[:5]
			
        """ id = 2 """
        context['cp'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.19032738456*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.19032738456*pi()/180)) '
			'* cos((`Latitude`*pi()/180)) * cos(((109.160307024- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (2, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC ')[:5]
        context['cp1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.19032738456*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.19032738456*pi()/180)) '
			'* cos((`Latitude`*pi()/180)) * cos(((109.160307024- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC ')[:5]
        context['cp2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.19032738456*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.19032738456*pi()/180)) '
			'* cos((`Latitude`*pi()/180)) * cos(((109.160307024- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC ')[:5]
			
        """ id = 3 """			
        context['pball'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.207275*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.207275*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.165936- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (3, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC ')[:5]
        context['pball1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.207275*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.207275*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.165936- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC ')[:5]
        context['pball2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.207275*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.207275*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.165936- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC ')[:5]
			
        """ id = 4 """
        context['kwis'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.850536*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.850536*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.142247- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (4, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['kwis1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.850536*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.850536*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.142247- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['kwis2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.850536*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.850536*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.142247- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
			
        """ id = 5 """
        context['musek'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.973476*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.973476*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.139983- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (5, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['musek1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.973476*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.973476*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.139983- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['musek2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.973476*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.973476*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.139983- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
			
        """ id = 6 """
        context['paseng'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.866570*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.866570*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.137127- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (6, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['paseng1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.866570*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.866570*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.137127- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['paseng2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.866570*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.866570*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.137127- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
			
        """ id = 7 """
        context['langpes'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.856322*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.856322*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.134257- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (7, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['langpes1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.856322*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.856322*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.134257- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['langpes2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.856322*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.856322*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.134257- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]

        """ id = 8 """
        context['scs'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.867350*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.867350*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.142786- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (8, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['scs1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.867350*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.867350*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.142786- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['scs2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.867350*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.867350*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.142786- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
			
        """ id = 9 """	
        context['mkgsb'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.074257*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.074257*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.133525- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (9, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['mkgsb1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.074257*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.074257*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.133525- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['mkgsb2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.074257*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.074257*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.133525- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]

        """ id = 10 """			
        context['aat'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.867446*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.867446*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.137861- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (10, 14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['aat1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.867446*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.867446*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.137861- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['aat2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.867446*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.867446*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.137861- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]

        """ id = 14 """				
        context['sankita'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.1908552*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.1908552*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1554631- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['sankita1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.1908552*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.1908552*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1554631- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (17) HAVING distance ORDER BY distance ASC')[:5]
        context['sankita2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-7.1908552*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-7.1908552*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1554631- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
		
        """ id = 17 """		
        context['rpalace'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8641746*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8641746*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.132218- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (14, 17, 18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['rpalace1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8641746*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8641746*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.132218- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14) HAVING distance ORDER BY distance ASC')[:5]
        context['rpalace2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8641746*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8641746*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.132218- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
			
        """ id = 18 """		
        context['ceria'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.99067*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.99067*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1649759- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (18, 14, 17, 20, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['ceria1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.99067*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.99067*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1649759- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['ceria2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.99067*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.99067*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1649759- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (20, 21) HAVING distance ORDER BY distance ASC')[:5]
			
        """ id = 20 """		
        context['sstrawberry'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8668117*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8668117*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1340219- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (20, 14, 17, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['sstrawberry1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8668117*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8668117*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1649759- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['sstrawberry2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8668117*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8668117*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1649759- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 21) HAVING distance ORDER BY distance ASC')[:5]
			
        """ id = 21 """		
        context['bigberry'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8824622*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8824622*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1347744- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE NOT id IN (20, 14, 17, 21) HAVING distance ORDER BY distance ASC')[:5]
        context['bigberry1'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8824622*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8824622*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1347744- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (14, 17) HAVING distance ORDER BY distance ASC')[:5]
        context['bigberry2'] = Informasi.objects.raw('SELECT id,(((acos(sin((-6.8824622*pi()/180)) * sin((`Latitude`*pi()/180))+cos((-6.8824622*pi()/180))' 
			'* cos((`Latitude`*pi()/180)) * cos(((109.1347744- `Longitude`)* pi()/180))))*180/pi())*60*1.1515 )*1.609344 as distance FROM `webku_informasi`' 
			'WHERE id IN (18, 20) HAVING distance ORDER BY distance ASC')[:5]
        return context

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(DetailView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)
    count_hit = True
	

    """
    Generic hitcount class based view.
    """
    pass
    

class PostCountHitDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True

class DaftarView(PostMixinDetailView, TemplateView):
    template_name = 'daftar.html'
    def judul(request):
        return {"today": today}
    def get_context_data(self, **kwargs):
        context = super(DaftarView, self).get_context_data(**kwargs)
        context['tags'] = Keywords.objects.order_by('-kategori')
        context['feed'] = Berita.objects.order_by('-pub_date')[:5]
        return context

class BudayaView(ListView):
    paginate_by = 5
    template_name = 'budaya.html'
    model = "Informasi"
    context_object_name = 'budaya'
    queryset = Informasi.objects.filter(key__kategori__in=["budaya"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(BudayaView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context

class TransportView(ListView):
    paginate_by = 5
    template_name = 'transport.html'
    model = "Informasi"
    context_object_name = 'transport'
    queryset = Informasi.objects.filter(key__kategori__in=["transportasi"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(TransportView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context

class AkomodasiView(ListView):
    paginate_by = 5
    template_name = 'akomodasi.html'
    model = "Informasi"
    queryset = Informasi.objects.filter(key__kategori__in=["akomodasi"],status='p').order_by('-date')
    context_object_name = 'akomodasi'
    def get_context_data(self, **kwargs):
        context = super(AkomodasiView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class KulinerView(ListView):
    paginate_by = 5
    template_name = 'kuliner.html'
    model = "Informasi"
    queryset = Informasi.objects.filter(key__kategori__in=["kuliner"],status='p').order_by('-date')
    context_object_name = 'kuliner'
    def get_context_data(self, **kwargs):
        context = super(KulinerView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context

		
class WisataView(ListView):		
    paginate_by = 5
    template_name = 'wisata.html'
    model = "Informasi"
    context_object_name = 'wisata'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata air","wisata alam","wisata alternatif","wisata budaya","wisata edukasi",
		"wisata kuliner","wisata religi","wisata sejarah","wisata ziarah","public area"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WisataView, self).get_context_data(**kwargs)
        context['tags'] = Keywords.objects.order_by('-kategori')
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]
        return context
	
class BeritaView(PostMixinDetailView, TemplateView):
	template_name = 'berita.html'		
	model = "Keywords"
	def get_context_data(self, **kwargs):
		context = super(BeritaView, self).get_context_data(**kwargs)
		context['tags'] = Keywords.objects.order_by('-kategori')
		return context

class WairView(ListView):
    template_name = 'tags/wisataair.html'		
    paginate_by = 5
    model = "Informasi"
    context_object_name = 'wair'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata air"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WairView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
	
	def search_form(request):
		return render(request)

class WziarahView(ListView):
    paginate_by = 5
    template_name = 'tags/wisataziarah.html'
    model = "Informasi"
    context_object_name = 'ziarah'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata ziarah"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WziarahView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class WsejarahView(ListView):
    paginate_by = 5
    template_name = 'tags/wisatasejarah.html'
    model = "Informasi"
    context_object_name = 'sejarah'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata sejarah"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WsejarahView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context

class WreligiView(ListView):
    paginate_by = 5
    template_name = 'tags/wisatareligi.html'
    model = "Informasi"
    context_object_name = 'religi'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata religi"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WreligiView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class WkulinerView(ListView):
    paginate_by = 5
    template_name = 'tags/wisatakuliner.html'
    model = "Informasi"
    context_object_name = 'wiskul'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata kuliner"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WkulinerView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class WedukasiView(ListView):
    paginate_by = 5
    template_name = 'tags/wisataedukasi.html'
    model = "Informasi"
    context_object_name = 'edukasi'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata edukasi"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WedukasiView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
	
class WbudayaView(ListView):
    paginate_by = 5
    template_name = 'tags/wisatabudaya.html'
    model = "Informasi"
    context_object_name = 'wisbud'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata budaya"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WbudayaView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class WalternatifView(ListView):
    paginate_by = 5
    template_name = 'tags/wisataalternatif.html'
    model = "Informasi"
    context_object_name = 'alternatif'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata alternatif"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WalternatifView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class WalamView(ListView):
    paginate_by = 5
    template_name = 'tags/wisataalam.html'
    model = "Informasi"
    context_object_name = 'alam'
    queryset = Informasi.objects.filter(key__kategori__in=["wisata alam"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(WalamView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
	
class PublicareaView(ListView):
    paginate_by = 5
    template_name = 'tags/publicarea.html'
    model = "Informasi"
    context_object_name = 'pbarea'
    queryset = Informasi.objects.filter(key__kategori__in=["public area"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(PublicareaView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class TalangView(ListView):
    paginate_by = 5
    template_name = 'tags/talang.html'
    model = "Informasi"
    context_object_name = 'talang'
    queryset = Informasi.objects.filter(key__kategori__in=["talang"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(TalangView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class SlawiView(ListView):
    paginate_by = 5
    template_name = 'tags/slawi.html'
    model = "Informasi"
    context_object_name = 'slawi'
    queryset = Informasi.objects.filter(key__kategori__in=["slawi"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(SlawiView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class PangkahView(ListView):
    paginate_by = 5
    template_name = 'tags/pangkah.html'
    model = "Informasi"
    context_object_name = 'pangkah'
    queryset = Informasi.objects.filter(key__kategori__in=["pangkah"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(PangkahView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class OlehView(ListView):
    paginate_by = 5
    template_name = 'tags/oleh2.html'
    model = "Informasi"
    context_object_name = 'oleh'
    queryset = Informasi.objects.filter(key__kategori__in=["oleh - oleh khas"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(OlehView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class MelatiView(ListView):
    paginate_by = 5
    template_name = 'tags/melati.html'
    model = "Informasi"
    context_object_name = 'melati'
    queryset = Informasi.objects.filter(key__kategori__in=["melati"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(MelatiView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context

class KedungbantengView(ListView):
    paginate_by = 5
    template_name = 'tags/kedungbanteng.html'
    model = "Informasi"
    context_object_name = 'kedungbanteng'
    queryset = Informasi.objects.filter(key__kategori__in=["kedungbanteng"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(KedungbantengView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class BumijawaView(ListView):
    paginate_by = 5
    template_name = 'tags/bumijawa.html'
    model = "Informasi"
    context_object_name = 'bumijawa'
    queryset = Informasi.objects.filter(key__kategori__in=["bumijawa"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(BumijawaView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class BalapulangView(ListView):
    paginate_by = 5
    template_name = 'tags/balapulang.html'
    model = "Informasi"
    context_object_name = 'balapulang'
    queryset = Informasi.objects.filter(key__kategori__in=["balapulang"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(BalapulangView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
	
class KotategalView(ListView):
    paginate_by = 5
    template_name = 'tags/kotategal.html'
    model = "Informasi"
    context_object_name = 'kotategal'
    queryset = Informasi.objects.filter(key__kategori__in=["Kota Tegal"],status='p').order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(KotategalView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]		
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context	
	
		
class VideoView(ListView):
    paginate_by = 2
    template_name = 'videoresult.html'
    model = "Vidio"
    context_object_name = 'item'
    queryset = Vidio.objects.order_by('-date')
    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]
        context['tags'] = Keywords.objects.order_by('-kategori')
        return context
		
class SearchView(ListView):
    template_name = 'results.html'
    model = "Informasi"
    paginate_by = 5
    context_object_name = 'entries'
    def get_queryset(self):
        key = self.request.GET
        if 'query' in key:
             compiled = reduce(Q.__or__, [Q(alamat__icontains=word) for word in query])| reduce(Q.__or__,
			     [Q(contents__icontains=word) for word in query] ) | reduce(Q.__or__, [Q(title__icontains=word) for word in query] )
             objects = Informasi.objects.filter(compiled, status='p')
        else:
            objects = Informasi.objects.filter(status='p')
        
        return objects

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        key = self.request.GET.get('q')
        context['tags'] = Keywords.objects.order_by('-kategori')
        context['word'] = key		
        context['news'] = Informasi.objects.filter(status='p').order_by('-date')[:5]
        return context

			
class MailView(PostMixinDetailView, TemplateView):
    template_name = 'contact_form/contact_form_sent.html'
    model = "Informasi"
 
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            subject    = request.POST.get('subject')
            message    = request.POST.get('message')
            from_email = request.POST.get('email')
 
            if subject and message and from_email:
                try:
                    fullemail = "Email : "+ " " +from_email + " \n" + message 
                    send_mail(subject, fullemail, from_email, [from_email])
                    return HttpResponseRedirect('/webku/')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')
        return super(MailView, self).dispatch(*args, **kwargs)
 
    def get_context_data(self, **kwargs):
        context = super(MailView, self).get_context_data(**kwargs)
        return context
		
class LocationView(PostMixinDetailView, TemplateView):
    template_name = 'maps.html'
    def geocode_address(address):
		address = address.encode('utf-8')
		geocoder = Google()
		try:
			_, latlon = geocoder.geocode(address)
		except (URLError, GQueryError, ValueError):
			return None
		else:
			return latlon

    def get_shops(longitude, latitude):
		current_point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
		distance_from_point = {'km': 10}
		shops = models.Shop.gis.filter(location__distance_lte=(current_point, measure.D(**distance_from_point)))
		shops = shops.distance(current_point).order_by('distance')
		return shops.distance(current_point)
	
    def dispatch(self, request, *args, **kwargs):		
		if location:
			latitude, longitude = location
			shops = get_shops(longitude, latitude)
		return super(LocationView, self).dispatch(*args, **kwargs)
		
    def get_context_data(self, **kwargs):
        context = super(LocationView, self).get_context_data(**kwargs)
        return context

	
