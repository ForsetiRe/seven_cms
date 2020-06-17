from django.shortcuts import render
from django.views.generic import View
from apps.news.models import NewsCategory, News
from utils import restful
from .forms import WriteNewsForm


# Create your views here.
def index(request):
    return render(request, 'cms/index.html')


class WriteNews(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, reuqest):
        form = WriteNewsForm(reuqest.POST)
        if form.is_valid():
            # 文章分类接收过来的是一个id，根据id获取该分类对象
            pass


def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'cms/news_category.html', context=context)


def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.success()
    else:
        return restful.params_error(message='该分类已经存在')

