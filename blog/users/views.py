from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import CustomUser, Blog
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm, UpdateUserForm, BlogForm


class HomeView(View):
    def get(self, request):
        return render(request, "users/home.html")


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect("home")


class LoginView(View):
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("login")

    def get(self, request):
        return render(request, "users/login.html")


class SignupView(View):
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your account."

            # Below code will connect with tokens and send verification mail to user.
            message = render_to_string(
                "users/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                "Please confirm your email address to complete the registration"
            )
        else:
            form = SignUpForm()
        return render(request, "users/signup.html", {"form": form})

    def get(self, request):
        form = SignUpForm()

        return render(request, "users/signup.html", {"form": form})


# User view will show list of total users registered currently.
class UserView(View):
    def get(self, request):
        total = CustomUser.objects.all()
        count = CustomUser.objects.count()
        context = {"count": count, "total": total}
        return render(request, "users/users.html", context)


# Blog view will show list of total blogs present currently.
class BlogView(View):
    def get(self, request):
        total = Blog.objects.all()
        count = Blog.objects.count()
        context = {"count": count, "total": total}
        return render(request, "users/blogs.html", context)


# User Detail view will show detail of each user currently registered by clicking on their first name.
class UserDetailView(View):
    def get(self, request, user_id):
        total = CustomUser.objects.all()
        user_detail = CustomUser.objects.get(pk=user_id)
        context = {"user_detail": user_detail, "total": total}
        return render(request, "users/userdetail.html", context)


# Blog Detail view will show detail of each blog currently present by clicking on blog name.
# It also contains 'update blog' and 'delete blog' feature inside it.
class BlogDetailView(View):
    def get(self, request, user_id):
        total = Blog.objects.all()
        blog = Blog.objects.get(pk=user_id)
        blog_detail = Blog.objects.get(pk=user_id)
        context = {"blog_detail": blog_detail, "total": total, "blog": blog}
        return render(request, "users/blogdetail.html", context)


# It will create a blog including all blogs fields.
class CreateBlogView(View):
    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/")

    def get(self, request):
        form = BlogForm(request.POST)
        context = {"form": form}
        return render(request, "users/create_blog.html", context)


# It will update any field of blog which user wants to update.
class UpdateBlogView(View):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        form = BlogForm(instance=blog)
        context = {"form": form, "blog": blog}
        print(blog.id)
        return render(request, "users/update_blog.html", context)

    def post(self, request, pk):
        blog = Blog.objects.get(id=pk)
        form = BlogForm(request.POST, instance=blog)
        form.save()
        return redirect("/")


# It will delete any blog which user wants to delete.
class DeleteBlogView(View):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        context = {"blog": blog}
        return render(request, "users/delete_blog.html", context)

    def post(self, request, pk):
        blog = Blog.objects.get(id=pk)
        blog.delete()
        return redirect("/")


class PasswordDoneView(View):
    def get(self, request):
        return render(request, "users/password_done.html")


class LoginRequiredView(View):
    def get(self, request):
        return render(request, "users/login_required.html")

# It will update any field of user which user wants to update.
class UpdateUserView(View):
    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        form = UpdateUserForm(instance=user)
        context = {"form": form}
        return render(request, "users/forms.html", context)

    def post(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect("/")


# It is the method which generate unique tokens for verifying registered user via email.
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "users/verification_done.html")
    else:
        return HttpResponse("Activation link is invalid!")
