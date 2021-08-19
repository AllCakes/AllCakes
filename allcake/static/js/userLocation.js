
function getapi() {
    fetch(`//dapi.kakao.com/v2/maps/sdk.js?appkey=46d5f6c310a78632612936d0ea60df74&libraries=services`
    );
}
function getLocation() {
    if (navigator.geolocation) {
        // GPS를 지원하면
        navigator.geolocation.getCurrentPosition(
            function (position) {
                console.log(position);
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const coords = position.coords;

                var geocoder = new window.kakao.maps.services.Geocoder(); //window 추기
                function searchAddrFromCoords(coords, callback) {
                    // 좌표로 geocoder에게 행정동 주소 정보를 요청
                    console.log(callback);
                    geocoder.coord2RegionCode(coords.longitude, coords.latitude, callback);
                    //=> geocoder이 위도와 경도 좌표 바탕으로 주소 정보를 알려준다
                }
                searchAddrFromCoords(coords, displayCenterInfo);
                //이 함수를 display~가 들어가면서 위치 정보 얻고 얘를 html에 바로 출력하게 해준다

                function displayCenterInfo(result, status) {
                    console.log(result);
                    console.log(status); //status 는 연결 상태 말하는 것 -> 연결상태가 ok 라면..
                    if (status === kakao.maps.services.Status.OK) {
                        for (var i = 0; i < result.length; i++) {
                            // 행정동의 region_type 값은 'H' 이므로
                            if (result[i].region_type === "H") {
                                const address = result[1].address_name;
                                console.log(latitude + " " + longitude + " " + address);
                                // const element = document.querySelector(`.location`);
                                //  element.style.display = "block";
                                const input1 = document.getElementById("location_input");
                                input1.innerText = address;
                                const input2 = document.getElementById("mylatlon");
                                input2.innerText = latitude; 
                                const input3 = document.getElementById("mylatlon");
                                input3.innerText = longitude;                                 
                                //console.log(element);
                                break;
                            }
                        }
                    }
                }
            },
            function (error) {
                console.error(error);
            },
            { //옵션 사항들입니당~
                enableHighAccuracy: false,
                maximumAge: 0,
                timeout: Infinity,
            }
        );
    } else {
        alert("GPS를 지원하지 않습니다");
    }
}

const onLocation = () => {
    getLocation();
};


onLocation(); //실행을 시켜줘야지