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
// 가게 디테일 부분 열고 닫기 
function 열기(num) {
    document.getElementsByClassName('items')[num].style.display = 'block';
    document.getElementsByClassName('items')[(num + 1) % 3].style.display = 'none';
    document.getElementsByClassName('items')[(num + 2) % 3].style.display = 'none';
}
// 위치 디테일 부분 열고 닫기 
function 열기1(num1) {
    document.getElementsByClassName('items1')[num1].style.display = 'block';
    document.getElementsByClassName('items1')[(num1 + 1) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 2) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 3) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 4) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 5) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 6) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 7) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 8) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 9) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 10) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 11) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 12) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 13) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 14) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 15) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 16) % 18].style.display = 'none';
    document.getElementsByClassName('items1')[(num1 + 17) % 18].style.display = 'none';
    
}