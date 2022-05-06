from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404

from articles import seriallizers
from .forms import Article_updateForm, ArticleForm,CommentForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Article,Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .seriallizers import ArticleSeriallizer
# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    paginator = Paginator(articles,2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'articles': page_obj,
    }
    return render(request, 'articles/index.html', context)

@api_view(['GET'])
def ajax(request) :
    articles = Article.objects.order_by('-pk')
    paginator = Paginator(articles,2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    seriallizer = ArticleSeriallizer(page_obj,many=True)
    return Response(seriallizer.data)

# 요청에 따라 실행을 구분하고 new와 create 함수 합치기 
@login_required
def create(request):
    if request.method == 'POST' :
        form = ArticleForm(request.POST, request.FILES)
        #form에서 전달한 데이터가 유효하면 저장하고 detail을 redircet해라
        if form.is_valid() :
            # form.save()를 하면 생성된 객체를 리턴한다.
            article = form.save(commit=False)
            article.user = request.user
            article.save()
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
    if request.user == article.user :
        if request.method == 'POST' : 
            # instacne=article을 안써주면 새로운 글을 만든다. 
            form = ArticleForm(request.POST, request.FILES,instance=article)
            if form.is_valid() :
                article=form.save()
                return redirect('articles:detail', article.pk) 
        else :
            # 기존 정보를 받아서 update.html을 표시하기 
            form = ArticleForm(instance=article)
    else :
        return redirect('articles:index')
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
    # 조회한 article에 모든 댓글을 조회 
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form' : comment_form,
        'comments' : comments
    }
    return render(request, 'articles/detail.html', context)

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article,pk=pk)
        if request.user == article.user :
            article.delete()
    return redirect('articles:index')


@require_POST
def comments_create(request,pk) :
    if request.user.is_authenticated :
        article = get_object_or_404(Article,pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() :
            # commit의 기본값은 true이다. commit을 False로 바꿔서 DB에 저장은 안하고 인스턴스는 만들어줌 
            comment = comment_form.save(commit=False)
            # 누락된 article입력 해주고 
            comment.article = article
            comment.user = request.user
            #세이브 해줌 
            comment.save()
        return redirect('articles:detail',article.pk)
    return redirect('accounts:login')

@require_POST
def comments_delete(request,article_pk,comment_pk) :
    if request.user.is_authenticated :
        comment = get_object_or_404(Comment,pk=comment_pk)
        # article_pk = comment.article.pk
        if request.user == comment.user :
            comment.delete()
        return redirect('articles:detail',article_pk)
    return redirect('accounts:login')


def likes(request,article_pk) :
    #어떤 객체에 좋아요가 눌렸는지 확인
    article = get_object_or_404(Article, pk=article_pk)
    #누르는게 무조건 좋아요를 활성화하는 것은 아님 좋아요를 2번 누르면 취소되게 구현할 수 있음
    
    #이 게시글에 좋아요를 누른 유저 목록에 현재 요청하는 유저가 있다면 좋아요 취소 
    ##2가지 방법으로 조회 가능 
    if article.like_users.filter(pk=request.user.pk).exists() :
    # if request.user in article.like_users.all() : 
        article.like_users.remove(request.user)
        liked = False 
    #아니면 좋아요
    else :
        article.like_users.add(request.user)
        liked = True 
    context = {
        'liked' : liked,
        'like_count' : article.like_users.count()
    }
    return JsonResponse(context)
    # return redirect('articles:index')

