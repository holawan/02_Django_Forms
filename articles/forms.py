from django import forms

class ArticleForm(forms.Form) :
    REGION_A = 'sl'
    REGION_B = 'dj'
    REGION_C = 'bs'

    REGIONS_CHOICES = [
        (REGION_A, '서울'),
        (REGION_B, '대전'),
        (REGION_C, '광주')
    ]

    # Models.py와 유사한 구조 (form 클래스를 상속받음)
    title = forms.CharField(max_length=10)
    content = forms.CharField(widget=forms.Textarea)
    # select 태그 만들기 
    region = forms.ChoiceField(choices = REGIONS_CHOICES, widget = forms.Select())