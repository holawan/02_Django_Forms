from django import forms

from articles.models import Article,Comment

class ArticleForm(forms.ModelForm) :
    # 장고 모델을 참고해서 form을 만들어줌 
    
    # input에 속성을 넣으려면 widget 내부 attribute에 작성을 해야한다.
    title = forms.CharField(
        widget=forms.TextInput(
            # attributes
            attrs = {
                'class' : 'my-title form-control',
                'placeholder':'Enter the title',

            }
        )
    )
    content = forms.CharField(
        widget = forms.Textarea(
            attrs={
                'class' : 'my-content form-control',
                'placeholder' :'Enter the content',

            }
        ),
        error_messages={
            'required' : 'Please enter your content!!!!!',
        }
    )
    class Meta :
        model = Article
        # 전체 필드 출력하는 __all__
        # fields = '__all__'
        exclude = ('user',)

# updateform을 만들 때 제목은 변경 못하게 하고 싶다면,
#기존 사용하던 createform을 상속 받은 후 
#원하느 필드를 읽기전용으로 만들거나 작동하지 않게 만듬 
class Article_updateForm(ArticleForm) :
    def __init__(self,*args,**kwargs) :
        super().__init__(*args,**kwargs)

        # self.fields['title'].widget.attrs['readonly'] = True
        
        # self.fields['content'].disabled = True

class CommentForm(forms.ModelForm) :

    class Meta :
        model = Comment
        fields = ('content',)