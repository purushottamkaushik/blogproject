from django.shortcuts import render, get_object_or_404

from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import EmailForm, CommentForm

from django.core.mail import send_mail
import taggit
from taggit.models import Tag


# Create your views here.

def display_post(request, tag_slug=None):
    post = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])

    paginator = Paginator(post, 2)
    page_number = request.GET.get('page')

    try:
        post = paginator.page(page_number)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', context={'post': post, 'tag': tag})


def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )

    comments = post.comments.filter(active=True)
    commentsubmit = False

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            newcomment = form.save(commit=False)
            newcomment.post = post
            newcomment.save()
            commentsubmit = True


    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html',
                  {'post': post, 'form': form, 'comments': comments, 'csubmit': commentsubmit})


def sendMail(request, id):
    post = get_object_or_404(Post, id=id, status='published')

    form = EmailForm()
    sent = False

    if request.method == "POST":
        form = EmailForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            subject = cd['name'] + "(" + cd['sender'] + " )\"recommends you to read " + str(post.title)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = post_url + "\n\n\n" + cd['message']
            FROM = cd['sender']
            TO = cd['to']
            to = [TO ,]

            send_mail(subject, message, FROM, to, fail_silently=False)
            sent = True
    else:
        form = EmailForm()

    return render(request, 'blog/send_mail.html', {'form': form, 'post': post, 'sent': sent})
