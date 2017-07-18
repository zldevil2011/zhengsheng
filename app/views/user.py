# coding=utf-8
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from app.models import AppUser, Adminer
from django.contrib.auth.hashers import check_password
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@csrf_exempt
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print username, password
    print "before"
    try:
        print "try"
        try:
            print "TRY1"
            user = User.objects.get(username = username)
        except Exception, e:
            print "EXP"
            print str(e)
            user = None
            return HttpResponse("error")
        print user.password
        print check_password(password, user.password)
        if check_password(password, user.password):
            try:
                adminer = Adminer.objects.get(user=user)
            except:
                return HttpResponse("error")
            print "check ok"
            request.session['username'] = adminer.name
            return HttpResponse("success")
        else:
            return HttpResponse("error")
    except AppUser.DoesNotExist:
        print "except"
        return HttpResponse("error")


@csrf_exempt
def logout(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    del request.session['username']
    return HttpResponseRedirect("/admin_login/")


@csrf_exempt
def admin_account(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    try:
        page = request.GET.get("page", 1)
    except:
        pass
    page = int(page)
    if page < 1:
        page = 1
        return HttpResponseRedirect("/admin_account?page=1")
    start_num = (page - 1) * 10
    end_num = page * 10
    if user.level == 0:
        userlist = AppUser.objects.filter()
    else:
        userlist = AppUser.objects.filter(adminer=user)
    total_page = int(math.ceil(userlist.count()/10.0))
    if total_page < 1:
        total_page = 1
    if page > total_page:
        return HttpResponseRedirect("/admin_account?page=" +str(total_page))
    userlist = userlist[start_num:end_num]
    return render(request, 'app/admin_account.html', {
        "userlist" : userlist,
        "page": page,
        "total_page": total_page,
        "user": user
    })


def admin_work_order(request):
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    return render(request, 'app/admin_workOrder.html', {})


@csrf_exempt
def admin_delete_user(request):
    # return HttpResponse("success")
    try:
        user = Adminer.objects.get(name=request.session['username'])
    except:
        return HttpResponseRedirect("/admin_login/")
    user_id = request.POST.get("user_id", None)
    if user_id is None:
        return HttpResponse("error")
    user_id = int(user_id)
    user = AppUser.objects.get(id=user_id)
    try:
        # 删除设备，避免用户存在，但是设备不存在
        device = user.device
        device.device_status = u"未安装"
        device.city_code=''
        device.village_code=''
        device.building_code=''
        device.unit_code = ''
        device.room_code = ''
        device.remarks=''
        device.save()
    except Exception as e:
        print(str(e))
    sys_user = user.user
    sys_user.delete()
    user.delete()
    return HttpResponse("success")