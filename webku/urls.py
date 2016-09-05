from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views, feed
from .models import *


app_name= 'webku'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^feed/$', feed.LatestPosts(), name="blog_feed"),
	url(r'^(?P<pk>[0-9]+)/$', views.PostDetailJSONView.as_view(), name='ajax'),
	url(r'^info/(?P<pk>[0-9]+)/$', views.DetailView.as_view(model=Informasi), name='detail'),
	url(r'^belanja/$', views.DaftarView.as_view(), name='belanja'),
	url(r'^budaya/$', views.BudayaView.as_view(), name='budaya'),
	url(r'^transport/$', views.TransportView.as_view(), name='transport'),
	url(r'^akomodasi/$', views.AkomodasiView.as_view(), name='akomodasi'),	
	url(r'^$', views.LocationView.as_view(), name='index'),		
	url(r'^wisata/$', views.WisataView.as_view(), name='wisata'),			
	url(r'^kuliner/$', views.KulinerView.as_view(), name='kuliner'),
	url(r'^wisataair/$', views.WairView.as_view(), name='wisataair'),
	url(r'^wisataziarah/$', views.WziarahView.as_view(), name='wisataziarah'),
	url(r'^wisatasejarah/$', views.WsejarahView.as_view(), name='wisatasejarah'),
	url(r'^wisatareligi/$', views.WreligiView.as_view(), name='wisatareligi'),
	url(r'^wisatakuliner/$', views.WkulinerView.as_view(), name='wisatakuliner'),
	url(r'^wisataedukasi/$', views.WedukasiView.as_view(), name='wisataedukasi'),
	url(r'^wisatabudaya/$', views.WbudayaView.as_view(), name='wisatabudaya'),
	url(r'^wisataalternatif/$', views.WalternatifView.as_view(), name='wisataalternatif'),
	url(r'^wisaalam/$', views.WalamView.as_view(), name='wisataalam'),
	url(r'^publicarea/$', views.PublicareaView.as_view(), name='publicarea'),
	url(r'^talang/$', views.TalangView.as_view(), name='talang'),
	url(r'^slawi/$', views.SlawiView.as_view(), name='slawi'),
	url(r'^pangkah/$', views.PangkahView.as_view(), name='pangkah'),
	url(r'^oleh-olehkhas/$', views.OlehView.as_view(), name='oleh2'),
	url(r'^melati/$', views.MelatiView.as_view(), name='melati'),
	url(r'^kedungbanteng/$', views.KedungbantengView.as_view(), name='kedungbanteng'),
	url(r'^bumijawa/$', views.BumijawaView.as_view(), name='bumijawa'),
	url(r'^balapulang/$', views.BalapulangView.as_view(), name='balapulang'),	
	url(r'^kotategal/$', views.KotategalView.as_view(), name='kotategal'),	
	url(r'^search/$', views.SearchView.as_view(), name='search'),	
	url(r'^video/$', views.VideoView.as_view(), name='video'),		
	url(r'^mail/$', views.MailView.as_view(), name='mail'),		
	url(r'^(?P<pk>[0-9]+)/$', views.PostCountHitDetailView.as_view(), name="detail-with-count"),
	url(r'^(?P<location>\w{0,50})/$', views.LocationView.as_view(), name='maps'),   
	] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)