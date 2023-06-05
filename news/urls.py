from django.urls import path
from .views import NewsListView, NewsDetailView, SearchView, SearchResultView
from .views import NewsCreateView, NewsUpdateView, NewsDeleteView, LoginView, ArticleCreateView

app_name = 'news'

urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/search/', SearchView.as_view(), name='search'),
    path('news/search/results/', SearchResultView.as_view(), name='search_results'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('create/', ArticleCreateView.as_view(), name='article_create')
]