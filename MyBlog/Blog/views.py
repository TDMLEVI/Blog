from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator
from django.views import View
from .models import Post, Category, ContentBlock, Comment, Tag
from .forms import (
    CommentForm,
    PostForm,
    ContentBlockForm,
)
from datetime import timedelta

class TrendingPostsMixin:
    def get_trending_posts(self):
        last_7_days = timezone.now() - timedelta(days=7)
        return Post.objects.filter(last_viewed__gte=last_7_days).order_by('-views')[:5]

class PostViewTrackingMixin:
    def track_post_views(self, post):
        session = self.request.session
        post_id = str(post.id)  # Convert post id to string for session storage

        # Check if the post id is already in the session (i.e., viewed by this user)
        if not session.get(f'viewed_post_{post_id}'):
            post.increment_views()  # Increment views only if not already viewed
            session[f'viewed_post_{post_id}'] = True  # Mark post as viewed

class BlogListView(PostViewTrackingMixin, TrendingPostsMixin, ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        posts = Post.objects.order_by('-created_at')
        
        # Track views for all posts in the queryset
        for post in posts:
            self.track_post_views(post)
            
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'first_post': self.object_list.first(),
            'remaining_posts': self.object_list[1:self.paginate_by],
            'content_blocks': ContentBlock.objects.filter(post__in=self.object_list).order_by('order'),
            'popular_posts': Post.objects.order_by('-views')[:5],
            'trending_posts': self.get_trending_posts(),
            'latest_posts': Post.objects.order_by('-created_at')[:5],
            'tags': Tag.objects.all(),
        })

        context.update(self.get_category_posts('Culture', 'culture'))
        context.update(self.get_category_posts('Business', 'business'))
        context.update(self.get_category_posts('Lifestyle', 'lifestyle'))

        return context

    def get_trending_posts(self):
        last_7_days = timezone.now() - timedelta(days=7)
        return Post.objects.filter(last_viewed__gte=last_7_days).order_by('-views')[:5]

    def get_category_posts(self, category_name, context_key):
        category = Category.objects.get(name=category_name)
        return {
            f'{context_key}_first_post': Post.objects.filter(category=category).order_by('-created_at').first(),
            f'{context_key}_remaining_posts': Post.objects.filter(category=category).order_by('-created_at')[1:5],
        }


class SinglePostView(PostViewTrackingMixin, DetailView):
    model = Post
    template_name = 'blog/single_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_object(self):
        post = super().get_object()
        self.track_post_views(post)  # Call the mixin method to track views
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'content_blocks': self.object.content_blocks.all(),
            'related_posts': Post.objects.filter(category=self.object.category).exclude(id=self.object.id)[:5],
            'categories': Category.objects.all(),
            'tags': Tag.objects.all(),
            'comment_form': CommentForm(),
            'root_comments': self.object.comments.filter(parent__isnull=True),
            'total_comments': self.object.comments.count(),
            'total_views': self.object.views,  # Pass total views
        })
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            comment.save()
            return redirect('Blog:single_post', id=post.id)
        return self.render_to_response(self.get_context_data(form=form))

class CategoryPostsView(PostViewTrackingMixin, ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        posts = Post.objects.filter(category=self.category).order_by('-created_at')
        
        # Track views for all posts in the queryset
        for post in posts:
            self.track_post_views(post)
            
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category': self.category,
            'categories': Category.objects.all(),
            'popular_posts': Post.objects.order_by('-views')[:5],
            'trending_posts': self.get_trending_posts(),
            'latest_posts': Post.objects.order_by('-created_at')[:5],
            'tags': Tag.objects.all(),
        })
        return context

    def get_trending_posts(self):
        last_7_days = timezone.now() - timedelta(days=7)
        return Post.objects.filter(last_viewed__gte=last_7_days).order_by('-views')[:5]
    
class SearchView(PostViewTrackingMixin, TrendingPostsMixin, View):
    def get(self, request):
        query = request.GET.get('q', '')
        posts = Post.objects.filter(Q(title__icontains=query) | Q(intro__icontains=query)).order_by('-created_at') if query else Post.objects.none()

        # Track views for all posts in the search results
        for post in posts:
            self.track_post_views(post)
        
        paginator = Paginator(posts, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'posts': page_obj,
            'query': query,
            'popular_posts': Post.objects.order_by('-views')[:5],
            'trending_posts': self.get_trending_posts(),
            'latest_posts': Post.objects.order_by('-created_at')[:5],
            'tags': Tag.objects.all(),
        }

        return render(request, 'blog/search-result.html', context)

@login_required
def create_post(request):
    ContentBlockFormSet = inlineformset_factory(Post, ContentBlock, form=ContentBlockForm, extra=1, can_delete=True)

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        formset = ContentBlockFormSet(request.POST, request.FILES)

        if post_form.is_valid() and formset.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    content_block = form.save(commit=False)
                    content_block.post = new_post
                    content_block.save()

            return redirect('Blog:single_post', id=new_post.id)
    else:
        post_form = PostForm()
        formset = ContentBlockFormSet()

    return render(request, 'blog/create_post.html', {'post_form': post_form, 'formset': formset})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    ContentBlockFormSet = inlineformset_factory(Post, ContentBlock, form=ContentBlockForm, extra=0, can_delete=True)

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        formset = ContentBlockFormSet(request.POST, request.FILES, instance=post)

        if post_form.is_valid() and formset.is_valid():
            post_form.save()
            formset.save()
            return redirect('Blog:single_post', id=post.id)
    else:
        post_form = PostForm(instance=post)
        formset = ContentBlockFormSet(instance=post)

    return render(request, 'blog/edit_post.html', {'post_form': post_form, 'formset': formset})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    post.delete()
    return redirect('Blog:blog_list')