from django.shortcuts import render, redirect,get_object_or_404
from .forms import Article_updateForm, ArticleForm,CommentForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Article
from django.contrib.auth.decorators import login_required


# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

# 요청에 따라 실행을 구분하고 new와 create 함수 합치기 
@login_required
def create(request):
    if request.method == 'POST' :
        form = ArticleForm(request.POST, request.FILES)
        #form에서 전달한 데이터가 유효하면 저장하고 detail을 redircet해라
        if form.is_valid() :
            # form.save()를 하면 생성된 객체를 리턴한다.
            article = form.save()
            return redirect('articles:detail',article.pk)

    else :
        form = ArticleForm()
    context = {
        'form' : form,
    }
    # 유효성 검사를 통과하지 못하면 form은 에러메시지를 담고 있다. 그래서 에러메시지를 출력한다. 
    return render(request, 'articles/form.html',context)

#GET과 POST만 허용한다. 아니면 405에러 리턴 
@login_required
@require_http_methods(['GET','POST'])
def update(request, pk):
    article = get_object_or_404(Article,pk=pk)
    if request.method == 'POST' : 
        # instacne=article을 안써주면 새로운 글을 만든다. 
        form = ArticleForm(request.POST, request.FILES,instance=article)
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
    return render(request, 'articles/form.html', context)

@require_safe
def detail(request, pk):
    # article = Article.objects.get(pk=pk)
    # 객체가 있으면 객체를 없으면 404에러를 담아서 반환 
    article = get_object_or_404(Article,pk=pk)
    comment_form = CommentForm()
    context = {
        'article': article,
        'comment_form' : comment_form,
    }
    return render(request, 'articles/detail.html', context)

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article,pk=pk)
        article.delete()
    return redirect('articles:index')


@require_POST
def comments_create(request,pk) :
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid() :
        # commit의 기본값은 true이다. commit을 False로 바꿔서 DB에 저장은 안하고 인스턴스는 만들어줌 
        comment = comment_form.save(commit=False)
        # 누락된 article입력 해주고 
        comment.article = article
        #세이브 해줌 
        comment.save()
    return redirect('articles:detail',article.pk)