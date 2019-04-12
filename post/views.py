from django.shortcuts import render
from django.http import HttpRequest,HttpResponseBadRequest,JsonResponse,HttpResponseNotFound
from user.views import auth
import simplejson
from  post.models import Post,Content
import datetime
import math

# Create your views here.

@auth
def pub(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        title = payload['title']
        content_text = payload['content']
        post = Post()
        post.title = title
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))#时区
        post.author =request.user
        post.save()

        content = Content()
        content.post = post
        content.content = content_text
        content.save()
        return JsonResponse({
            'post':post.id
        })
    except Exception as e:
        print(e,'~'*30)
        return HttpResponseBadRequest()

def get(request:HttpRequest,id): #/post/1
    print(id,type(id))
    try:
        post = Post.objects.get(pk=int(id))
        return JsonResponse({
            'post':{
                'post_id':post.id,
                'title':post.title,
                'postdate':int(post.postdate.timestamp()),
                'author':post.author.name,
                'author_id':post.author_id, #post.author.id
                'content':post.content.content
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseNotFound()

#http://127.0.0.1:8000/post/?page=1
#conut pagas page size
def validate(d:dict,name:str,convert_func,default,validate_func):
    try:
        x = convert_func(d.get(name))
        # lambda x,y: x if x>0 else y
        ret = validate_func(x,default) #x if x >0 else default
    except:
        ret = default
    return ret

def getall(request:HttpRequest):
    # try:
    #     page = int(request.GET.get('page'))
    #     page = page if page > 0 else 1
    # except Exception as e:
    #     page = 1
    #
    # try:
    #     size = int(request.GET.get('size'))
    #     size = size if size > 0 and size <=25 else 20
    # except Exception as e:
    #     size = 20

    page = validate(request.GET, 'page', int, 1, lambda x,y: x if x > 0 else y)
    size = validate(request.GET, 'size', int, 20, lambda x,y: x if x>0 and x<101 else y)
    start = (page - 1) * size

    posts = Post.objects.order_by('-pk').all()
    count = posts.count()
    posts = posts[start:start+size]
    if posts:
        return JsonResponse({
            'posts':[
                {
                    'post_id':post.id,
                    'title':post.title,
                } for post in posts
            ],
            'pagination':{
                'page':page,
                'size':size,
                'count':count,
                'pages': math.ceil(count/size) #向上取整
            }
        })
    else:
        return HttpResponseNotFound()