#kdy : url을 앱별로 분리
from django.urls import path
from .views import (base_views, cake_views, store_views, like_views, menu_views, order_views, review_views,search_views, test_views)


urlpatterns = [
    # base_views.py
    path('', base_views.home , name="home"),
    
    # store_views.py
    # 가게 CRUD (다만, C는 admin 사이트에서 이뤄지고, U는 주인이 가능하도록)
    path('store/new/', store_views.store_new, name="store_new"), 
    path('store/<int:pk>', store_views.store_detail, name="store_detail"),
    path('store/edit/<int:pk>', store_views.store_edit, name="store_edit"),
    path('store/<int:pk>/delete', store_views.store_delete, name="store_delete"),

    # cake_views.py
    # 케이크 CRUD (다만, CUD는 가게 pk 참조해서 현재 유저가 사장 유저이면 접근하도록!)
    path('cake/new/<int:pk>', cake_views.cake_new, name="cake_new"), 
    path('cake/detail/<int:pk>', cake_views.cake_detail, name="cake_detail"),
    path('cake/edit/<int:pk>', cake_views.cake_edit, name="cake_edit"),
    path('cake/delete/<int:pk>', cake_views.cake_delete, name="cake_delete"),

    # order_views.py
    # 1. 주문 CRUD (주문 결과화면 + R-상세보기 U-수정 D-주문취소 구현필요)
    path('order/submit/<int:cake_pk>', order_views.order_new, name="order_submit"), # 케이크 주문
    path('order/detail/<int:order_pk>', order_views.order_detail, name="order_detail"), # 주문 상세
    path('order/all/<int:user_pk>', order_views.order_all, name="order_all"), # 내 주문 전체
    path('order/edit/<int:order_pk>', order_views.order_edit, name="order_edit" ), # 주문 수정하기 (이후 주문진행 상황에 따라 수정이 불가하도록 구현할 예정)
    path('order/delete/<int:order_pk>', order_views.order_delete, name="order_delete"), # 주문 취소하기 (이후 주문진행 상황에 따라 수정이 불가하도록 구현할 예정)
    # 2. 결제관련 주문 추가 url
    path('order/init_transaction', order_views.OrderTransactionAjaxView.as_view(), name="order_init_transaction"), # 결제 진행 전 객체 생성
    path('order/validation', order_views.OrderImpAjaxView.as_view(), name="order_validation"), # 결제내역 검증
    path('order/complete', order_views.order_complete, name="order_complete"), # 결제, 검증 완료 후 페이지

    # like_views.py : 좋아요 기능 관련 url
    path('like', like_views.like_it, name="like"),
    path('likedcake_delete/<int:user_pk>/<int:cake_pk>/<int:state>', like_views.likedcake_delete, name="likedcake_delete"),
    path('likedstore_delete/<int:user_pk>/<int:store_pk>/<int:state>', like_views.likedstore_delete, name="likedstore_delete"),
    path('likedcakes/all/<int:user_pk>', like_views.likedcakes_all, name="likedcakes_all"),
    path('likedstores/all/<int:user_pk>', like_views.likedstores_all, name="likedstores_all"),

    # review_views.py : 리뷰 CRUD 및 별점 CRUD
    path('review_page/<int:pk>/order/<int:orderpk>', review_views.review_page, name="review_page"),
    path('review/delete/<int:pk>', review_views.review_delete, name="review_delete"),
    path('review/edit/<int:pk>', review_views.review_edit, name="review_edit"),
    path('review/detail/<int:review_pk>', review_views.review_detail, name="review_detail"),
    path('review/all/<int:user_pk>', review_views.review_all, name="review_all"),

    # search_views.py : 검색 및 필터
    # cake와 store의 기본정보(장소,이름 등등...), 상세설명(store.text, cake.body, ...부족하면 리뷰도) 등을 토대로 검색 구현
    # 필터는 장소 필터링만
    path('all/search', search_views.search, name="search"), # 지역 필터링 (알바몬)
    path('search2/', search_views.search_location2, name="search_location2"), # 거리 가까운 순 정렬 페이지
    path('search3/', search_views.search_location3, name="location_result"),  # 거리 가까운 가게 출력
    path('nearby/', search_views.nearby_stores, name="nearby_stores"),
    path('sorting/', search_views.sorting ,name="sorting"),
    path('recommend/', search_views.recommend, name="recommend"),
    path('filtering/', search_views.filtering, name="filtering"),
    # path('category/',category,name="category"),

    # menu_views.py : 맞춤형 메뉴 선택
    path('storemenu/<int:store_pk>', menu_views.storemenu, name="storemenu"),
    path('storemenu_edit/<int:store_pk>', menu_views.storemenu_edit, name="storemenu_edit"),
    path('add_menu/<int:store_pk>', menu_views.add_menu , name="add_menu"),

    # test_views.py : TEST
    # 홈에 임시로 작성한 Stores, Cakes 링크 (가게 상세페이지 들어가기 불편해서)
    path('all/stores', test_views.stores_all, name="stores_all"),
    path('all/cakes', test_views.cakes_all, name="cakes_all"),
    path('all', test_views.search_all, name="search_all"),
    path('test/', test_views.test, name="test"),    
    path('chkbox/', test_views.chkbox, name="chkbox"), 
    path('character/', test_views.character, name="character"),
]