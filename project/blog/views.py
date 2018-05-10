from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.db.models import Q

from .forms import PostForm
from .models import *

# Create your views here.


def date_parse(date):
    date = date.strftime('%Y-%m-%d')
    return date


class WriteView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/write.html', {'form':form})

    def post(self, request):
        form = PostForm(self.request.POST)

        if form.is_valid():

            tags = request.POST.get('hashtag')
            tag_list = []

            post = form.save()
            post.summer_field = request.POST['post']
            post.published_date = timezone.now()
            post.hashtag = tags

            for x in tags.split(','):
                tag_list.append(x)
                try:
                    tag_object = HashTag.objects.get(title=x)
                except:
                    HashTag.objects.create(title=x, nou=1)
                else:
                    HashTag.objects.filter(title=x).update(nou=tag_object.nou + 1)

            index = 1

            for x in tag_list:
                name = 'tag' + str(index)
                setattr(post, name, x)
                index += 1

            post.save()
        return redirect('blog')


class PostView(View):
    def get(self, request, post_id):
        try:
            post = SummerNote.objects.get(attachment_ptr_id=post_id)
            SummerNote.objects.filter(attachment_ptr_id=post_id).update(hits=post.hits + 1)
        except:
            raise Http404

        tag_list = []

        if (post.hashtag == ''):
            post.hashtag = None

        try:
            for x in post.hashtag.split(','):
                tag_list.append(x)

        except AttributeError as e:
            context = {'post': post}

        else:
            context = {'post': post, 'tags': tag_list}

        return render(request, 'blog/post.html', context)


class BlogView(View):
    def get(self, request):
        recent_posts = SummerNote.objects.order_by('-published_date')[:10]
        tags = HashTag.objects.order_by('-nou')[:3]

        for x in recent_posts:
            x.published_date = date_parse(x.published_date)

        context = {'recent_posts': recent_posts, 'tags': tags}
        return render(request, 'blog/blog.html', context)


class SearchView(View):
    def get(self, request):
        raise Http404

    def post(self, request):
        keyword = request.POST.get('search_title')

        result = SummerNote.objects.filter(title__contains=keyword)

        if (result):
            for x in result:
                x.published_date = date_parse(x.published_date)

        context = {'keyword': keyword, 'post': result}

        return render(request, 'blog/search.html', context)


class TagView(ListView):
    template_name = 'blog/tags.html'
    paginate_by = 10

    def get_queryset(self):
        self.keyword = self.kwargs['keyword']
        keyword = self.keyword

        post = SummerNote.objects.filter(Q(tag1__icontains=keyword) | Q(tag2__icontains=keyword) |
                                         Q(tag3__icontains=keyword)| Q(tag4__icontains=keyword) |
                                         Q(tag5__icontains=keyword)).distinct()
        self.count = 0

        if post:
            self.count = len(post)
            for x in post:
                x.published_date = date_parse(x.published_date)

        return post

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['count'] = self.count

        print(context)

        return context

