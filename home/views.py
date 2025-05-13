from django.shortcuts import render
from blog.models import *

# Create your views here.
def home(request):
    all_posts = Post.objects.all().order_by('-create_date')
    feature_post = all_posts.first()
    posts = all_posts[1:]
    return render(request, 'home/home.html', {'posts': posts, 'feature_post':feature_post})