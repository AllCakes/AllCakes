from django.shortcuts import *
from django.core.exceptions import ValidationError
from ..models import *
from ..forms import *
from django.http import JsonResponse
from django.views.generic.base import View

# 주문 C (RUD 구현 필요!)
def order_new(request, cake_pk): #cake의 pk값
    if not request.user.is_authenticated:
        return redirect('login_home')
    cake = get_object_or_404(Cake, pk=cake_pk)
    # 가게별 요청 - 선택사항 콤마로 분리
    a_coupons = AmountCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    p_coupons = PercentCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    # 케이크 - 재료
    havecolor = cake.print_color_menu()
    havecream = cake.print_cream_menu()
    colorObj = []
    creamObj = []

    q = Q()
    for i in list(havecolor.keys()):
        q.add(Q(pk = int(i)), q.OR)
    if q:
        colorObj = Menu_Color.objects.filter(q)
    q = Q()
    for i in list(havecream.keys()):
        q.add(Q(pk = int(i)), q.OR)
    if q != Q():
        creamObj = Menu_Cream.objects.filter(q)
    print(colorObj)
    print(creamObj)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.pub_date = timezone.now()
            order.referred_cake = cake
            order.referred_store = cake.referred_store
            order.pay_price = cake.price
            # 정제 작업
            color = request.POST.get('color')
            cream = request.POST.get('cream')
            # 재료 저장
            color_price = 0
            cream_price = 0
            if color != None :
                order.save_menu('color', color, havecolor[color])
                color_price = havecolor[color]
            if cream != None :
                order.save_menu('cream', cream, havecream[cream])
                cream_price = havecream[cream]
            # 계산 작업
            order.prev_price = (int(cake.price) + int(color_price) + int(cream_price))
            order.pay_price = order.prev_price
            s = request.POST.get('coupon').split("_")
            if request.POST.get('coupon') != "a_0":
                # 쿠폰 있다 한 경우 (쿠폰이 적용 안된 경우 아무런 조치 X)
                if s[0] == 'a':
                    # 금액쿠폰
                    try:
                        coupon = AmountCoupon.objects.get(pk=int(s[1]))
                    except AmountCoupon.DoesNotExist:
                        raise ValidationError("해당 쿠폰이 없습니다.")
                    if coupon.user != request.user:
                        #유저의 것인지 확인
                        raise ValidationError("해당 쿠폰을 사용할 수 없습니다.")
                    else:
                        order.amount_coupon = coupon
                        order.prev_price = int(cake.price) + int(color_price) + int(cream_price)
                        order.pay_price = int(order.prev_price) - coupon.amount
                else:
                    # 비율쿠폰
                    try:
                        coupon = PercentCoupon.objects.get(pk=int(s[1]))
                    except PercentCoupon.DoesNotExist:
                        raise ValidationError("해당 쿠폰이 없습니다.")
                    if coupon.user != request.user:
                        #유저의 것인지 확인
                        raise ValidationError("해당 쿠폰을 사용할 수 없습니다.")
                    else:
                        order.percent_coupon = coupon
                        order.prev_price = (int(cake.price) + int(color_price) + int(cream_price))
                        order.pay_price = int(order.prev_price) * (float(100 - coupon.percent) / 100)
                    #유저의 것인지 확인 해야 함.
            order.save()
            # 주문 결과 페이지로 가도록 수정하기!
            return redirect('order_detail', order_pk=order.pk)
    else:
        form = OrderForm()
    Context = {
        'form': form,
        'cake':cake,
        'havecolor':havecolor,
        'havecream':havecream,
        'color':colorObj,
        'cream':creamObj,
        'a_coupons':a_coupons,
        'p_coupons':p_coupons
    }
    return render(request, 'order.html', Context)

# 주문 상세 R
def order_detail(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    return render(request, 'order_detail.html',{'order':order})

# 주문 전체 R
def order_all(request, user_pk):
    if request.user.pk != user_pk:
        raise ValidationError("잘못된 접근입니다.")
    orders = Order.objects.filter(user=user_pk)
    return render(request, 'order_all.html', {'orders':orders})

# 주문 수정 U (고칠 예정)
def order_edit(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    cake = get_object_or_404(Cake, pk=order.referred_cake.pk)
    if not request.user.is_authenticated:
        return redirect('login_home')
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    if order.is_paid:
        raise ValidationError("잘못된 접근입니다.")
    # 가게별 요청 - 선택사항 콤마로 분리
    a_coupons = AmountCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    p_coupons = PercentCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    # 케이크 재료
    havecolor = cake.print_color_menu()
    havecream = cake.print_cream_menu()
    colorObj = []
    creamObj = []
    q = Q()
    for i in list(havecolor.keys()):
        q.add(Q(pk = int(i)), q.OR)
    if q :
        colorObj = Menu_Color.objects.filter(q)
    q = Q()
    for i in list(havecream.keys()):
        q.add(Q(pk = int(i)), q.OR)
    if q:
        creamObj = Menu_Cream.objects.filter(q)
    # 기존 주문 내역
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            # 정제 작업
            color = request.POST.get('color')
            cream = request.POST.get('cream')
            # 재료 재저장
            color_price = 0
            cream_price = 0
            order.reset_menu()
            if color != None :
                order.save_menu('color', color, havecolor[color])
                color_price = havecolor[color]
            if cream != None :
                order.save_menu('cream', cream, havecream[cream])
                cream_price = havecream[cream]
            s = request.POST.get('coupon').split("_")
            order.prev_price = (int(cake.price) + int(color_price) + int(cream_price))
            order.pay_price = order.prev_price
            if request.POST.get('coupon') != "a_0":
                # 쿠폰 있다 한 경우 (쿠폰이 적용 안된 경우 아무런 조치 X)
                if s[0] == 'a':
                    # 금액쿠폰
                    try:
                        coupon = AmountCoupon.objects.get(pk=int(s[1]))
                    except AmountCoupon.DoesNotExist:
                        raise ValidationError("해당 쿠폰이 없습니다.")
                    if coupon.user != request.user:
                        #유저의 것인지 확인
                        raise ValidationError("해당 쿠폰을 사용할 수 없습니다.")
                    else:
                        order.amount_coupon = coupon
                        order.prev_price =  (int(cake.price) + int(color_price) + int(cream_price))
                        order.pay_price = int(order.prev_price) - coupon.amount
                else:
                    # 비율쿠폰
                    try:
                        coupon = PercentCoupon.objects.get(pk=int(s[1]))
                    except PercentCoupon.DoesNotExist:
                        raise ValidationError("해당 쿠폰이 없습니다.")
                    if coupon.user != request.user:
                        #유저의 것인지 확인
                        raise ValidationError("해당 쿠폰을 사용할 수 없습니다.")
                    else:
                        order.percent_coupon = coupon
                        order.prev_price =  (int(cake.price) + int(color_price) + int(cream_price))
                        order.pay_price = int(order.prev_price) * (float(100 - coupon.percent) / 100)
                    #유저의 것인지 확인 해야 함.
            # get 방식으로 가져와 저장
            order.save()
            return redirect('order_detail', order_pk=order.pk)
    else:
        form = OrderForm(instance=order)
    context = {
        'form': form,
        'price':order.pay_price,
        'order': order.print_menu(),
        'cake': cake,
        'havecolor': havecolor,
        'havecream': havecream,
        'color':colorObj,
        'cream':creamObj,
        'a_coupons':a_coupons,
        'p_coupons':p_coupons
    }
    return render(request, 'order_edit.html', context)

# 주문 삭제 D
def order_delete(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    if order.is_paid:
        raise ValidationError("잘못된 접근입니다.")    
    order.delete()
    return redirect('mypage', pk=request.user.pk)

def order_complete(request):
    order_id = request.GET.get("order_id")
    order = Order.objects.get(id=order_id)
    if order.user != request.user:
        raise ValidationError("잘못된 접근입니다.")
    if order.is_paid:
        return render(request, 'order_complete.html', {'order':order})
    else:
        raise ValidationError("잘못된 접근입니다.")

class OrderTransactionAjaxView(View):
    def post(self, request, *args, **kawargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)
        
        order_id = request.POST.get('order_id')
        order = Order.objects.get(pk=order_id)
        amount = order.pay_price
        try:
            merchant_uid = OrderTransaction.objects.create_new(order = order, amount = amount)
        except:
            merchant_uid = None
        
        if merchant_uid is not None:
            data = {
                "works" : True,
                "merchant_uid" : merchant_uid
            }
            # Json 응답으로 생성여부 및 생성 내용을 반환
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class OrderImpAjaxView(View):
    # 결제한 결과에서 주문번호, 가격을 가져와 이전의 거래 객체와 비교해주고, 그러한 객체가 있으면(일치하면)
    # 통과 및 Order 객체의 결제 여부 True로 만들어주기
    # 다만 이렇게 DB와 비교하고 True로 만들어주는 것보다, 거래번호를 저장한 후에
    # 나중에 import 서버 통신을 통한 검증 후에 True로 바꿔주는 것이 더 나을듯..

    # 서버를 통한 검증 + DB의 pay_price 확인

    # 통과 X시 결제정보 위변조 가능성이 있으므로 오류발생시키고, 관리자 문의하도록 유도
    def post(self, request, *args, **karags):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_uid = request.POST.get('merchant_uid')
        imp_uid = request.POST.get('imp_uid')
        amount = request.POST.get('amount')
        try:
            trans = OrderTransaction.objects.get(order=order,merchant_uid=merchant_uid, amount=amount)
        except:
            trans = None
        if order.pay_price != amount:
            return JsonResponse({}, status=402)
        if trans is not None:
            trans.transaction_id = imp_uid
            trans.success = True
            trans.save()
            order.is_paid = True
            order.save()
            data = {
                "works": True
            }
            return JsonResponse(data)

        else:
            return JsonResponse({}, status=401)