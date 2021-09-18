from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post,Rate
from .forms import RatingForm




class PostDetailView(DetailView):
    model=Post
    ordering=['-date_posted']


class PostListView(ListView):
    model=Post
    template_name='codablog/success.html'
    context_object_name='posts'
    ordering=['-date_posted']


class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url="/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# For Rating-Internal Use Only

def rate(request):
    if request.method== "POST":
        form=RatingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('codablog-rating')
    else:
        form=RatingForm()
    return render(request, 'codablog/rate.html',{'form':form})

class RateCreateView(LoginRequiredMixin, CreateView):
    model=Rate
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class RateListView(ListView):
    model=Rate
    template_name='codablog/rating.html'
    context_object_name='ratings'
    ordering=['-date_posted']

