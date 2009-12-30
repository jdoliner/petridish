from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^graph/(?P<graph_id>\d+)/$', 'petridish.graph.views.graph_id'),
	(r'^dish/$', 'petridish.dish.views.dish'),
	(r'^dish/new/$', 'petridish.dish.views.new'),
	(r'^dish/(?P<d_id>\d+)/$', 'petridish.dish.views.dish_id'),
	(r'^dish/(?P<d_id>\d+)/generation=(?P<generation>\d+)/$', 'petridish.dish.views.dish_id'),
	(r'^dish/(?P<d_id>\d+)/populate/$', 'petridish.dish.views.populate'),
	(r'^dish/(?P<d_id>\d+)/populate/graph/$', 'petridish.graph.views.populate'),
	(r'^dish/(?P<d_id>\d+)/clear/$', 'petridish.dish.views.clear'),
	(r'^dish/(?P<d_id>\d+)/delete/$', 'petridish.dish.views.delete'),
	(r'^organism/(?P<organism_id>\d+)/$', 'petridish.organism.views.organism_id'),
	(r'^breed/$', 'petridish.graph.views.breed'),
	(r'^function/(?P<f_id>\d+)/$', 'petridish.function.views.function_id')
)
