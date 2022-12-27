from os import link
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from core.models import Profile, Post, PostComments, PostLike, FollowProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse



def index(request):
    user = request.user
    following_user = FollowProfile.objects.filter(user = user)
    Not_following = FollowProfile.objects.exclude(user=user)
    POST = []
    for x in following_user:
        user_following = x
        post = Post.objects.filter(user__username=user_following)
        POST += post
   
    context = {
        'posts': POST,
        'Not_following': Not_following,
    }

    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username already taken")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(email=email, username=username, password=password1)
                Profile.objects.create(user=user)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                return redirect('signin')
        else:
            messages.info(request, "password doesn't matched")
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def profile(request, user_id):
    # user = request.user
    profile = Profile.objects.get(user=user_id)
    posts = Post.objects.filter(user=user_id)
    post_count = posts.count()
    following_user = FollowProfile.objects.filter(user = request.user)

    following_user = []

    for x in following_user:
        following_user.append(x)
    print(following_user)

    context = {
        'profile': profile,
        'posts': posts,
        'post_count': post_count,
        'following': following_user,
    }
    return render(request, 'profile.html', context)


def setting(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        print("heii")
        if request.FILES.get('profile_pic') == None: 
            bio = request.POST['bio']
            profile.bio = bio
            profile.save()
            print("i will")                                      
            pass

        if request.FILES.get('profile_pic') != None:
            print("done")
            image = request.FILES.get('profile_pic')
            bio = request.POST['bio']
            location = request.POST['location']

            profile.profile_pic = image
            profile.bio = bio
            profile.location = location
            profile.save()

        context = {
            'profile': profile
        }

        return render(request, 'setting.html', context)
    else:
        context = {
            'profile': profile
        } 
        return render(request, 'setting.html', context)
 

def upload_post(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        if request.FILES.get('post_pic') == None:
            pass
        if request.FILES.get('post_pic') != None:
            image = request.FILES.get('post_pic')
            caption = request.POST['caption']

            post = Post.objects.create(post=image, caption=caption, user=user, profile=profile)
        return redirect('index')
    else:
        return render(request, 'index.html')


def like_post(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    like_post = PostLike.objects.filter(user=user, post=post_id).first()
    if like_post == None:
        PostLike.objects.create(user=user, post=post, profile=profile)
        post.like += 1
        post.save()
        return redirect('/')
    else:
        post.like -= 1
        post.save()
        like_post.delete()
        return redirect('/')
       

def add_comment(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        print(post_id)
        comment = request.POST['comment']
        PostComments.objects.create(
            comment=comment,
            user=user,
            post=post,
            profile=profile,
        )
        return HttpResponseRedirect(reverse('post_detail', args=(post.id,)))
    else:
        return HttpResponseRedirect(reverse('post_detail', args=(post.id,)))


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    postcomment = PostComments.objects.filter(post=post_id)
    context = {
        'post': post,
        'postcomment': postcomment,
    }
    return render(request, 'post_detail.html', context)


def signout(request):
    logout(request)
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('signin')

    else:
         return render(request, 'signin.html')


def search(request):
    profile = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            profile = Profile.objects.filter(user__username__icontains=keyword)

    context = {
        'profile': profile,
    }
    return render(request, 'search.html', context)
        

def follow(request, user_id):
    user = request.user
    user_2 = User.objects.get(id=user_id)
    followcheck = FollowProfile.objects.filter(user=user, following_user=user_2).first()
    profile = Profile.objects.get(user=user)
    user_profile = Profile.objects.get(user=user_2)

    if followcheck == None:
        FollowProfile.objects.create(user=user, following_user=user_2)
        profile.following_count += 1
        user_profile.follower_count += 1
        profile.save()
        user_profile.save()

    else:
        followcheck.delete()
        profile.following_count -= 1
        user_profile.follower_count -= 1
        profile.save()
        user_profile.save()

    return HttpResponseRedirect(reverse('profile', args=(user_2.id,)))

