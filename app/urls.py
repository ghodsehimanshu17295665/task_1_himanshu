from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    Home,
    SignupView,
    LoginView,
    TaskListView,
    LogoutView,
    AssignTaskView,
    TaskDetailView,
    TaskUpdateView,
)

urlpatterns = [
    path("", Home.as_view(), name="home_page"),
    path("signup/page/", SignupView.as_view(), name="signup"),
    path("login/page/", LoginView.as_view(), name="login"),
    path("logout/page/", LogoutView.as_view(), name="logout"),
    path("task/list", TaskListView.as_view(), name="tasklist"),
    path("assign/task", AssignTaskView.as_view(), name="assigntask"),
    path("detail/task/<int:pk>/", TaskDetailView.as_view(), name="detailtask"),
    path(
        "task/<int:pk>/comments/",
        TaskDetailView.as_view(),
        name="add_comments",
    ),
    path("update/task/<int:pk>/", TaskUpdateView.as_view(), name="updatetask")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
