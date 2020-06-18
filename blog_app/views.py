from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
		ListView,
		DetailView, 
		CreateView,
		UpdateView,
		DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post

# posts = [
#     {
#         "title": "My first Post",
#         "author": "dev",
#         "content": "this is my first post hurray",
#         "date_posted": "12 jun 2020",
#     },
#     {
#         "title": "My Second Post",
#         "author": "dev",
#         "content": "this is my first post hurray",
#         "date_posted": "13 jun 2020",
#     },
#     {
#         "title": "My Third Post",
#         "author": "dev",
#         "content": "this is my first post hurray",
#         "date_posted": "14 jun 2020",
#     },
# ]
# Create your views here.
def home(request):

    context = {'posts':Post.objects.all()}
    return render(request, "blog_app/home.html",context)

class PostListView(ListView):
	model = Post
	template_name = 'blog_app/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ('-date_posted')
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'blog_app/user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 5
	def get_queryset(self):
		user = get_object_or_404(User,username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')



		
class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']
	success_url = '/'

	def form_valid(self,form):
		# if self.request.user:
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	success_url = '/'

	def form_valid(self,form):
		# if self.request.user:
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False



def about(request):
    return render(request, "blog_app/about.html",{'title':"about"})