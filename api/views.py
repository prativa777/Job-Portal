from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from .serializers import UserProfileSerializer, UserRegistrationSerializer
from apps.account.models import UserProfile

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "User logged in successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "User logged out successfully."}, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):
    def get(self, request):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.core.models import Job, JobApplication, Category
from apps.core.forms import ContactForm
from apps.core.pagination import CustomPagination
from apps.commons.utils import get_base_url, is_profile_complete

# Serializers
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'

# APIs
class HomeAPIView(APIView):
    def get(self, request):
        category = request.GET.get('category')
        search = request.GET.get('search')
        jobs_filter = {"is_active": True}
        exclude_filter = dict()
        if request.user.is_authenticated:
            exclude_filter = {"job_applications__user": request.user}
        if category:
            jobs_filter.update(category__uuid=category)
        if search:
            jobs_filter.update(title__icontains=search)
        jobs = Job.objects.filter(**jobs_filter).exclude(**exclude_filter).order_by('id')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

class JobDetailAPIView(APIView):
    def get(self, request, uuid):
        try:
            job = Job.objects.get(uuid=uuid, is_active=True)
            serializer = JobSerializer(job)
            return Response(serializer.data)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

class JobApplyAPIView(APIView):
    def post(self, request, uuid):
        try:
            job = Job.objects.get(uuid=uuid)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated and is_profile_complete(request.user.profile):
            JobApplication.objects.get_or_create(user=request.user, job=job, defaults={"status": "APPLIED"})
            return Response({"message": "Job applied successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Please log in and complete your profile to apply for this job"}, status=status.HTTP_403_FORBIDDEN)

class MyJobsAPIView(APIView):
    def get(self, request):
        status = request.GET.get("status")
        filter_dict = dict(user=request.user)
        if status:
            filter_dict.update(status=status)
        job_applications = JobApplication.objects.filter(**filter_dict)
        serializer = JobApplicationSerializer(job_applications, many=True)
        return Response(serializer.data)

class ContactAPIView(CreateAPIView):
    serializer_class = ContactForm
    # queryset = ContactForm.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contact form submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Views
class HomeView(ListView):
    template_name = "core/home.html"
    pagination_class = CustomPagination

    def get_pagination(self):
        return self.pagination_class()

    def get_queryset(self):
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        job_filter = {"is_active": True}
        exclude = dict()
        if self.request.user.is_authenticated:
            exclude = {"job_applications__user": self.request.user}
        if category:
            job_filter.update(category__uuid=category)
        if search:
            job_filter.update(title__icontains=search)
        return Job.objects.filter(**job_filter).exclude(**exclude).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        pagination = self.get_pagination()
        qs = pagination.get_paginated_qs(view=self)
        paginated_qs = pagination.get_nested_pagination(qs, nested_size=2)
        context['job_lists'] = paginated_qs
        context['categories'] = Category.objects.all()
        page_number, page_str = pagination.get_current_page(view=self)
        context[page_str] = 'active'
        context["next_page"] = page_number + 1
        context["prev_page"] = page_number - 1
        context['base_url'] = get_base_url(request=self.request)
        if page_number >= pagination.get_last_page(view=self):
            context["next"] = "disabled"
        if page_number <= 1:
            context["prev"] = "disabled"
        context['home_active'] = 'active'
        return context

class JobDetailView(DetailView):
    template_name = 'core/job_detail.html'
    queryset = Job.objects.filter(is_active=True)
    slug_field = 'uuid'  # This must be a unique field from the table
    slug_url_kwarg = 'uuid'  # This must be exactly from the url
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Job Detail"
        return context

@login_required
def job_apply(request, uuid):
    try:
        job = Job.objects.get(uuid=uuid)
    except Job.DoesNotExist:
        messages.error(request, "Something Went Wrong!!")
        return redirect('home')
    if is_profile_complete(request.user):  # Apply for Job
        JobApplication.objects.get_or_create(user=request.user, job=job, defaults={"status": "APPLIED"})
        messages.success(request, f"You Have Successfully Applied For The Role Of {job.title}")
        return redirect('home')
    messages.error(request, "Please Activate Your Account And Complete Your Profile !!")
    return redirect('home')

@method_decorator(login_required, name='dispatch')
class MyJobsView(ListView):
    template_name = 'core/my_jobs.html'
    context_object_name = 'job_applications'

    def get_queryset(self):
        status = self.request.GET.get("status")
        filter_dict = dict(user=self.request.user)
        if status:
            filter_dict.update(status=status)
        return JobApplication.objects.filter(**filter_dict)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = ["APPLIED", "SCREENING", "SHORT_LISTED", "REJECTED", "SELECTED"]
        context["my_jobs_active"] = 'active'
        return context

class ContactView(CreateView):
    template_name = 'core/contact.html'
    success_url = reverse_lazy('contact')
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "We Have Received Your Response")
            return self.form_valid(form)
        else:
            messages.error(request, "Something Went Wrong")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Contact Us"
        context['contact_active'] = 'active'
        return context
