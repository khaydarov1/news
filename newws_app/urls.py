from django.urls import path
from .views import news_list, news_detail, homePageView, contactPageView, page404View, aboutPageView,\
    LocalNewsViews,SportNewsViews,TechnoNewsViews,XorijNewsViews

urlpatterns = [
    path('', homePageView, name="home_page"),
    path('news/', news_list, name="all_news_list"),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('contact/', contactPageView, name='contact_page'),
    path('404/', page404View, name='404_page'),
    path('about/', aboutPageView, name='about_page'),
    path('mahaliy/',LocalNewsViews.as_view(),name='local_page'),
    path('xorij/',XorijNewsViews.as_view(),name='world_page'),
    path('sport/',SportNewsViews.as_view(),name='sport_page'),
    path('texnologiya/',TechnoNewsViews.as_view(),name='texno_page')

]
