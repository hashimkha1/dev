from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import PostForm
from .models import Post
from .utils import buildmodel

class PostDetailView(DetailView):
    model=Post
    ordering=['-date_posted']

class PostListView(ListView):
    model=Post
    template_name='codablog/success.html'
    context_object_name='posts'
    ordering=['-date_posted']

def newpost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # # quest = 'List the fininancial statements?'
            form.instance.writer = request.user
            # print("request_user", request.user)
            # print("User",form.instance.author)            
            form.save()
            return redirect('main:layout')
            # try:
            # except:
            #     return render(request, "main/errors/404.html")
    else:
        form = PostForm()
        quest = "write 3 full paragraphs each on how good my data analyst coach was"
        # sample_description=buildmodel(question=quest)
        # print("sample_description",sample_description)
        response = buildmodel(question=quest)
        context={
            "response" : response,
            "form": form
        }
        # form.instance.description = buildmodel(question=quest)
        print("response",response)
    return render(request, "codablog/post_form.html", context)


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