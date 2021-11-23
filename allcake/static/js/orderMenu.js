// JSON file 에서 fetch 작업
function loadMenu(){
    return fetch('/static/data/menu.json')
    .then(response => response.json())
    .then(json => json.menu);
}

// 각 json data를 html 요소로 변환
function display(menu){
    const sim = document.querySelector(".simulation");
    const simStr = [];

    for(type in menu[0]){
        const container = document.querySelector(`.${type}`);
        const str = [];
        var list, price;

        if(type === '색'){
            list = color.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
            price = colorP.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
        }
        else if(type === '크림종류'){
            list = cream.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
            price = creamP.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
        }

        for(i in list){ // 딸기
            const img = menu[0][type][list[i]];   // 이미지
            if((type == "색" && list[i] == choice_color) || (type == "크림종류" && list[i] == choice_cream)){
                str.push(createHTMLString(type, list[i], price[i], img, 0));
                simStr.push(createSimHTMLString(type, list[i], img, 0));
            }
            else{
                str.push(createHTMLString(type, list[i], price[i], img, 1));
                simStr.push(createSimHTMLString(type, list[i], img, 1));
            }
        }
        container.innerHTML = str.join('');
    }
    // 레터링 부분 추가
    simStr.push(createSimLetter(1));
    simStr.push(createSimLetter(2));

    sim.innerHTML = simStr.join('');
}

// Html 문서 
function createHTMLString(type, item, price, img, num) {
    if(num == 0)
        return `<div id="caketype">
        <input class="butn" name="${type}" data-key="${type},${item}" data-value="${price}" type="radio" checked value="${item}">
        <img src="${img}" style="height : 100px"> ${item} : + ${price} 원
        </div>`;
    return `<div id="caketype">
    <input class="butn" name="${type}" data-key="${type},${item}" data-value="${price}" type="radio" value="${item}">
    <img src="${img}" style="height : 100px"> ${item} : + ${price} 원
    </div>`;
}

// 시물레이션에 필요한 Html 문서 
function createSimHTMLString(type, item, img, num) {
    if(img === '/static/img/noimg.png'){
        return`<div class="${type}sel" id="${type}${item}"></div>`;
    }
    if(num == 0){
        return `<div class="${type}sel" id="${type}${item}" style="position:absolute; display:block">
        <img src ="${img}" width="400px"></div>`;
    }
    return `<div class="${type}sel" id="${type}${item}" style="position:absolute; display:none">
    <img src ="${img}" width="400px"></div>`;
}

// 시물레이션에 필요한 Html 문서 - 레터링 부분 
function createSimLetter(num) {
    return `<div id="letter_pos${num}" style="position:absolute; display:none">
    <img src ="/static/img/letter${num}.png" width="400px"></div>`;
}

// 클릭시 이벤트
function setEventListeners() {
    const logo = document.querySelectorAll('.butn');
    for(i in logo){
        logo[i].addEventListener('click', event => {onMenuClick(event)});
    }
}

function onMenuClick(event){
    const dataset = event.target.dataset;
    const k = dataset.key;
    const value = dataset.value;
    const key = k.split(',');

    if(key[0] === 'letter'){
        mesg = document.getElementById('id_lettering_position').value;
        console.log(mesg)
        if(mesg == "케이크에 직접 레터링"){
            document.getElementById('letter_pos1').style.display ='none';
            document.getElementById('letter_pos2').style.display ='block';
        }
        else{
            document.getElementById('letter_pos1').style.display ='block';
            document.getElementById('letter_pos2').style.display ='none';
        }
    }
    else{
        calPrice();
        // 나머지 닫기
        list = document.getElementsByClassName(`${key[0]}sel`);
        for(i of list){
            i.style.display = 'none';
        }
        // 그것만 열기
        document.getElementById(`${key[0]}${key[1]}`).style.display ='block';
    }
}
function calPrice(){
        // 가격 계산
        var price_cream = 0, price_color = 0;
        var cream_list = document.querySelectorAll('input[name="크림종류"]:checked');
        var color_list = document.querySelectorAll('input[name="색"]:checked');
        if(cream_list[0]){
            price_cream = cream_list[0].dataset.value;
        }
        if(color_list[0]){
            price_color = color_list[0].dataset.value;
        }
        
        var tol = Number(total_price) + Number(price_color) + Number(price_cream);
        document.getElementById('total_price').value = tol;
}
// main
loadMenu()
.then(menu => {
    display(menu)
    calPrice()
    setEventListeners()
})
.catch(console.log)