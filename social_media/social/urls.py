from django.urls import include, path
from . import views
from . import api


urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.user_list, name="discover"),
    path('user/<int:pk>', views.user_profile, name="profile"),
    path('login/', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('signup/', views.user_signup, name="signup"),

    # API
    path('api/createpost/', api.CreatePost.as_view(), name="post_api"),
    path('api/posts/', api.PostList.as_view(), name="posts_api"),
    path('api/users/', api.UserList.as_view(), name="users_api"),
    path('api/user/<int:pk>', api.UserDetail.as_view(), name="users_api"),
    path('api/signup/', api.User_signup.as_view(), name="signup_api"),
    path('api/profile/<int:pk>', api.UserProfile.as_view(), name='profile_update'),
    path('api/chat/<str:room>/', api.ChatMessageList.as_view(), name='chat_messages_api'),

    # path('chat/', views.chat, name='chat'),
    path('chat/<str:room_name>/<int:pk>', views.chatroom, name='chatroom'),
]
