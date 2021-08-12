const star1 = document.getElementById('star-1')
const star2 = document.getElementById('star-2')
const star3 = document.getElementById('star-3')
const star4 = document.getElementById('star-4')
const star5 = document.getElementById('star-5')

const select = (sel) =>{
    switch(sel){
        case 'star1':{
            star1.classList.add('checked')
            star2.classList.remove('checked')
            star3.classList.remove('checked')
            star4.classList.remove('checked')
            star5.classList.remove('checked')
            return
        }
        case 'star2':{
            star1.classList.add('checked')
            star2.classList.add('checked')
            star3.classList.remove('checked')
            star4.classList.remove('checked')
            star5.classList.remove('checked')
            return
        }
        case 'star3':{
            star1.classList.add('checked')
            star2.classList.add('checked')
            star3.classList.add('checked')
            star4.classList.remove('checked')
            star5.classList.remove('checked')
            return
        }
        case 'star4':{
            star1.classList.add('checked')
            star2.classList.add('checked')
            star3.classList.add('checked')
            star4.classList.add('checked')
            star5.classList.remove('checked')
            return
        }
        case 'star5':{
            star1.classList.add('checked')
            star2.classList.add('checked')
            star3.classList.add('checked')
            star4.classList.add('checked')
            star5.classList.add('checked')
            return
        }
    }
}

function 열기(num) {
    document.getElementsByClassName('items')[num].style.display = 'block';
    document.getElementsByClassName('items')[(num + 1) % 3].style.display = 'none';
    document.getElementsByClassName('items')[(num + 2) % 3].style.display = 'none';
}

var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
mapOption = {
    center: new kakao.maps.LatLng(37.5573264, 126.9474058), // 지도의 중심좌표
    level: 3 // 지도의 확대 레벨
};

var map = new kakao.maps.Map(mapContainer, mapOption);

// 마커가 표시될 위치입니다 
var markerPosition = new kakao.maps.LatLng(37.5573264, 126.9474058);

// 마커를 생성합니다
var marker = new kakao.maps.Marker({
position: markerPosition
});

// 마커가 지도 위에 표시되도록 설정합니다
marker.setMap(map);

var iwContent =
'<div style="padding:5px;">뽀들렌 케이크<br><a href="https://map.kakao.com/link/map/뽀들렌케이크,37.5573264,126.9474058"  target="_blank">큰지도보기</a> <a href="https://map.kakao.com/link/to/Hello World!,37.5573264,126.9474058" target="_blank">길찾기</a></div>', // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
iwPosition = new kakao.maps.LatLng(37.5573264, 126.9474058); //인포윈도우 표시 위치입니다

// 인포윈도우를 생성합니다
var infowindow = new kakao.maps.InfoWindow({
position: iwPosition,
content: iwContent
});

// 마커 위에 인포윈도우를 표시합니다. 두번째 파라미터인 marker를 넣어주지 않으면 지도 위에 표시됩니다
infowindow.open(map, marker);