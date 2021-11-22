#kdy : url을 앱별로 분리
from django.urls import path, include
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
    path('order/submit/<int:cake_pk>', order_new, name="order_submit"), # 케이크 주문
    path('order/detail/<int:order_pk>', order_detail, name="order_detail"), # 주문 상세
    path('order/all/<int:user_pk>', order_all, name="order_all"), # 내 주문 전체
    path('order/edit/<int:order_pk>', order_edit, name="order_edit" ), # 주문 수정하기 (이후 주문진행 상황에 따라 수정이 불가하도록 구현할 예정)
    path('order/delete/<int:order_pk>', order_delete, name="order_delete"), # 주문 취소하기 (이후 주문진행 상황에 따라 수정이 불가하도록 구현할 예정)
    
    # 결제관련 주문 추가 url
    path('order/init_transaction', OrderTransactionAjaxView.as_view(), name="order_init_transaction"), # 결제 진행 전 객체 생성
    path('order/validation', OrderImpAjaxView.as_view(), name="order_validation"), # 결제내역 검증
    path('order/complete', order_complete, name="order_complete"), # 결제, 검증 완료 후 페이지
    # 마이페이지 users로 옮김

    # 좋아요 기능 관련 url
    path('like', like_it, name="like"),
    path('likedcake_delete/<int:user_pk>/<int:cake_pk>/<int:state>', likedcake_delete, name="likedcake_delete"),
    path('likedstore_delete/<int:user_pk>/<int:store_pk>/<int:state>', likedstore_delete, name="likedstore_delete"),
    path('likedcakes/all/<int:user_pk>', likedcakes_all, name="likedcakes_all"),
    path('likedstores/all/<int:user_pk>', likedstores_all, name="likedstores_all"),

    # 리뷰 CRUD 및 별점 (R-상세보기 U-수정 D-삭제 구현 필요) (앱 새로 파야 되는지..?)
    # 리뷰 작성, 수정 시 사진 멀티업로드 구현 필요할듯  
    path('review_page/<int:pk>/order/<int:orderpk>', review_page, name="review_page"),
    path('review/delete/<int:pk>', review_delete, name="review_delete"),
    path('review/edit/<int:pk>', review_edit, name="review_edit"),
    path('review/detail/<int:review_pk>', review_detail, name="review_detail"),
    path('review/all/<int:user_pk>', review_all, name="review_all"),

    # 홈에 임시로 작성한 Stores, Cakes 링크 (가게 상세페이지 들어가기 불편해서)
    path('all/stores', stores_all, name="stores_all"),
    path('all/cakes', cakes_all, name="cakes_all"),
    path('all', search_all, name="search_all"),

    # 검색 및 필터(검색이 주된 내용)
    # cake와 store의 기본정보(장소,이름 등등...), 상세설명(store.text, cake.body, ...부족하면 리뷰도) 등을 토대로 검색 구현
    # 필터는 장소 필터링만

    path('all/search',search, name="search"),
    # 지역 필터링 (알바몬)
    path('search2/',search_location2, name="search_location2"),
    # 거리 가까운 순 정렬 페이지
    path('search3/',search_location3, name="location_result"),
    # 거리 가까운 가게 출력
    path('nearby/', nearby_stores, name="nearby_stores"),
    


    #동윤이의 테스트 url
    path('test/', test, name="test"),    
    path('chkbox/', chkbox, name="chkbox"), 
    path('character/', character, name="character"),
    #path('category/',category,name="category"),
    path('sorting/',sorting ,name="sorting"),
    path('recommend/',recommend, name="recommend"),
    path('filtering/', filtering, name="filtering"),

    # 맞춤형 메뉴 선택
    path('storemenu/<int:store_pk>', storemenu, name="storemenu"),
    path('storemenu_edit/<int:store_pk>', storemenu_edit, name="storemenu_edit"),
    path('add_menu/', add_menu , name="add_menu"),
]