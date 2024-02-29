from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from hitcount.utils import get_hitcount_model

# Create your views here.
from .models import News, Category
from .forms import ContactForm, CommentForm
from news_project.custom_permissions import OnlyLoggedSuperUser
from hitcount.views import HitCountDetailView, HitCountMixin


def news_list(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


def news_detail(request, news):
    context = {}
    # hitcount logic
    # HitCountModel = get_hitcount_model()
    # hit_count = HitCountModel.objects.get_for_object(news)
    # hits = hit_count.hits
    # hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    # hit_count_response = HitCountMixin.hit_count(request, hit_count)
    # if hit_count_response.hit_counted:
    #     hits = hits + 1
    #     hitcontext['hit_counted'] = hit_count_response.hit_counted
    #     hitcontext['hit_message'] = hit_count_response.hit_message
    #     hitcontext['total_hits'] = hits

    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    comments = news.comments.filter(active=True)
    comment_count=comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        'comments': comments,
        'comment_count':comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, "news/news_detail.html", context)


def homePageView(request):
    news_list = News.published.all().order_by('-publish_time')[:5]
    categories = Category.objects.all()
    mahaliy_news = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[:5]
    sport_news = News.published.all().filter(category__name="Sport").order_by('-publish_time')[:5]
    texno_news = News.published.all().filter(category__name="Texnologiya").order_by('-publish_time')[:5]
    world_news = News.published.all().filter(category__name="Xorij").order_by('-publish_time')[:5]

    context = {
        'news_list': news_list,
        'categories': categories,
        'mahaliy_news': mahaliy_news,
        'sport_news': sport_news,
        'texno_news': texno_news,
        'world_news': world_news
    }
    return render(request, 'news/home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_one'] = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[0:1]
        context['local_news'] = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[1:5]
        return context


def contactPageView(request):
    print(request.POST)
    form = ContactForm(request.POST)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("<h2>Tez orada bog'lanamiz</h2>")

    context = {
        'form': form
    }
    return render(request, 'news/contact.html', context)


# class ContactPageView(TemplateView):
#     temlate_name='news/contact.html'
#
#     def get(self,request,*args,**kwargs):
#         form=ContactForm
#         context={
#             'form':form
#         }
#         return render(request,'news/contact.html',context)
#
#     def post(self,request,*args,**kwargs):
#         form=ContactForm(request.POST)
#         if request.method=='POST'and form.is_valid():
#             form.save()
#             return HttpResponse("<h1>RAHMAT</h1>")
#         context={
#         'form':form
#         }
#         return render(request, 'news/contact.html', context)

def page404View(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'news/404.html', context)


def aboutPageView(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'news/about.html', context)


class LocalNewsViews(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahaliy_news'

    def category(self):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return context

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news


class XorijNewsViews(ListView):
    model = News
    template_name = 'news/world.html'
    context_object_name = 'world_news'

    def category(self):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(self, context)

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news


class SportNewsViews(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'
    categories = Category.objects.all()
    context = {
        'categories': categories
    }

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news


class TechnoNewsViews(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texno_news'

    def category(self):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(self, context)

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_create.html'

    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearechResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)

                                   )
