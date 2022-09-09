from django.urls import path
from .views import (HomeView,LogoutView,LoginView,SignupView,UserView,UserDetailView,
                    PasswordDoneView,UpdateUserView,BlogView,BlogDetailView,CreateBlogView,
                    LoginRequiredView,UpdateBlogView,DeleteBlogView)
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # Home page
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("users/", UserView.as_view(), name="users"),
    path("blogs/", BlogView.as_view(), name="blogs"),
    path("create/blog/", CreateBlogView.as_view(), name="create-blog"),
    path("updateblog/<str:pk>", UpdateBlogView.as_view(), name="update-blog"),
    path("deleteblog/<str:pk>", DeleteBlogView.as_view(), name="delete-blog"),
    path("login/required/", LoginRequiredView.as_view(), name="login-required"),
    path('update_user/<str:pk>/', UpdateUserView.as_view(), name="update_user"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path("user/details/<int:user_id>", UserDetailView.as_view(), name="details"),
    path("blog/details/<int:user_id>", BlogDetailView.as_view(), name="blog-details"),
    path("password-done/", PasswordDoneView.as_view(), name="password"),

    # Default Django views used below.
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password.html", success_url="/password-done/"
        ),
        name="change_password",
    ),
    path(
        "reset-password/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html"),
        name="reset_password",
    ),
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "confirm-password/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
