from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from BYEOLZZI.models import Members, MemberLocation
from datetime import datetime

# Create your views here.
def join (request):
    return render(request,'join.html')

def idDuplicateCheck (request):
    print("Ajax 들어옴?")
    userid = request.GET.get('userid')
    try:
        id_checked = Members.objects.get(id=userid)
        pass
    except:
        id_checked = None

    if id_checked is None:
        checkresult = "pass"
    else:
        checkresult = "fail"

    print("checkresult : ", checkresult)
    context = {
        'checkresult' : checkresult
    }

    return JsonResponse(context)

def createMember(request:HttpRequest):
    id = request.POST.get("id")
    pw = request.POST.get("pw")
    name = request.POST.get("name")
    addr = request.POST.get('addr')

    print("=" * 30)
    print("id:", id)
    print("pw:", pw)
    print("name:", name)
    print("addr:", addr)

    try:
        Members.objects.create(
            id = id,
            pw = pw,
            m_name = name,
            addr = addr
        )
    except Exception as e:
        print(e)
        return redirect('/member/join/')

    return render(request,'login.html')

def login(request:HttpRequest):
    id = request.GET.get("id")
    #result = request.GET.get("result")
    print('login/id : ', id)
    check = False
    if id == None:
        print('login/id : ', id)
        id = request.COOKIES.get("checkedid")
        if id != None:
            check = True

    print('login/check : ', check)
    context = {
        'id' : id,
        "check" : check,
    }

    return render(request,'login.html',context);

def checkLogin(request:HttpRequest):
    id = request.POST.get("id")
    pw = request.POST.get("pw")
    
    result = None

    try:
        member = Members.objects.get(id=id,pw=pw)
    except Exception as e:
        result = True
        return redirect('/member/login/?result=' + result)
    else:
        request.session['login'] = member.members_idx
    
    response = render(request,'main.html')

    if result:
        checkedid = request.POST.get("checkedid")
        print("checkLogin/checkedid : ", checkedid)

        cookieid = request.COOKIES.get('checkedid')
        print("checkLogin/cookieid : ", cookieid)
        
        if checkedid != None:
            if cookieid == None:
                response.set_cookie("checkedid",id,max_age=60*60*48)
            elif cookieid != id:
                response.set_cookie("checkedid",id,max_age=60*60*48)
        else:
            if cookieid == id:
                response.delete_cookie("checkedid")

    return redirect('/')

def logout(request:HttpRequest):
    request.session.pop('login')
    return redirect('/')


def mypage (request:HttpRequest):
    user_idx = request.session['login']

    member = Members.objects.get(members_idx=user_idx)
    memberLocation = MemberLocation.objects.filter(m_idx=user_idx)
    m_list = []

    for i in range(len(memberLocation)):
        m_list.append(memberLocation[i].location_list)

    context = {
        'member' : member,
        'm_list' : m_list
    }
    return render(request,'mypage.html', context);