from django.urls import path
from .views import detailView, listView, redirectPage, searchView, tagged_post_list, series_post_list

urlpatterns = [
    path('', redirectPage, name='pageredirect'),
    path('search/', searchView, name='search'),
    path('tag/<slug:tag_url>/', tagged_post_list, name='tagged_post_list'),
    path('series/<slug:series_url>/', series_post_list, name='series_post_list'),
    path('<slug:list_url>/', listView, name='listpage'),
    path('<slug:category>/<slug:url>/', detailView, name='detailpage'),
]
