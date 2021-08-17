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
    document.getElementsByClassName('items')[(num + 1) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 2) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 3) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 4) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 5) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 6) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 7) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 8) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 9) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 10) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 11) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 12) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 13) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 14) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 15) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 16) % 18].style.display = 'none';
    document.getElementsByClassName('items')[(num + 17) % 18].style.display = 'none';
    
}