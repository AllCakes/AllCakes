// JSON file 에서 fetch 작업
function loadMenu(){
    return fetch('/static/data/menu.json')
    .then(response => response.json())
    .then(json => json.menu);
}

// 각 json data를 html 요소로 변환
// $("input[name='맛'][value='딸기']").prop("checked",true);
function display(menu){
    console.log(menu);
    for(type in menu[0]){ //type(key) : 맛 , menu[0][type](value) : {딸기 : 이미지}
        const container = document.querySelector(`.${type}`);
        const str = [];

        const 색 = color.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
        const 크림종류 = cream.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');

        let chk;   
        for(item in menu[0][type]){
        
            if(type === '색') chk = 색.includes(item)
            else if(type === "크림종류") chk = 크림종류.includes(item)

            const img = menu[0][type][item]   // 이미지찾기
            if(chk){
                str.push(createHTMLString(type, item, img, 1));
            }
            else{
                str.push(createHTMLString(type, item, img, 0));
            }
        }
        container.innerHTML = str.join('');
    }
}

// Html 문서로 만들기 
function createHTMLString(type, item,img, num) {
    if(num == 1)
        return `<div id="caketype">
        <input type="checkbox" id="${type}" name="${type}" checked value="${item}">
        <img src="${img}" style="height : 100px">
        <div style="text-align: center;">${item}</div>
        </div>`;
    return `<div id="caketype">
                <input type="checkbox" id="${type}" name="${type}" value="${item}">
                <img src="${img}" style="height : 100px;">
                <div style="text-align: center;">${item}</div>
            </div>`;
}

// 클릭시 메뉴 추가
function setEventListeners(menu) {
    const buttons = document.querySelectorAll('.AddMenu');
    for(i in buttons){
        buttons[i].addEventListener('click', event => { AddMenu(event, menu)});
    }
}
// 메뉴 추가 함수
function AddMenu(event, menu){
    const dataset = event.target.dataset;
    const key = dataset.key;
    const value = dataset.value;
    console.log(key, value);
    
    const inputtext = document.getElementById(`${key}`)
    const input_value = inputtext.value

    let chk = false;
    for (i in menu[0][`${value}`]){
        if(i == inputtext.value) chk = true;
    }

    if(chk){
        alert("중복된 값입니다.");
    }
    else{
        if(inputtext.value === "")
            alert("아무것도 입력되지 않았습니다.");
        else{
            $.ajax({
                type: 'POST',
                url: '/add_menu/',
                data: {
                    ty: `${value}`,
                    value: `${input_value}`,
                    img : "/static/img/noimg.png"
                }
            })
            // .then(window.location.href=delete_url;);
        }
    }
}

// main
loadMenu()
.then(menu => {
    display(menu)
    setEventListeners(menu)
})
.catch(console.log)