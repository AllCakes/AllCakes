// JSON file 에서 fetch 작업
function loadMenu(){
    return fetch('/static/data/menu.json')
    .then(response => response.json())
    .then(json => json.menu);
}

// 각 json data를 html 요소로 변환
function display(menu){

    for(type in menu[0]){

        var list;
        const container = document.querySelector(`.${type}`);
        const str = [];

        if(type === '색')
            list = color.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
        else if(type === '크림종류')
            list = cream.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');

        for(i in list){ // 딸기
            const img = menu[0][type][list[i]];   // 이미지
            str.push(createHTMLString(type, list[i], img));
        }
        container.innerHTML = str.join('');
    }
}

// Html 문서 
function createHTMLString(type, item, img) {
    return `<div id="caketype">
    <label for="${type}${item}" onclick="selectCheck('${type}${item}')">
    <input id="${type} ${type}${item}" type="checkbox" name="${type}" value="${item}"></label>
    <img src="${img}" style="height : 100px"> ${item}
    가격입력 : <input class = "${type}${item}" name="${type}price" type="text" value=0  disabled>
    </div>`;
}

function selectCheck(t){
    const a = document.querySelector(`.${t}`);
    if(a.hasAttribute("disabled")){
        a.removeAttribute("disabled");
    }
    else{
        a.setAttribute("disabled",true);
    }
}

// main
loadMenu()
.then(menu => {
    display(menu)
})
.catch(console.log)