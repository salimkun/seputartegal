from __future__ import unicode_literals
from django.contrib import admin
from webku.models import *
from checkboxselectmultiple.admin import CheckboxSelectMultipleAdmin
from django.http import HttpResponse
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django_object_actions import DjangoObjectActions



	
class InformasiAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('id', 'title', 'date', "status")
    search_fields = ('id', 'title', 'date')
    list_display_links = ('title',)
    list_per_page = 20
    actions = ['make_published']
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
	

admin.site.register(Images)
admin.site.register(Keywords)
admin.site.register(Informasi, InformasiAdmin)
admin.site.register(Vidio)
admin.site.register(Testimonial)