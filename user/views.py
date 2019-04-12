# Create your views here.
import datetime
from django.shortcuts import render
from django.http import JsonResponse,HttpRequest,HttpResponseBadRequest
import simplejson
from .models import User
from django.db.models import Q
import bcrypt
import jwt
from django.conf import settings

key = settings.SECRET_KEY
AUTH_EXPIRE  = 8*60*60 #8小时过期

def gen_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp':int(datetime.datetime.now().timestamp() + AUTH_EXPIRE)
    }, key, 'HS256').decode()

#注册
def reg(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        query = User.objects.filter(email=email)#获取用户提交的email是否存在
        if query.first():
            return JsonResponse({"error" :'用户名已经存在'})
        name = payload['name']
        password = payload['password']
        user = User()
        user.email = email
        user.name = name
        user.password = bcrypt.hashpw(password.encode(),bcrypt.gensalt())#密码加密

        try:
            user.save()
            # return JsonResponse({
            #     'token':gen_token(user.id)
            # }) #注册成功后直接给了token实现免登录
            return JsonResponse({
                'user_id':user.id
            })
        except Exception as e:
            print(e)
            return JsonResponse({'error':'注册失败！'},status=400)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('参数错误')

def login(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password']

        user = User.objects.filter(email=email).first()
        if user:
            if bcrypt.checkpw(password.encode(),user.password.encode()):#判断密码
                token = gen_token(user.id)
                res = JsonResponse({
                    'user':{
                        'user_id':user.id,
                        'name':user.name,
                        'email':user.email,
                    },
                    'token':token
                })
                res.set_cookie('jwt',token)
                return res
            else:
                return HttpResponseBadRequest('密码错误！')
        else:
            return HttpResponseBadRequest('账号不存在！')
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('登录失败2')

def auth(view_func):
    def wrapper(request:HttpRequest):
        token = request.META.get('HTTP_JWT', None)
        if not token:  # 认证失败
            return HttpResponseBadRequest('请登陆!', status=401)

        try:
            payload = jwt.decode(token, key, algorithms=['HS256'])

            user = User.objects.filter(pk=payload['user_id']).first()
            if user:
                request.user = user
                ret = view_func(request)
                return ret
            else:
                return HttpResponseBadRequest('Error! ')
        except jwt.ExpiredSignatureError as e:
            print('error',e)
            return HttpResponseBadRequest('jwt过期')

        except Exception as e:
            print(e)
            return HttpResponseBadRequest('用户名密码错误！')
    return wrapper

#用装饰器来认证
# @auth
def show(request:HttpRequest):
    print(1111111111111111111111111111,request.GET)
    ret = JsonResponse({
        'status':'ok',
    })
    ret['Access-Control-Allow-Origin'] = '*'
    return ret

#定义一个中间件认证用户身份
class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_JWT', None)
        if not token:  # 认证失败
            return HttpResponseBadRequest('请登陆!', status=401)

        try:
            payload = jwt.decode(token, key, algorithms=['HS256'])

            user = User.objects.filter(pk=payload['user_id']).first()
            if user:
                request.user = user
            else:
                return HttpResponseBadRequest('Error! ')
        except jwt.ExpiredSignatureError as e:
            print('error', e)
            return HttpResponseBadRequest('jwt过期')

        except Exception as e:
            print(e)
            return HttpResponseBadRequest('用户名密码错误！')

        response = self.get_response(request)
        return response


