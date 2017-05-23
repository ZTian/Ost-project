from .models import Reservation, Resource
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserRegisterForm, ResourceCreateForm, ReservationCreateForm, ReserveResourceForm, TagCreateForm
from .models import Resource, Tag
from django.http import HttpResponse
from django.views import generic
import datetime

def index(request):
    all_reservations = Reservation.objects.all().order_by('start_time')
    reverse_reservations = Reservation.objects.all().order_by('-start_time')
    all_resources = []
    filter_reservations = []
    if reverse_reservations:
        for reservation in reverse_reservations:
            if reservation.resource not in all_resources:
                all_resources.append(reservation.resource)
    for reservation in all_reservations:
        if reservation.date_time > datetime.datetime.today().date():
            filter_reservations.append(reservation)
        if reservation.end_time > datetime.datetime.today().time() and reservation.date_time == datetime.datetime.today().date():
            filter_reservations.append(reservation)
    rest_resources = Resource.objects.all()
    for resource in rest_resources:
        if resource not in all_resources:
            all_resources.append(resource)
    reservation_log=[]
    for resource in all_resources:
        reservation_log.append(Reservation.objects.filter(resource=resource).count())
    zip_all = zip(all_resources,reservation_log)
    context = {
        'all_reservations': filter_reservations,
        'zip_all':zip_all,
    }
    return render(request, 'reserve/index.html', context)


# show the detail of the reservation
def detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render(request, 'reserve/detail.html', {'reservation': reservation})

def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    all_reservation = Reservation.objects.filter(resource=resource).order_by('date_time','start_time')
    reservation_list = []
    tag_list = Tag.objects.filter(resource__id=resource_id)
    for reservation in all_reservation:
        if reservation.date_time > datetime.datetime.today().date():
            reservation_list.append(reservation)
        if reservation.end_time > datetime.datetime.today().time() and reservation.date_time == datetime.datetime.today().date():
            reservation_list.append(reservation)
    context = {
        'resource': resource,
        'reservation_list':reservation_list,
        'tag_list':tag_list
    }
    return render(request, 'reserve/resource.html', context)


class ReserveCreate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_class = ReservationCreateForm
    template_name = "reserve/reservation_form.html"
    success_url = "/reserve"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if Reservation.objects.filter(owner=self.request.user).count() > 1:
            return HttpResponse("<h1>Already have one reservation!</h1>")
        return super(ReserveCreate, self).form_valid(form)


class ResourceCreate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Resource
    form_class = ResourceCreateForm
    template_name = "reserve/resource_form.html"
    success_url = "/reserve"

    def form_valid(self, form):
        form.instance.resource_owner = self.request.user
        return super(ResourceCreate, self).form_valid(form)

class TagCreate(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Resource
    form_class = TagCreateForm
    template_name = "reserve/tag_form.html"
    success_url = "/reserve"


class ResourceUpdate(UpdateView):
    model = Resource
    fields = [
        'title',
        'start_time',
        'end_time',
        'tag',
        'resource_logo',
        'resource_description',
    ]


def reserve_delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == "POST":
        reservation.delete()
        return redirect("/reserve")
    return render(request,"reserve/delete_reservation.html", {"reservation":reservation})



class ReserveResourceCreate(CreateView):
    form_class = ReserveResourceForm
    template_name = "reserve/reserve_resource.html"
    success_url = "/reserve"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        pk=self.kwargs['pk']
        resource = Resource.objects.filter(pk=pk).first()
        form.instance.resource = resource

        start_time = form.cleaned_data.get("start_time")
        end_time = form.cleaned_data.get("end_time")
        date_time = form.cleaned_data.get("date_time")
        if start_time > resource.end_time:
            return HttpResponse("<h1>Not available at that time! Please go back</h1>")
        if end_time < resource.start_time:
            return HttpResponse("<h1>Not available at that time! Please go back</h1>")
        reservation_list = Reservation.objects.filter(resource=resource)
        for reservation in reservation_list:
            if date_time == reservation.date_time:
                if not (end_time <= reservation.start_time and start_time >= reservation.end_time):
                    return HttpResponse("<h1>Not available at that time! Please go back</h1>")
        return super(ReserveResourceCreate, self).form_valid(form)


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/reserve")
    return render(request, "reserve/form.html", {"form": form, "title": title})

def error_message(request):
    return HttpResponse("<h1>Error")


def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/reserve")
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "reserve/form.html", context)

def logout_view(request):
    title = "Logout"
    logout(request)
    if not request.user.is_authenticated:
        return redirect("/reserve")
    return render(request, "reserve/form.html", {"title":title})

def user_detail(request, username):
    user = User.objects.get(username=username)
    all_reservations = Reservation.objects.filter(owner=user)
    all_resources = Resource.objects.filter(resource_owner=user)
    context = {
        "all_reservations":all_reservations,
        "all_resources":all_resources,
        "user":user
    }
    return render(request, "reserve/user.html", context)

def tag_info(request, tag_id):
    tag = Tag.objects.filter(pk=tag_id).first()
    all_resources = Resource.objects.filter(tag__id=tag_id)
    return render(request, "reserve/tag.html", {"tag":tag, "all_resources":all_resources})

def resource_comment(request, object_pk):
    resource = Resource.objects.get(pk=object_pk)
    reservation_list = Reservation.objects.filter(resource=resource)
    return HttpResponse("<h1>Hello")

def search(request):
    query = request.GET.get("q")
    if query:
        query_list = Resource.objects.filter(title__icontains=query)
    return HttpResponse("<h1>No idea")