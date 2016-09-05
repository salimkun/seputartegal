from __future__ import unicode_literals


from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin
from embed_video.fields import EmbedVideoField
from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError
import qrcode  
import StringIO
from django.core.signals import request_finished  
from django.db.models.signals import pre_delete  
from django.dispatch import receiver
from django.core.urlresolvers import reverse  
from django.core.files.uploadedfile import InMemoryUploadedFile
from urllib2 import URLError
from geoposition.fields import GeopositionField
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.db import models
from geopy.geocoders.googlev3 import GoogleV3
from geopy.exc import GeocoderQueryError
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField

class Keywords(models.Model):
    kategori = models.CharField(max_length=30)

    def __str__(self):       
        return self.kategori

    class Meta:
        ordering = ('kategori',)

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)

class Images(models.Model):
 title = models.CharField(max_length=50)
 keterangan = models.CharField(max_length=200,null=True, blank=True)
 image = models.ImageField(upload_to='document/%Y/%m/%d' ,null=True, blank=True)
 image_satu = models.ImageField(upload_to='document/%Y/%m/%d', null=True, blank=True)
 image_dua = models.ImageField(upload_to='document/%Y/%m/%d', null=True, blank=True)
 image_tiga = models.ImageField(upload_to='document/%Y/%m/%d', null=True, blank=True)
 image_empat = models.ImageField(upload_to='document/%Y/%m/%d', null=True, blank=True)

 def __str__(self):
	return self.title	

 class Meta:
	ordering = ['title']
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    location = gis_models.PointField(null=True, blank=True)
    longitude = gis_models.FloatField(null=True, blank=True)
    latitude = gis_models.FloatField(null=True, blank=True)
    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        self.location = Point(self.longitude, self.latitude)
        super(Location, self).save(**kwargs)
		
class Informasi(models.Model, HitCountMixin):
 title = models.CharField(max_length=50)
 body = RichTextUploadingField(null=True, blank=True)
 alamat = models.TextField(null=True, blank=True)
 date = models.DateTimeField(auto_now_add=True)
 status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, blank=True)
 latitude = gis_models.FloatField(null=True, blank=True)
 longitude = gis_models.FloatField(null=True, blank=True) 
 location = GeopositionField(null=True, blank=True)
 key = models.ManyToManyField(Keywords)
 qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True)
 image = models.ForeignKey(Images, on_delete=models.CASCADE)
 hit_count_generic = GenericRelation( HitCount, object_id_field='object_pk',
 related_query_name='hit_count_generic_relation')
 def get_colour(self):
    if not self.colour:
        return 'red'
    else:
        return self.colour
 def get_absolute_url(self):
	return reverse('events.views.details', args=[str(self.id)])

 def generate_qrcode(self):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=6,
		border=0,
    )
    
	qr.add_data(self.get_absolute_url())
	qr.make(fit=True)

	img = qr.make_image()

	buffer = StringIO.StringIO()
	img.save(buffer)
	filename = 'events-%s.png' % (self.id)
	filebuffer = InMemoryUploadedFile(
		buffer, None, filename, 'image/png', buffer.len, None)
	self.qrcode.save(filename, filebuffer) 

 def get_lat(self):
        return self.location.latitude

 def get_lon(self):
        return self.location.longitude	

 def __str__(self):
	return self.title	

 class Meta:
	ordering = ['date']

class Vidio(models.Model):
	title = models.CharField(max_length=50)
	url = models.CharField(max_length=50)
	date = models.DateTimeField('date published')	
	key = models.ManyToManyField(Keywords)
	
	def __str__(self):
		return self.title	

	class Meta:
		ordering = ['date']
	
class Komentar(models.Model):
    title = models.ForeignKey(Informasi, on_delete=models.CASCADE)
    comments = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
	  return self.title

MY_CHOICES = (
        ('SuaraMerdeka.com', 'SuaraMerdeka'),
        ('RadarTegal.com', 'RadarTegal'),
)

class Testimonial(models.Model):
 name = models.CharField(max_length=25)
 contents = models.TextField()
 image = models.ImageField(upload_to='document/%Y/%m/%d' ,null=True, blank=True)
 date = models.DateTimeField('date published')		
 def __str__(self):
	return self.name	

 class Meta:
	ordering = ['date']
	

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=Textarea())


