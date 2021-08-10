#kdy : url을 앱별로 분리
from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="home"),
    
    # 순서대로 가게, 케이크, 주문, 리뷰, 검색필터

    # 가게 CRUD (다만, C는 admin 사이트에서 이뤄지고, U는 주인이 가능하도록 ) + 찜하기 기능 javascript필요
    path('store/new/', store_new, name="store_new"),
    path('store/<int:pk>', store_detail, name="store_detail"),
    path('store/edit/<int:pk>', store_edit, name="store_edit"),
    path('store/<int:pk>/delete', store_delete, name="store_delete"),

    # 케이크 CRUD (다만, CUD는 가게 pk 참조해서 현재 유저가 사장 유저이면 접근하도록!) + 찜하기 기능 javascript필요
    path('cake/new/<int:pk>', cake_new, name="cake_new"), 
    path('cake/detail/<int:pk>', cake_detail, name="cake_detail"),
    path('cake/edit/<int:pk>', cake_edit, name="cake_edit"),
    path('cake/delete/<int:pk>', cake_delete, name="cake_delete"),

    # 주문 CRUD (주문 결과화면 + R-상세보기 U-수정 D-주문취소 구현필요) (앱 새로 파야 되는지..?)
    path('order/<int:pk>', order_new, name="order"),

    # 마이페이지 users로 옮김

    # 리뷰 CRUD 및 별점 (R-상세보기 U-수정 D-삭제 구현 필요) (앱 새로 파야 되는지..?)
    # 리뷰 작성, 수정 시 사진 멀티업로드 구현 필요할듯  
    path('review_page/<int:pk>/order/<int:orderpk>', review_page, name="review_page"),
    path('review/', review_rating, name="review"),

    # 검색 및 필터(검색이 주된 내용)
    # cake와 store의 기본정보(장소,이름 등등...), 상세설명(store.text, cake.body, ...부족하면 리뷰도) 등을 토대로 검색 구현
    # 필터는 장소 필터링만

]