from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import SignupForms, LoginForms, TaskForm, CommentForm
from django.contrib.auth import login, logout, authenticate
from .models import User, Task, Comment


# Home page
class Home(TemplateView):
    template_name = "index.html"


class SignupView(View):
    template_name = "signup.html"

    def get(self, request):
        form = SignupForms()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignupForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("tasklist")
        form = LoginForms()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForms(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("tasklist")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home_page")


class AssignTaskView(View):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        form = TaskForm()
        return render(
            request, "assign_task.html", {"form": form, "users": users}
        )

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            return redirect("tasklist")
        else:
            return render(request, "assign_task.html", {"form": form})


class TaskListView(View):
    template_name = "tasklist.html"

    def get(self, request):
        task = Task.objects.all()
        context = {"task": task}
        return render(request, self.template_name, context=context)


class TaskUpdateView(View):
    template_name = "taskupdate.html"

    def get(self, request, pk):
        task = Task.objects.filter(id=pk).first()
        if task:
            users = User.objects.exclude(id=request.user.id)
            form = TaskForm(instance=task)
            return render(
                request, self.template_name, {"form": form, "users": users}
            )

    def post(self, request, pk):
        task = Task.objects.filter(id=pk).first()
        if task:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect("tasklist")


class TaskDetailView(View):
    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        comments = Comment.objects.filter(task=task)
        form = CommentForm()
        return render(
            request,
            "taskdetail.html",
            {"task": task, "comments": comments, "form": form},
        )

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.task = task
            comment.save()
            return redirect("detailtask")
        comments = Comment.objects.filter(task=task)
        return render(
            request,
            "taskdetail.html",
            {"task": task, "comments": comments, "form": form},
        )
