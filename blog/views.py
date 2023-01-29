import os
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from uuid import uuid4
from .models import Post, Comment, Category
from .forms import (EmailPostForm, CommentForm, SearchForm, CategoryCreateForm,
    PostCreateForm, CategoryUpdateForm, PostUpdateForm, NewsletterForm)
from .decorators import user_is_superuser
from users.models import SubscribedUsers

RECORD_TEMPLATE = 'blog/post/new_record.html'

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag,
                   'type': 'post'})

def category(request, category: str):
    matching_category = Post.published.filter(category__category_slug=category).all()
    
    return render(
        request=request,
        template_name='blog/post/list.html',
        context={
            'posts': matching_category,
            'type': 'category'
        }
    )
  
def post_detail(request, year, month, day, post, tag_slug=None):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             post_slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    author = post.author
    # List of  active comments for this post
    tag = None
    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])
    
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    similar_posts = post.tags.similar_objects()
    return render(request,
                  'blog/post/detail.html',
                  {'post':post,
                   'comments': comments,
                   'form': form,
                   'similar_posts':similar_posts,
                   'tag': tag,
                   'author': author})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'bgashebr@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create a comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
        messages.success(request, f'Comment created successfully')
        redirect('/')
    
    else:
        for error in list(form.errors.values()):
            messages.error(request, error)

    return render(request, 'blog/post/comment.html',
                  {
                      'post': post,
                      'form': form,
                      'comment': comment
                  })

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    
    return render(request, 'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
    
def new_category(request):
    if request.method == 'POST':
        form = CategoryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category created successfully')
            return redirect('/')
    else:
        form = CategoryCreateForm()
            
    return render(
        request=request,
        template_name=RECORD_TEMPLATE,
        context={
            'object': 'Category',
            'form': form,
        }
    )

def new_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Post created successfully.')
            return redirect('/')
    else:
        form = PostCreateForm()
    return render(
        request=request,
        template_name=RECORD_TEMPLATE,
        context={
            'object': 'Post',
            'form': form
        }
    )

def category_update(request, category):
    matching_category = Category.objects.filter(slug=category).first()
    
    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, request.FILES, instance=matching_category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category updated successfully.')
            return redirect('/')
    else:
        form = CategoryUpdateForm(instance=matching_category)
        
        return render(
            request=request,
            template_name='blog/post/new_record.html',
            context={
                'object': 'Category',
                'form': form
            }
        )

def category_delete(request, category):
    matching_category = Category.objects.filter(slug=category).first()
    
    if request.method == 'POST':
        matching_category.delete()
        messages.success(request, f'Category deleted successfully.')
        return redirect('/')
    else:
        return render(
            request=request,
            template_name='blog/post/confirm_delete.html',
            context={
                'object': matching_category,
                'type': 'Category'
            }
        )

def post_update(request, category, post):
    matching_post = Post.published.filter(category__category_slug=category, post_slug=post).first()
    
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance=matching_post)
        if form.is_valid():
            form.save()
            messages.success(request, f'Post updated successfully')
            return redirect(matching_post.get_absolute_url())
    
    else:
        form = PostUpdateForm(instance=matching_post)
    
        return render(request=request, template_name=RECORD_TEMPLATE,
                      context={
                          'object': 'Post',
                          'form': form
                      })


def post_delete(request, category, post):
    matching_post = Post.published.filter(category__category_slug=category, post_slug=post).first()
    if request.method == 'POST':
        matching_post.delete()
        messages.success(request, f'Category deleted successfully.')
        return redirect('/')
    else:
        return render(
            request=request,
            template_name='blog/post/confirm_delete.html',
            context={
                'object': matching_post,
                'type': 'post',
            }
        )

@csrf_exempt
@user_is_superuser
def upload_image(request, category: str=None, post: str=None):
    if request.method != 'POST':
        return JsonResponse({'Error Message': 'Wrong request'})
    # If it's not category and not post, handle it differently
    matching_post = Post.published.filter(category__category_slug=category, post_slug=post).first()
    if not matching_post:
       return JsonResponse({'Error Message': f"Wrong category ({category}) or post ({post})"})
    
    file_obj = request.FILES['file']
    file_name_suffix = file_obj.name.split(".")[-1]
    if file_name_suffix not in ['jpg', 'png', 'gif', 'jpeg']:
        return JsonResponse({"Error Message": f"Wrong file suffix ({file_name_suffix}), supported are .jpg, .png, .gif, .jpeg"})
    
    file_path = os.path.join(settings.MEDIA_ROOT, 'Category', matching_post.category.slug, matching_post.slug, file_obj.name)
    if os.path.exists(file_path):
        file_obj.name = str(uuid4()) + '.' + file_name_suffix
        file_path = os.path.join(settings.MEDIA_ROOT, 'Category', matching_post.category.slug, matching_post.slug, file_obj.name)
        
    print(f'url: {file_path}')
    with open(file_path, 'wb+') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
            
        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': os.path.join(settings.MEDIA_URL, 'Category', matching_post.category.slug, matching_post.slug, file_obj.name)
        })
        
@user_is_superuser
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')
            
            mail = EmailMessage(subject, email_message, f'BGA <{request.user.email}>', bcc=receivers)
            mail.content_subtype = 'html'
            
            if mail.send():
                messages.success(request, 'Email sent successfully')
                return redirect('blog:newsletter')
            else:
                messages.error(request, 'There was an error sending email.')
                return redirect('blog:newsletter')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    
    form = NewsletterForm()
    form.fields['receivers'].initial = ', '.join([active.email for active in SubscribedUsers.objects.all()])
    
    return render(request=request, template_name='blog/post/newsletter.html',
                  context={
                      'form': form
                  })