import json

from django.core import serializers
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.mail import send_mail

from blog.forms import EmailPostForm
from blog.models import Post, Comment
from blog.pagination import StandardPagination
from blog.serializers import PostSerializer, CommentSerializer


# Create your views here.
def post_list(request):
    _post_list = Post.published.all()
    paginator = Paginator(_post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    serialized_data = json.loads(serialize('json', posts))
    return JsonResponse(serialized_data, safe=False)


def post_detail(request, year, month, day, post):
    _post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    serializer = PostSerializer(_post)
    print(serializer)
    return JsonResponse(serializer.data, safe=False)


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if not form.is_valid():
            form = EmailPostForm()
        else:
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cleaned_data['name']({cleaned_data['email']})}"
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cleaned_data['name']}\'s comments: {cleaned_data['comments']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cleaned_data['to']]
            )

            sent = True


class PostListView(ListAPIView):
    queryset = Post.objects.annotate(total_comments=Count('comments'))
    serializer_class = PostSerializer
    pagination_class = StandardPagination
    # context_object_name = 'posts'
    # paginate_by = 3


class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.prefetch_related('comments').annotate(total_comments=Count('comments'))
    serializer_class = PostSerializer
    pagination_class = StandardPagination
    

class CommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

