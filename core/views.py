from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages # used to send message to frontend
from .models import Profile, Post, LikePost, Follower, Comment
from django.contrib.auth.decorators import login_required #only open pages if login
from django.contrib.auth import get_user_model
from itertools import chain
import random 


User = get_user_model()
# Create your views here.
@login_required(login_url ='signin')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user= user_object)
    
    user_following_list=[]
    feed = []
    img_feed=[]
    
    user_following = Follower.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
      
    
    for usernames in user_following_list:
        user_object = User.objects.get(username=usernames)
        feed_list_prof = Profile.objects.filter(user=user_object)
        feed_lists= Post.objects.filter(user=usernames)
        feed.append(feed_lists)
        img_feed.append(feed_list_prof)

    
    feed_list = list(chain(*feed))
    img_list = list(chain(*img_feed))
        
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    
    
    comment_feed = Comment.objects.all()
    
    
    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list ,'img_list':img_list,'suggestions_profile':suggestions_username_profile_list[:3], 'comment_feed':comment_feed } )


def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pw']
        password2 = request.POST['pw2'] 
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
                
        else:
            messages.info(request, 'Password Not matching')
            return  redirect('signup')
            
            
        # return render(request, 'index.html')
        
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['pw']
        
        user=auth.authenticate( username=username , password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
def logout(request):
    auth.logout(request)
    return redirect('signin')
    messages.info(request, 'You have been logged out')

@login_required(login_url='signin')   
def settings(request):
    
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            job = request.POST['job']

            

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.job=job
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            job = request.POST['job']
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.job=job
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'settings.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    username  = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id = post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, username = username).first()

    if like_filter == None:
        status='liked'
        new_like = LikePost.objects.create(post_id=post_id, username = username, stats=status)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    
    else :
        current_post = LikePost.objects.get(username = username, post_id=post_id)
        if current_post.stats == 'liked' :
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1
            post.save()
            return redirect('/')
        else :
            post.no_of_dislikes = post.no_of_dislikes - 1
            post.no_of_likes = post.no_of_likes + 1
            post.save()
            current_post.stats='liked'
            current_post.save()
            return redirect('/')
            
    return redirect('/')

@login_required(login_url='signin')
def dislike_post(request):
    username  = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id = post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, username = username ).first()
    if like_filter == None:
        status='disliked'
        new_like = LikePost.objects.create(post_id=post_id, username = username, stats=status)
        new_like.save()
        post.no_of_dislikes = post.no_of_dislikes + 1
        post.save()
        return redirect('/')
    
    else :
        current_post = LikePost.objects.get(username = username, post_id=post_id)
        if current_post.stats == 'disliked' :
            like_filter.delete()
            post.no_of_dislikes = post.no_of_dislikes - 1
            post.save()
            return redirect('/')
        else :
            post.no_of_dislikes = post.no_of_dislikes + 1
            post.no_of_likes = post.no_of_likes - 1
            post.save()
            current_post.stats='disliked'
            current_post.save()
            return redirect('/')
    return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user=pk
    
    if Follower.objects.filter(follower=follower, user=user).first():
        button_text='Unfollow'
    else:
        button_text='Follow'
        
    user_followers=len(Follower.objects.filter(user=pk))
    user_following=len(Follower.objects.filter(follower=pk))
        
    context = {
        'user_object' : user_object,
        'user_profile' :  user_profile,
        'num_posts' : user_post_length,
        'user_posts'   : user_posts,
        'button_text' : button_text,
        'user_followers' :user_followers,
        'user_following' : user_following,
        
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
   if request.method == 'POST':
       follower=request.POST['follower']
       user= request.POST['user']
       
       if Follower.objects.filter(follower=follower, user=user).first():
           delete_follower =Follower.objects.get(follower=follower, user=user)
           delete_follower.delete()
           return redirect('/profile/'+user)
       else:
           new_follower = Follower.objects.create(follower=follower, user=user)
           new_follower.save()
           return redirect('/profile/'+user)
           
   else:
       return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    if request.method =='POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        
        
        username_profile = []
        username_profile_list =[]
        
        for users in username_object:
            username_profile.append(users.id)
            
        for ids in username_profile:
            profile_list=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)
        
        username_profile_list = list(chain(*username_profile_list))
        
    return  render(request, 'search.html',{'profile_list':username_profile_list,'user_profile':user_profile})

@login_required(login_url='signin')
def commenting(request):
    
    if request.method == 'POST':
        comment=request.POST['comment']
        poster = request.POST['poster']
        commenter = request.POST['commenter']
        post_id= request.POST['post_id']
        
        if len(comment)==0:
            messages.info(request, 'Enter a Comment First')
            return redirect('/')
        else:
            new_comment = Comment.objects.create(poster=poster, commenter=commenter, comment=comment , post_id = post_id)
            new_comment.save()
    
    return redirect('/')