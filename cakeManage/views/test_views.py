from django.shortcuts import *
from ..models import *
from ..forms import *
from itertools import chain #쿼리셋 결합 위해 추가

# 임시 템플릿 연결 뷰
def stores_all(request):
    stores= Store.objects.order_by('-pub_date')
    return render(request, 'stores_cpy.html', {'stores':stores})

def cakes_all(request):
    cakes= Cake.objects.order_by('-pub_date')
    return render(request, 'cakes_all.html', {'cakes':cakes})

# 처음 검색창 불러왔을 때 
def search_all(request):
    cakes=Cake.objects.all() 
    stores=Store.objects.all()
    products=[cakes,stores]
    products=list(chain(*products))
    num1=Cake.objects.all().count()
    num2=Store.objects.all().count()
    num=num1+num2
    return render(request, 'search_all.html', {'cakes':cakes, 'stores':stores,'product':products,'num':num})

def test(request):
    return render(request, 'test.html')

def chkbox(request):
    return render(request, 'chkbox.html')

def character(request):
    post_list=[]
    searchWord="캐릭터"
    if searchWord :
        for word in searchWord:
            post_list+=Cake.objects.filter(Q(meta_body__icontains=word)).distinct()
            # '+' 붙여서 리스트에 요소를 추가추가해주는 방식으로 가야함
            # 안 붙여주면 구로구,노원구 두개 이상 선택시 둘 중에 한 구만 필터링됨
    context={}
    context['search_term']=searchWord
    context['objects_list']=post_list
    return render(request, 'character.html',context)