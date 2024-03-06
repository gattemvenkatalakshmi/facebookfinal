from django.shortcuts import render, redirect
from .models import User, FriendRequest, Friendship,Post, Like,Comment
from .forms import UserForm, UserFormToExcludeFields,PostForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.shortcuts import get_object_or_404


# Create your views here.
def login_page(request):  

    form = UserFormToExcludeFields()
    if request.method == 'GET':
        return render(request, 'facebook/login.html', {'form': form})
    if request.method == 'POST':
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email_address=email_address)
            if check_password(password, user.password):
                print(user.first_name)
                request.session['user_email_address'] = user.email_address
                return redirect('home')
            else:
                return render(request, 'facebook/login.html', {'message': 'Incorrect Password'})
        except User.DoesNotExist:
            return render(request, 'facebook/login.html', {'message': 'Email does not exist'})
    return render(request, 'facebook/login.html', {'form': form})


def signup(request):

    form = UserForm()
    if request.method == 'GET':
        return render(request, 'facebook/signup.html', {'form': form})
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'facebook/signup.html', {'form': form})
    return render(request, 'facebook/signup.html', {'form': form})


def forgot_password(request):

    form = UserForm()
    if request.method == "POST":
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        try:
            user = User.objects.get(email_address=email_address)
            if password == confirm_password:
                hashed_password = make_password(password)
                user.password = hashed_password
                user.save()
                return redirect('login')
            else:
                return render(request, 'facebook/forgot_password.html', {'message': 'Different Password'})
        except User.DoesNotExist:
            return render(request, 'facebook/forgot_password.html', {'message': 'Email does not exist'})
    return render(request, 'facebook/forgot_password.html', {'form': form})


def home(request):

    email_address = request.session.get('user_email_address')
    if email_address is None:
        return redirect('login')
    else:
        user = User.objects.get(email_address=email_address)       
        current_user = user.id
        current_user_friend_ids = Friendship.objects.filter(
            user=current_user).values_list('friend_id', flat=True)
        current_user_friendship_ids = Friendship.objects.filter(
            friend=current_user).values_list('user_id', flat=True)
        friends_ids = set(current_user_friend_ids) | set(
            current_user_friendship_ids)
        posts = Post.objects.filter(User_id__in=friends_ids).order_by('-Created_Time')
        comments = Comment.objects.all()            
        return render(request, 'facebook/home.html', {'user': user,'posts':posts,'comments':comments})
    return redirect('home')


def logout(request):

    request.session.flush()
    return redirect('login')


def send_request(request, id):

    email_address = request.session.get('user_email_address')
    # email_address= 'gattemvenkatalakshmi@gmail.com'
    user = User.objects.get(email_address=email_address)
    from_user = user.id
    to_user = get_object_or_404(User, id=id)
    FriendRequest.objects.create(from_user=user, to_user=to_user)
    return redirect('friends')


def people_you_may_know(request):

    email_address = request.session.get('user_email_address')
    # email_address= 'gattemvenkatalakshmi@gmail.com'
    user = User.objects.get(email_address=email_address)
    current_user = user.id
    # Get IDs of users who are friends with the current user
    current_user_friend_ids = Friendship.objects.filter(
        user=current_user).values_list('friend_id', flat=True)
    current_user_friendship_ids = Friendship.objects.filter(
        friend=current_user).values_list('user_id', flat=True)
    # Get IDs of users who have sent a friend request to the current user
    friend_requests_received_ids = FriendRequest.objects.filter(
        to_user=current_user).values_list('from_user_id', flat=True)
    # Get IDs of users who have sent a friend request from the current user
    friend_requests_sent_ids = FriendRequest.objects.filter(
        from_user=current_user).values_list('to_user_id', flat=True)
    exclude_ids = set(current_user_friend_ids) | set(current_user_friendship_ids) | set(
        friend_requests_received_ids) | set(friend_requests_sent_ids)
    exclude_ids.add(current_user)
    people_you_may_know = User.objects.exclude(id__in=exclude_ids)
    return render(request, 'facebook/friends.html', {
        'people_you_may_know': people_you_may_know})


def add_friends(request, id):

    email_address = request.session.get('user_email_address')
    # email_address='gattemvenkatalakshmi@gmail.com'
    user = User.objects.get(email_address=email_address)
    current_user = user.id
    if request.method == 'POST':
        to_user = User.objects.filter(id=id).first()
        friend = Friendship.objects.create(user_id=current_user, friend_id=to_user.id)        
        # Update the friend request status
        friend_request = get_object_or_404(
            FriendRequest, from_user=to_user, to_user=current_user)  # Swapping from_user and to_user
        friend_request.status = 'accepted'
        friend_request.save()
    return redirect('view_friends')


def remove_friends_request(request, id):

    email_address = request.session.get('user_email_address')
    # email_address='gattemvenkatalakshmi@gmail.com'
    user = User.objects.get(email_address=email_address)
    current_user = user
    to_user = get_object_or_404(User, id=id)
    friend_request = get_object_or_404(
        FriendRequest, to_user=current_user, from_user_id=id)
    friend_request.status = 'removed'
    friend_request.save()
    return redirect('show_Requests')


def showing_friends_request(request):

    email_address = request.session.get('user_email_address')
    # email_address='gattemvenkatalakshmi@gmail.com'
    user = User.objects.get(email_address=email_address)
    current_user = user.id
    pending_friend_requests = FriendRequest.objects.filter(
        to_user=current_user, status='pending')
    # data = serialize('json', pending_friend_requests)
    # ans = json.loads(data)
    # for person in  pending_friend_requests:
    #     print(person.from_user)
    # return JsonResponse(ans, json_dumps_params={'indent': 4}, safe=False)
    return render(request, 'facebook/friends.html', {'pending_friend_requests': pending_friend_requests})


def view_friends(request):

    email_address = request.session.get('user_email_address')
    # email_address= 'gattemvenkatalakshmi@gmail.com'

    user = User.objects.get(email_address=email_address)
    current_user = user.id

    current_user_friend_ids = Friendship.objects.filter(
        user=current_user).values_list('friend_id', flat=True)
    current_user_friendship_ids = Friendship.objects.filter(
        friend=current_user).values_list('user_id', flat=True)
    friends_ids = set(current_user_friend_ids) | set(
        current_user_friendship_ids)
    friends_to_user = User.objects.filter(id__in=friends_ids)
    # data = serialize('json', friends_to_user)
    # ans = json.loads(data)
    # return JsonResponse(ans, json_dumps_params={'indent': 4}, safe=False)
    
    return render(request, 'facebook/friends.html', {'friends_to_user': friends_to_user})


def remove_friend(request, friend_id):
    current_user = request.session.get('user_email_address')
    to_user = get_object_or_404(User, id=friend_id)
    friendship = Friendship.objects.filter(
        from_user=current_user, to_user_id=to_user).first()
    if friendship:
        friendship.delete()
    return redirect('friends')

def view_profile(request):
    email_address = request.session.get('user_email_address')
    # email_address= 'gattemvenkatalakshmi@gmail.com'
    user = User.objects.get(email_address=email_address)   
    return render(request,'facebook/profile.html',{'user':user})


def create_post(request):   
    user_email = request.session.get('user_email_address')   
    # Check if user_email exists in the session
    if user_email:
        try:
            user = User.objects.get(email_address=user_email)
        except User.DoesNotExist:
            user = None
    else:
        user = None
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # If user is authenticated, associate user with the post
            if user:
                post = form.save(commit=False)
                post.User_id = user
                post.save()
                return redirect('profile')
            else:
                # Handle case where user is not found
                return redirect('login')  # Redirect to login page or handle the scenario appropriately
        else:
            return render(request, 'facebook/post.html', {'message': 'File is not valid'})  
    else:
        form = PostForm()       
    return render(request, 'facebook/post.html', {'form': form})

def view_all_my_posts(request):
    email_address = request.session.get('user_email_address')
    user = User.objects.get(email_address=email_address)
    posts = Post.objects.filter(User_id =user.id)   
    comments =Comment.objects.all()
    # data = serialize('json',posts)
    # ans = json.loads(data)
    # return JsonResponse(ans, json_dumps_params={'indent': 4}, safe=False)
    return render(request,'facebook/profile.html',{'user':user,'posts':posts,'comments':comments})

def like(request, id):
    email_address = request.session.get('user_email_address')
    # email_address= 'gattemvenkatalakshmi@gmail.com'
    user = User.objects.get(email_address=email_address)
    post = get_object_or_404(Post, id=id)
    current_likes = post.likes
    liked = Like.objects.filter(from_user_id=user.id, post_id=post).count()
    if not liked:
        Like.objects.create(from_user_id=user, post_id=post)
        current_likes += 1
    else:
        Like.objects.filter(from_user_id=user, post_id=post).delete()
        current_likes -= 1  
    post.likes = current_likes     
    post.save() 
    return redirect('home')


# def save_comment(request, id):
#     email_address = request.session.get('user_email_address')
#     # email_address= 'gattemvenkatalakshmi@gmail.com'
#     user = User.objects.get(email_address=email_address)
#     current_user = user.id
#     if request.method == 'POST':
#         user = current_user
#         post = Post.objects.get(id=id) 
#         Comment_text= request.POST.get('Comment_text')
#         print(Comment_text)
#         Comment.objects.create(from_user_id=user,post_id=post.id,Comment_text= Comment_text)
#         print(Comment)
#         return redirect('home')
#     return redirect('home')
def save_comment(request, id):
    if request.method == 'POST':
        email_address = request.session.get('user_email_address')
        if email_address:
            try:
                user = User.objects.get(email_address=email_address)
                post = Post.objects.get(id=id)
                Comment_text = request.POST.get('Comment_text')
                Comment.objects.create(from_user_id=user, post_id=post, Comment_text=Comment_text)
            except (User.DoesNotExist, Post.DoesNotExist) as e:
                print("User or Post does not exist:", e)
        return redirect('home')
    else:
        return redirect('home')

      


