from django.urls import include, path

urlpatterns = [
    path('news/', include('news.urls', namespace='news')),
    path('articles/', include('news.urls', namespace='articles')),
    path('accounts/', include('django.contrib.auth.urls')),
]