from .models import News
def latest_news(request):
    latest_news=News.published.all().order_by('-publish_time')[0:5]

    context={
        'latest_news':latest_news
    }
    return context