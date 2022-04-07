from django.shortcuts import render, redirect
from .forms import Article_updateForm, ArticleForm
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

# 요청에 따라 실행을 구분하고 new와 create 함수 합치기 
def create(request):
    if request.method == 'POST' :
    
        form = ArticleForm(request.POST)
        #form에서 전달한 데이터가 유효하면 저장하고 detail을 redircet해라
        if form.is_valid() :
            # form.save()를 하면 생성된 객체를 리턴한다.
            article = form.save()
            return redirect('articles:create',article.pk)

    else :

        form = ArticleForm()
    context = {
        'form' : form,
    }
    # 유효성 검사를 통과하지 못하면 form은 에러메시지를 담고 있다. 그래서 에러메시지를 출력한다. 
    return render(request, 'articles/create.html',context)

def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST' : 
        # instacne=article을 안써주면 새로운 글을 만든다. 
        form = ArticleForm(request.POST,instance=article)
        if form.is_valid() :
            article=form.save()
            return redirect('articles:detail', article.pk) 
    else :
        # 기존 정보를 받아서 update.html을 표시하기 
        form = ArticleForm(instance=article)
    context = {
        'article' : article,
        'form': form
    }
    return render(request, 'articles/update.html', context)

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


# def edit(request, pk):
#     article = Article.objects.get(pk=pk)
#     context = {
#         'article': article,
#     }
#     return render(request, 'articles/edit.html', context)

