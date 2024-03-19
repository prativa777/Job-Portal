from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserProfileAPIView, HomeAPIView, JobDetailAPIView, JobApplyAPIView,\
MyJobsAPIView, ContactAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='api_register'),
    path('login/', UserLoginAPIView.as_view(), name='api_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='api_logout'),
    path('profile/', UserProfileAPIView.as_view(), name='api_profile'),
    path('home/', HomeAPIView.as_view(), name='api_home'),
    path('job/<uuid:uuid>/', JobDetailAPIView.as_view(), name='api_job_detail'),
    path('job/apply/<uuid:uuid>/', JobApplyAPIView.as_view(), name='api_job_apply'),
    path('my_jobs/', MyJobsAPIView.as_view(), name='api_my_jobs'),
    path('contact/', ContactAPIView.as_view(), name='api_contact'),

]
