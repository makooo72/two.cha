from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import ForumUser
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse


class RegistrationView(View):
    
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', context={"form":form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ForumUser.objects.create(user=user)
            login(request, user)
            return redirect('login')
        return render(request, 'registration/register.html', context={"form":form})
    
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    context_object_name = "user"
    login_url = reverse_lazy('login')

    def get_object(self):
        return self.model.objects.select_related("forum_user").prefetch_related("posts", "following", "followers").get(id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["following"] = self.object.following.count()
        kwargs["followers"] = self.object.followers.count()
        kwargs["posts_count"] = self.object.posts.count()
        kwargs["posts"] = self.object.posts.all()
        return kwargs

class EditProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "edit_profile.html"
    context_object_name = "user"
    login_url = reverse_lazy('login')

    def get_object(self):
        return self.model.objects.select_related("forum_user").get(id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        return kwargs
    

class SaveChangesProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "user"
    login_url = reverse_lazy('login')

    def post(self, request):
        description_by_id = self.model.objects.select_related("forum_user").filter(id=self.request.user.id)

        if description_by_id.description != request.POST["description"]: description_by_id.description = request.POST["description"]
        description_by_id.save()
