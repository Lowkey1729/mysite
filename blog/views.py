import json

from django.core import serializers
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from blog.models import Post


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

    return HttpResponse(serializers.serialize('json', _post))
