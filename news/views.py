from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import render
from django import forms
from .forms import PostForm


class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post_type='news')  # Отфильтровать только новости
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        current_page = self.request.GET.get('page', 1)
        news = paginator.get_page(current_page)

        start_range = max(news.number - 5, 1)
        end_range = min(news.number + 4, paginator.num_pages)

        context['news'] = news
        context['paginator'] = paginator
        context['start_range'] = start_range
        context['end_range'] = end_range
        context['current_page'] = news.number
        context['news_count'] = Post.objects.filter(post_type='news').count()
        context['news'] = Post.objects.filter(post_type='news')  # Получить только новости
        return context


class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'


class SearchView(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Post.objects.filter(title__icontains=query)

        return Post.objects.none()


class SearchResultView(ListView):
    model = Post
    template_name = 'news/search_results.html'
    context_object_name = 'search_results'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_results = context['search_results']

        paginator = Paginator(search_results, self.paginate_by)
        current_page = self.request.GET.get('page', 1)
        search_results = paginator.get_page(current_page)

        start_range = max(search_results.number - 5, 1)
        end_range = min(search_results.number + 4, paginator.num_pages)

        context['start_range'] = start_range
        context['end_range'] = end_range
        context['current_page'] = search_results.number

        return context


class LoginView(AuthLoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'news/news_create.html'
    form_class = PostForm
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'news'  # Устанавливаем значение поля post_type
        return super().form_valid(form)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'articles/article_create.html'
    form_class = PostForm
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'article'  # Задаем тип записи как "статья"
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    model = Post
    template_name = 'news/news_edit.html'
    fields = ['title', 'content', 'rating', 'categories']
    success_url = reverse_lazy('news:news_list')


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news:news_list')

