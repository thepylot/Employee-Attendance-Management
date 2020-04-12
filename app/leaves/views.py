from datetime import date, datetime
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse

from core import models

# SIGN_IN_URL = reverse('auth:signin')

@login_required(login_url='/auth/signin')
def create_leave(request):

    annual_leave_limit = models.AnnualLimit.objects.values('annual_leave_limit').filter(user=request.user)
    requested_leave_days = models.Leave.objects.filter(user=request.user).aggregate(Sum('days'))['days__sum']
    if requested_leave_days == None:
        requested_leave_days = 0

    if request.method =="POST":
        leave_type = request.POST.get('leave_type')
        leave_start_date = request.POST.get('leave_start_date')
        leave_end_date = request.POST.get('leave_end_date')
        leave_start_time = request.POST.get('leave_start_time')
        leave_end_time = request.POST.get('leave_end_time')
        leave_reason = request.POST.get('leave_reason')
        user = request.user

        s = leave_start_date.split('-')
        d1 = date(int(s[0]),int(s[1]),int(s[2]))
        s = leave_end_date.split('-')
        d2 = date(int(s[0]),int(s[1]),int(s[2]))    
        diff_date = abs(d2-d1).days
        
        for day in annual_leave_limit:
            if day['annual_leave_limit'] < requested_leave_days + diff_date:
                messages.warning(request, 'Your leave request is greater than limit!')
            else:
                models.Leave.objects.create(
                    user=request.user,
                    leave_type = leave_type,
                    leave_start_date = leave_start_date,
                    leave_end_date = leave_end_date,
                    leave_start_time = leave_start_time,
                    leave_end_time =leave_end_time,
                    days = diff_date,
                    leave_reason = leave_reason,
                ) 
        return HttpResponse('')

@login_required(login_url='/auth/signin')
def leaves_view(request):
    profilepic = get_object_or_404(models.ProfilePic, user=request.user)
    leaves = models.Leave.objects.filter(user=request.user).order_by('-id')
     
    percentage_stroke_1 = 100
    percentage_stroke_2 = 0
    percentage_num = 0

    if leaves != None:
        requested_leave_days = models.Leave.objects.filter(user=request.user).aggregate(Sum('days'))['days__sum']
        annual_leave_limit = models.AnnualLimit.objects.values('annual_leave_limit').filter(user=request.user)

        if requested_leave_days != None:
            for day in annual_leave_limit:
                if day['annual_leave_limit'] <= 0:
                    day['annual_leave_limit'] = 0
                else:
                    day['annual_leave_limit'] -= requested_leave_days
                    percentage_stroke_2 = (day['annual_leave_limit'] * 100) / (day['annual_leave_limit'] + requested_leave_days)
                    percentage_stroke_1 -= percentage_stroke_2
                    percentage_num = int(percentage_stroke_1)


    paginator = Paginator(leaves, 5)
    page = request.GET.get('page')
    if not page:
        page = paginator.num_pages
    try:
        leaves = paginator.page(page)
    except PageNotAnInteger:
        leaves = paginator.page(1)
    except EmptyPage:
        leaves = paginator.page(paginator.num_pages)

    context = {
    'profilepic':profilepic,
    'leaves':leaves,
    'requested_leave_days':requested_leave_days,
    'annual_leave_limit':annual_leave_limit,
    'percentage_stroke_2':percentage_stroke_2,
    'percentage_stroke_1':percentage_stroke_1,
    'percentage_num':percentage_num,
    }
    return render(request,'leaves/leaves.html',context)

def delete_leave(request, id):
    leave = get_object_or_404(models.Leave, id=id)
    leave.delete()
    return redirect ('base:leaves')
