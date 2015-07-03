from django.conf.urls import patterns, url
from workspace.manageDataviews.views import *
from workspace.manageDatasets.views import filter as filterDataset
from core.datastream_manager.views import action_invoke
# Check if we have to use manageDataviews.create or datasream_manger.action_insert
# from workspace.datastream_manager.views import action_view

urlpatterns = patterns('',

    url(r'^$', list, name='manageDataviews.list'),
    url(r'^(?P<revision_id>\d+)$', action_view, name='manageDataviews.view'),
    url(r'^filter$', filter, name='manageDataviews.filter'),
    url(r'^filters.json$', get_filters_json, name='manageDataviews.get_filters'),
    url(r'^filter_dataset$', filterDataset, name='manageDatasets.filter'),
    url(r'^remove/(?P<type>[a-z]+)/(?P<id>\d+)$', remove, name='manageDataviews.remove'),
    url(r'^remove/(?P<id>\d+)$', remove, name='manageDataviews.remove'),
    url(r'^create$', create, name='manageDataviews.create'),
    url(r'^edit$', edit, name='manageDataviews.edit'),
    url(r'^edit/(?P<datastream_revision_id>\d+)$', edit, name='manageDataviews.edit'),
    url(r'^related_resources$', related_resources, name='manageDataviews.related_resources'),
    url(r'^review/(?P<datastream_revision_id>\d+)/$', review, name='manageDataviews.review'),
    url(r'^action_preview$', action_preview, name='manageDatasets.action_preview'),
    url(r'^invoke$', action_invoke, name='core.datastream_manager.views.action_invoke'),
    url(r'^action_updategrid$', 'core.datastream_manager.views.action_updategrid', name='core.datastream_manager.action_updategrid'),
)
