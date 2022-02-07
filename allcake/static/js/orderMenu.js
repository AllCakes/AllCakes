// simulation
const click_list = document.querySelectorAll('.butn');
for (var i = 0; i < click_list.length; i++) {
    click_list[i].addEventListener('click', event => { onMenuClick(event) });
}
function onMenuClick(event) {
    const dataset = event.target.dataset;
    const k = dataset.key;
    const key = k.split(',');

    if (key[0] === 'letter') {
        mesg = document.getElementById('id_lettering_position').value;
        console.log(mesg)
        if (mesg == "케이크에 직접 레터링") {
            document.getElementById('letter_pos1').style.display = 'none';
            document.getElementById('letter_pos2').style.display = 'block';
        }
        else {
            document.getElementById('letter_pos1').style.display = 'block';
            document.getElementById('letter_pos2').style.display = 'none';
        }
    }
    else {
        // 나머지 닫기
        sumPrice()
        list = document.getElementsByClassName(`${key[0]}sel`);
        for (i of list) {
            i.style.display = 'none';
        }
        // 그것만 열기
        document.getElementById(`${key[0]}${key[1]}`).style.display = 'block';
    }
}

// color 부분
var c_key = Object.keys(color_list)
for (var i = 0; i < c_key.length; i++) {
    const t1 = document.querySelector(`.color_${c_key[i]}`)
    t1.innerHTML = color_list[c_key[i]] + "원"
}
// cream 부분
c_key = Object.keys(cream_list)
for (var i = 0; i < c_key.length; i++) {
    const t1 = document.querySelector(`.cream_${c_key[i]}`)
    t1.innerHTML = color_list[c_key[i]] + "원"
}

function sumPrice() {
    // 가격 계산
    var price_cream = 0, price_color = 0;
    var cream_query = document.querySelector('input[name="cream"]:checked');
    var color_query = document.querySelector('input[name="color"]:checked');
    if (cream_query) {
        idx = cream_query.value
        price_cream = cream_list[idx]
    }
    if (color_query) {
        idx = color_query.value;
        price_color = color_list[idx]
    }

    var total = Number("{{cake.price}}") + Number(price_color) + Number(price_cream);
    console.log(total)
    document.getElementById('total_price').value = total;
}

function goBack() {
    window.history.back();
}

function coupon(x) {
    document.getElementById('coupon').style.display = x;
}

function discount() {
    var price = document.getElementById('total_price').value;
    console.log(price)
    var ele = document.getElementsByName('discount');
    var discounted_price = 0;
    var check = 0;
    var val = 0;
    var pk = 0;

    for (i = 0; i < ele.length; i++) {
        if (ele[i].checked) {
            check = 1;
            val = ele[i].value.split(' ')[0];
            pk = ele[i].value.split(' ')[1];
            if (val <= 100) {
                discounted_price = price * (100 - val) / 100;
                document.getElementById('coupon-pk').setAttribute("value", "p_" + pk);
            } else {
                discounted_price = price - val;
                document.getElementById('coupon-pk').setAttribute("value", "a_" + pk);
            }
        }
    }
    if (check == 0) {
        discounted_price = price;
    }
    document.getElementById('total').innerHTML = discounted_price;
}