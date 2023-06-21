from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Post, Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':2, 'placeholder': 'Crea tu post!'}), required=True)

    class Meta:
        model = Post 
        fields = ['content']

class CommentForm(forms.ModelForm):

    class Meta: 
        model = Comment
        fields = ('user', 'content',)
        
class ProfileEditForm(forms.ModelForm):
    image = forms.ImageField(label='Foto de perfil', required=False)

    class Meta:
        model = User
        fields = ['username', 'image']