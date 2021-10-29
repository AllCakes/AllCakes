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
            str.push(createHTMLString(type, list[i], price[i], img));
            simStr.push(createSimHTMLString(type, list[i], img));
        }

        container.innerHTML = str.join('');
    }
    sim.innerHTML = simStr.join('');
}

// Html 문서 
function createHTMLString(type, item, price, img) {
    return `<div id="caketype">
    <input class="butn" name="${type}" data-key="${type}${item}" data-value="${type}sel" type="radio" value="${item}">
    <img src="${img}" style="height : 100px"> ${item} : + ${price} 원
    </div>`;
}

// Html 문서 
function createSimHTMLString(type, item, img) {
    return `<div class="${type}sel" id="${type}${item}" style="position:absolute; display:none;">
    <img src ="${img}" width="400px"></div>`;
}
function setEventListeners() {
    const logo = document.querySelectorAll('.butn');
    for(i in logo){
        logo[i].addEventListener('click', event => { onMenuClick(event)});
    }
    
}

function onMenuClick(event){
    const dataset = event.target.dataset;
    const key = dataset.key;
    const value = dataset.value;

    // 나머지 닫기
    list = document.getElementsByClassName(`${value}`);
    for(i of list){
        i.style.display = 'none';
    }
    // 그것만 열기
    document.getElementById(`${key}`).style.display ='block';

}

// main
loadMenu()
.then(menu => {
    display(menu)
    setEventListeners()
})
.catch(console.log)