from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from Blog.models import Comment

# Create your views here.

@login_required
def add_reply(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent')
        parent_comment = get_object_or_404(Comment, id=parent_id)
        Comment.objects.create(
            post_id=post_id,
            author=request.user,
            content=content,
            parent=parent_comment,
        )
        return redirect('Blog:single_post', id=post_id)
    return redirect('Blog:single_post', id=post_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    post_id = comment.post.id
    comment.delete()
    return redirect('Blog:single_post', id=post_id)