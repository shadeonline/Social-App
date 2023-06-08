from rest_framework import generics
from rest_framework import mixins

from .models import *
from .serializers import *
from django.http import HttpResponseRedirect
from .tasks import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.urls import reverse
from rest_framework import status


# api/createpost/
class CreatePost(mixins.CreateModelMixin, generics.GenericAPIView):
    # Define the Post queryset
    queryset = Post.objects.all()
    # Define the PostSerializer
    serializer_class = PostSerializer

    # perform_create() is called when a new post is created
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            # Get the current user and assign the new post to them
            current_user = User.objects.get(username=self.request.user)
            record = serializer.save(user=current_user)
            # Create a thumbnail for the new post asynchronously
            make_thumbnail.delay(record.pk)
    
    # Override create method to handle redirection after a new post is created
    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            #Check if all data/arguments is valid befor creating post
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            #Create post
            response = super(CreatePost, self).create(request, *args, **kwargs)
            
            # Redirect to the home page after a new post is created
            return HttpResponseRedirect(redirect_to='/')
        else:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    # Handle POST requests
    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        return self.create(request, *args, **kwargs)

# api/posts/
class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

# URL: api/users/
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

# URL: api/user/<int:pk>
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

# URL: api/signup/
class User_signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
       # Extract user data from the request.POST QueryDict and make a mutable copy
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        print(first_name, last_name)

        try:
            # Attempt to create a new user with the provided data
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

        except IntegrityError:
            # If a user with the same username or email already exists, show an error message and redirect to signup page
            messages.error(
                request, 'An account with that username or email already exists.')
            return HttpResponseRedirect(redirect_to='/signup')

        # Check if user is authenticated, and log them out if necessary
        if request.user.is_authenticated:
            logout(request)

        # Authenticate and log in the new user
        user = authenticate(username=username, password=password)
        login(request, user)

         # Send success message to the front end and prepare response data
        messages.success(request, 'Welcome to Social!')
        response_data = {'message': 'User created successfully!'}

        return HttpResponseRedirect(redirect_to='/users')

# api/profile/<int:pk>
class UserProfile(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        # Retrieve the user ID from URL parameters
        user_id = self.kwargs.get('pk')
        if user_id:
            # Get the profile of the user with that ID if it exists
            return get_object_or_404(Profile, user_id=user_id)
        # If no user ID was provided, return the profile of the authenticated user
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        # Get the profile data using the serializer and return it in a response
        response_data = self.serializer_class(self.get_object()).data
        return Response(response_data)

    def post(self, request, *args, **kwargs):
        # Get the profile object to update
        profile = self.get_object()
        # Create a mutable copy of the request data
        data = request.data.copy()
        # Set the user ID of the profile object on the copied data to ensure it is associated with the correct user
        data['user'] = profile.user.id
        # Use the serializer to validate the updated data and save it to the database
        serializer = self.serializer_class(profile, data=data)
        if serializer.is_valid():
            serializer.save()
            # Redirect to the URL for the updated profile
            url = reverse('profile', args=[profile.user.id])  # get URL for user_profile view
            return HttpResponseRedirect(redirect_to=url)
        else:
            # If the serializer is not valid, return an error response with the validation errors
            return Response(serializer.errors, status=400)


# api/chat/<str:room>/
class ChatMessageList(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        room = self.kwargs['room']
        return ChatMessage.objects.filter(room=room)


