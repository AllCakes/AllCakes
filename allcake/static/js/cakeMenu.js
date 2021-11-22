// JSON file 에서 fetch 작업
function loadMenu(){
    return fetch('/static/data/menu.json')
    .then(response => response.json())
    .then(json => json.menu);
}

// 각 json data를 html 요소로 변환
function display(menu){
    for(type in menu[0]){
        var store_list, list = [], price = [], str = [];
        const container = document.querySelector(`.${type}`);

        if(type === '색'){
            store_list = store_col.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
            list = color.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
            price = color_price.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
        }    
        else if(type === '크림종류'){
            store_list = store_cream.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
            list = cream.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
            price = cream_price.replace(/&#x27;/g,"").replaceAll(" ","").replace("[","").replace("]","").split(',');
        }

        for(i in store_list){ // 딸기
            const img = menu[0][type][store_list[i]];   // 이미지
            var idx = list.indexOf(store_list[i])
            if(idx >= 0){
                str.push(createHTMLString(type, store_list[i], img, price[idx]));
            }
            else{
                str.push(createHTMLString(type, store_list[i], img, 0));
            }
        }
        container.innerHTML = str.join('');
    }
}

// Html 문서 
function createHTMLString(type, item, img, price) {
    if(price != 0)
        return `<div id="caketype">
        <label for="${type}${item}" onclick="selectCheck('${type}${item}')">
        <input id="${type} ${type}${item}" type="checkbox" name="${type}" checked value="${item}"></label>
        <img src="${img}" style="height : 100px">
        ${item}<br/>

        가격입력 : <input class = "${type}${item}" name="${type}price" type="text" value="${price}" style="width: 120px; " >
        </div>`;
    return `<div id="caketype">
    <label for="${type}${item}" onclick="selectCheck('${type}${item}')">
    <input id="${type} ${type}${item}" type="checkbox" name="${type}" value="${item}"></label>
    <img src="${img}" style="height : 100px"> ${item}<br/>
    
    <div>
    가격입력 : <input class = "${type}${item}" name="${type}price" type="text" value="${price}" style="width: 120px;"disabled>
    </div>
    
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