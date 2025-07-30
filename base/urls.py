from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.home,name='home'),
    path('rate-logs/',views.rate_logs,name='logs'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('docs/', TemplateView.as_view(template_name="base/docs.html"), name='api_docs'),

]
