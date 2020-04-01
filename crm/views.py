from django import forms
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


# Create your views here.
from .models import *
from .forms import FamilyMemberForm, FamilyMemberFormSet, OrderForm

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    applicants = Applicant.objects.all().order_by('-date_created')
    orders = Order.objects.all().order_by('-date_created')
    total_applicant = applicants.count()

    pending = orders.filter(status='Pending').count()
    approved = orders.filter(status='Approved').count()
    rejected = orders.filter(status='Rejected').count()

    context = {
        'applicants':applicants,
        'orders':orders,
        'total_applicant':total_applicant,
        'pending':pending,
        'approved':approved,
        'rejected':rejected,
        'dashboard_sb':"active",
        'applications_sb':"active",
        'products_sb':"active",
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products':products})

@login_required(login_url='login')
def customers(request, pk):
    customer = Applicant.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
    }
    return render(request, 'customer.html', context)

@login_required(login_url='login')
def PlaceOrder(request, pk):
    OrderFormSet = inlineformset_factory(Applicant, Order, fields=('product', 'status'), max_num=1, can_delete=False)
    customer = Applicant.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'place_order.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'update_order.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'delete_order.html', context)

class ApplicationList(ListView):
    model = Applicant
    template_name = 'application/application_list.html'

class ApplicationCreate(CreateView):
    model = Applicant
    fields = ['dun', 'salutation', 'first_name', 'last_name', 'dob',
    'gender', 'nric', 'email', 'phone', 'alt_phone', 'job_title', 'salary',
    'marital_status', 'address1', 'address2', 'postal_code', 'city',
    'state']
    template_name = 'application/application_form.html'
    success_url = reverse_lazy('application-list')

    def get_context_data(self, **kwargs):
        data = super(ApplicationCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = FamilyMemberFormSet(self.request.POST)
        else:
            data['familymembers'] = FamilyMemberFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()
            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(ApplicationCreate, self).form_valid(form)

class ApplicationEdit(UpdateView):
    model = Applicant
    success_url = '/'
    fields = ['dun', 'salutation', 'first_name', 'last_name', 'dob',
    'gender', 'nric', 'email', 'phone', 'alt_phone', 'job_title', 'salary',
    'marital_status', 'address1', 'address2', 'postal_code', 'city',
    'state']

class ApplicationUpdate(UpdateView):
    model = Applicant
    fields = ['dun', 'salutation', 'first_name', 'last_name', 'dob',
    'gender', 'nric', 'email', 'phone', 'alt_phone', 'job_title', 'salary',
    'marital_status', 'address1', 'address2', 'postal_code', 'city',
    'state']
    template_name = 'application/application_form.html'
    success_url = reverse_lazy('application-list')

    def get_context_data(self, **kwargs):
        data = super(ApplicationUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = FamilyMemberFormSet(self.request.POST, instance=self.object)
        else:
            data['familymembers'] = FamilyMemberFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()
            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(ApplicationUpdate, self).form_valid(form)

class ApplicantDelete(DeleteView):
    model = Applicant
    template_name = 'application/application_delete.html'
    success_url = reverse_lazy('application-list')



