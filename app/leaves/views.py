from datetime import date, datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum

from core import models

def create_leave(request):
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


def leaves_view(request):
   
    leaves = models.Leave.objects.filter(user=request.user).order_by('-id')
   
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
                 
                percentage_stroke_2 = (day['annual_leave_limit'] * 100) / (day['annual_leave_limit'] + requested_leave_days) # white part 10
                percentage_stroke_1 -= percentage_stroke_2
                percentage_num = int(percentage_stroke_1)

        #     for limit in leave_limit:
        #         if total_days > limit['annual_leave_limit']:
        #             left = total_days - limit['annual_leave_limit']
        #             d = days['days'] - left
        #             total_days = total_days - left
        #             z = Attend.objects.filter(user=request.user).order_by('id')[0]
        #             z.status = 'declined'
        #             z.save(update_fields=['status'])
        #             percentage_stroke_1 = 100
        #             percentage_stroke_2 = 0
        #             percentage_num = 100
                    
        #             messages.error(request, 'Your annual leave limit is over!( {} days is more than limit )'.format(left))    

        #         if total_days == limit['annual_leave_limit']:
        #             messages.warning(request, 'Your annual leave limit is over! You can not request leaves anymore!')
    

    context = {

    'leaves':leaves,
    'requested_leave_days':requested_leave_days,
    'annual_leave_limit':annual_leave_limit,
    'percentage_stroke_2':percentage_stroke_2,
    'percentage_stroke_1':percentage_stroke_1,
    'percentage_num':percentage_num,
    # 'leave_limit':leave_limit,
    # 'profilepic':profilepic,
    }
    template = "leaves/leaves.html"
    return render(request,template,context)
