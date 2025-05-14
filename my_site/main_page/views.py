from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Comment, Post, Like
from django.views.generic.edit import FormMixin
from .forms import CommentCreationForm, PostCreationForm
from django.urls import reverse_lazy
import random
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import F


def chat(request):
    return render(request, 'main_page/chat.html', locals())

def post(request):
    return render(request, 'post.html', locals())

class PostListView(ListView):
    model = Post
    template_name = "main_page/home.html"
    context_object_name = "posts_lists" 

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("comments", "tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_posts = list(self.object_list)
        
        for post in all_posts:
            post.comments_count = post.comments.count()
            post.tag = post.tags.all()
        
        context['posts_lists'] = [
            random.sample(all_posts, len(all_posts)) 
            for _ in range(5)
        ]
        
        return context

class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = "main_page/post.html"
    context_object_name = "post"
    form_class = CommentCreationForm

    def get_object(self):
        return self.model.objects.prefetch_related("tags", "comments").get(id=self.kwargs[self.pk_url_kwarg])
    
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["tags"] = self.object.tags.all()
        kwargs["comments"] = self.object.comments.all()

        interacted_user = self.request.user
        post = self.object
        if interacted_user.is_authenticated and Like.objects.filter(user=interacted_user, post=post).exists():
            kwargs["is_liked"] = True
        else:
            kwargs["is_liked"] = False
        return kwargs
    
    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = self.get_object()
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post', kwargs={"pk":self.kwargs[self.pk_url_kwarg]})
    
def post_or_comment_like(request):
    if int(request.POST["is_comment"]) == 1: # Comment [1]
        change_like_counter(request.POST["id"], request.user, Comment)
    elif int(request.POST["is_comment"]) == 0: # Post [0]
        change_like_counter(request.POST["id"], request.user, Post)

    return HttpResponse("Success")


def change_like_counter(id: int, user, model):
    model_by_id = model.objects.filter(id=id)
    model_arguments = {
        'user': user,
        model.__name__.lower(): model_by_id[0]
    }
    model_like = Like.objects.filter(**model_arguments)

    if not model_like.exists():
        Like.objects.create(**model_arguments).save()
        model_by_id.update(likes=F("likes") + 1)
    else:
        model_like[0].delete()
        model_by_id.update(likes=F("likes") - 1)

@login_required
def create_post(request):
    form = PostCreationForm(request.POST or None)
    context = {
        "form": form
    }
    template = loader.get_template("main_page/create_post.html")
    if form.is_valid():
        post = form.save()
        post.save()
        return HttpResponseRedirect("/")
    return HttpResponse(template.render(context, request))