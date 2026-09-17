from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label="搜索关键词",error_messages={"required":"请输入搜索关键词"})
