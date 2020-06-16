from datetime import date, datetime
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse

from core import models

@login_required(login_url='/auth/signin')
def manager_leaves_detail(request, id):
    """ Leave detail review for managers or supervisors"""
    available_leave_days = 0
    leave = get_object_or_404(models.Leave, id=id)
    profile_pic = get_object_or_404(models.ProfilePic, user=leave.user)
    profile = models.User.objects.filter(email=leave.user.email)
    total_leave_days = models.Leave.objects.filter(user=leave.user).aggregate(Sum('days'))['days__sum']
    annual_leave_limit = models.AnnualLimit.objects.values('annual_leave_limit').filter(user=leave.user)

    waiting = models.Leave.objects.filter(user=leave.user, status='waiting').aggregate(Sum('days'))['days__sum']
    approved = models.Leave.objects.filter(user=leave.user, status='approved').aggregate(Sum('days'))['days__sum']

    for day in annual_leave_limit:
        available_leave_limit = day['annual_leave_limit'] - total_leave_days
    
    context = {
        'leave':leave,
        'profile_pic':profile_pic,
        'profile':profile,
        'total_leave_days':total_leave_days,
        'available_leave_limit':available_leave_limit,
        'waiting':waiting,
        'approved':approved,

        }

    return render(request, 'manager/manager_leave_detail.html', context)

@login_required(login_url='/auth/signin')
def manager_leaves_view(request):
    """ All leaves and only visible to managers or supervisors"""
    leaves = models.Leave.objects.order_by('-id')

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
    return render(request, 'manager/manager_leaves.html', {
        'leaves':leaves,
        })


def total_leaves_monthly_bar_chart(request):
    """ Bar chart for leave requests monthly"""
    months = []
    leaves_monthly = []
    monthly_total_leave_days = models.Leave.objects.annotate(month=TruncMonth('leave_start_date')).values('month').annotate(leaves_monthly=Sum('days')).order_by('month')
    for item in monthly_total_leave_days:
        months.append(item['month'].strftime('%B'))
        leaves_monthly.append(item['leaves_monthly'])


    return JsonResponse(data={
    'months': months,
    'leaves_monthly':leaves_monthly,
    })