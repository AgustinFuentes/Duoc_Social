from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PostForm, ProfileEditForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def feed(request):
  posts = Post.objects.all().order_by('-votes')
  comments = Comment.objects.all()

  context = { 'posts' : posts,
              'comments': comments, }

  return render(request, 'social/feed.html', context)

def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      messages.success(request, f'Usuario {username} creado')
      return redirect('feed')
  else:
    form = UserRegisterForm()

  context = { 'form' : form }
  return render(request, 'social/register.html', context)

def terms(request):
  return render(request, 'social/terms.html')

def post(request):
  current_user = get_object_or_404(User, pk=request.user.pk)
  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = current_user
      post.save()
      messages.success(request, 'Post publicado')
      return redirect('feed')
  else:
    form = PostForm()
  return render(request, 'social/post.html', {'form' : form})

@login_required
def vote_post(request, post_id):
  post = get_object_or_404(Post, id = post_id)
  if request.user in post.voters.all():
    return redirect('feed')

  post.votes += 1  
  post.voters.add(request.user)
  post.save()
  return redirect('feed')

def profile(request, username=None):
  current_user = request.user
  if username and username != current_user.username:
    user = User.objects.get(username=username)
    posts = user.posts.all()
  else:
    posts = current_user.posts.all()
    user = current_user

  if request.method == 'POST':
    form = ProfileEditForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      image = form.cleaned_data['image']
      if image:
        user.profile.image = image
      form.save()
      user.profile.save()
      messages.success(request, 'Perfil actualizado exitosamente.')
      return redirect('profile')
  else:
    form = ProfileEditForm(instance=user)

  can_start_conversation = username and username != current_user.username
  context = {
    'user': user,
    'posts': posts,
    'can_start_conversation': can_start_conversation,
    'form': form,
  }
  return render(request, 'social/profile.html', context)

@login_required
def follow(request, username):
  current_user = request.user
  to_user = User.objects.get(username = username)
  to_user_id = to_user
  rel = Relationship(from_user = current_user, to_user = to_user_id)
  rel.save()
  messages.success(request, f'Has comenzado a seguir a {username}!')
  return redirect('feed')

def unfollow(request, username):
  current_user = request.user
  to_user = User.objects.get(username = username)
  to_user_id = to_user.id
  rel = Relationship.objects.filter(from_user = current_user.id, to_user = to_user_id).get()
  rel.delete()
  messages.success(request, f'Has dejado a seguir a {username}!')
  return redirect('feed')

@login_required
def create_conversation(request, username):
  current_user = request.user
  target_user = get_object_or_404(User, username=username)

  conversation = Conversation.objects.filter(participants=current_user).filter(participants=target_user).first()
  if not conversation:
    conversation = Conversation.objects.create()
    conversation.participants.add(current_user, target_user)

  return redirect('conversation', conversation_id=conversation.pk)

def conversation(request, conversation_id):
  conversation = get_object_or_404(Conversation, pk=conversation_id)
  messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

  context = {
    'conversation':conversation,
    'messages':messages,
  }
  return render(request, 'social/conversation.html', context)

def send_message(request, conversation_id):
  if request.method == 'POST':
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    message_content = request.POST.get('message')
    sender = request.user
    message = Message(conversation=conversation, sender=sender, content=message_content)
    message.save()
  return HttpResponseRedirect(reverse('conversation', args=[conversation_id]))

@login_required
def conversation_list(request):
    current_user = request.user
    conversations = Conversation.objects.filter(participants=current_user)
    context = {'conversations': conversations}
    return render(request, 'social/conversation_list.html', context)


def add_comment(request, post_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        post = Post.objects.get(id=post_id)
        Comment.objects.create(user=request.user, post=post, content=comment_text)
    return redirect('feed')

