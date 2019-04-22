from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .forms import PostForm, ImageForm, CommentForm
from .models import Post, Image, Comment, Hashtag
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def list(request):
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    comment_form = CommentForm()
    context = {
        'posts':posts,
        'comment_form':comment_form,
    }
    return render(request, 'posts/list.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            # hashtag = post.save() 가 된 이후에 hashtag 코드가 와야함
            # 1. 게시글을 순회하면서 띄어쓰기를 잘라야함
            # 2. 자른 단어가 # 으로 시작하나?
            # 3. 이 해시태그가 기존 해시태그에 있는 건지?
            for word in post.content.split():
                # if word[0] == '#'
                if word.startswith('#'):
                    # 1
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag[0])
            		#2
            		# if word not in Hashtag.objects.all():
            		#     hashtag = Hashtag.objects.create(content = word)
            		# else:
            		#     hashtag = Hashtag.objects.get(content=word)
            		#3
            		# hashtag = Hashtag.objects.get(content=word, Hashtag.objects.create(content = word))


            
            # post = post_form.save()  # 게시글 내용 처리 끝
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
                    
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
        context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/form.html', context)
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user != request.user:
        return redirect('posts:list')
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')

@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if post.user != request.user:
        return redirect('posts:list')
        
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            # 수정 될 때는 기존의 해시태그 전체를 삭제라고 다시 등록하는 과정
            #  hashtag update
            post.hashtags.clear()
            for word in post.content.split():
                if word.startswith('#'):
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag[0])            
            
            return redirect('posts:list')
        else:
            post_form = PostForm(instance=board)
    else:
        post_form = PostForm(instance=post)
    context = {
        'post_form':post_form,
    }
    return render(request, 'posts/form.html', context)

@login_required
@require_POST
def comment_create(request, post_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_pk
        comment.save()
    return redirect('posts:list')
    
@login_required
@require_POST  
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment_user:
        return redirect('post:list')
    comment_delete()
    return redirect('post:list')
    
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 이미 해당 유저가 like 를 누른 상태면 좋아요 취소
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    # 안 눌렀다면 좋아요    
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
    
def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    posts = hashtag.post_set.order_by('-pk')
    context = {
        'hashtag': hashtag,
        'posts': posts,
    }
    return render(request, 'posts/hashtag.html', context)