from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


# def new(request):
#     form = ArticleForm()
#     context = {
#         'form' : form,
#     }
#     return render(request, 'articles/new.html',context)

# 제목과 내용을 누르고 제출을 했을 때 crate 변수로 가게되서 동작을 하고 마지막으로 redirect가 return 된다. 

# 요청에 따라 실행을 구분하고 new와 create 함수 합치기 
def create(request):
    if request.method == 'POST' :

        form = ArticleForm(request.POST)
        #form에서 전달한 데이터가 유효하면 저장하고 detail을 redircet해라
        if form.is_valid() :
            # form.save()를 하면 생성된 객체를 리턴한다.
            article = form.save()
            return redirect('articles:detail',article.pk)
        #유효하지 않으면 다시 new로 가라 
        # title = request.POST.get('title')
        # content = request.POST.get('content')

        # article = Article(title=title, content=content)
        # article.save()

        # return redirect('articles:detail', article.pk)
    elif request.method == 'GET' :

        form = ArticleForm()
    context = {
        'form' : form,
    }
    return render(request, 'articles/create.html',context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:index')
    else:
        return redirect('articles:detail', article.pk)


def edit(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/edit.html', context)


def update(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm(request.POST,instacne=article)
    article=form.save()
    # article.title = request.POST.get('title')
    # article.content = request.POST.get('content')
    # article.save()
    return redirect('articles:detail', article.pk)
