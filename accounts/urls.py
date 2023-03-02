from django.urls import path

from accounts import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('user/', views.UserView.as_view()),
    path('profile/', views.UpdateProfileView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('add_admin/', views.AddAdminView.as_view()),
    path('comments/', views.AllCommentListView.as_view()),
    path('comments/confirm_comment/', views.confirm_comment),
    path('comments/reject_comment/', views.reject_comment),
]
