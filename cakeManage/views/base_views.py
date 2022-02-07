from django.shortcuts import *
from django.core.paginator import Paginator
from ..models import *
from ..forms import *
import random

def home(request):
    #order_by -pub_date(최신순) pub_date(오래된순)
    cakes = Cake.objects.order_by('-pub_date')
    reviews = Review.objects.order_by('-pub_date')[:3]
    recentReviews = Review.objects.order_by('-pub_date')[:5]
    paginator = Paginator(cakes, 4)
    page = request.GET.get('page', 1)
    cakes = paginator.get_page(page)

    rand_num = random.randint(1,8)
    return render(request, 'index.html', {'cakes': cakes, 'reviews': reviews, 'recentReviews': recentReviews, 'rand_num': rand_num})
