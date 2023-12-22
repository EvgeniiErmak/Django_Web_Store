from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogpost/post_list.html'
    context_object_name = 'object_list'


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost/post_detail.html'


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost/post_form.html'


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost/post_form.html'


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogpost/post_confirm_delete.html'
    success_url = reverse_lazy('blogpost:post_list')
