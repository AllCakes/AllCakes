function LikeIt(object_type, object_id) {
        var request = $.ajax({
            method: "POST",
            url: like_url,
            async: false,
            // 좋아요 종류와 obj_id를 전달
            data: {
                type: object_type,
                obj_id: object_id,
                csrfmiddlewaretoken: csrf_token
            }
        });
        request.fail(function(data){
            alert("error")
        });

        // 클래스 바꿔주기
        // 좋아요 
        if (object_type == 1)
            var str = "cake";
        else if (object_type == 2)
            var str = "store";
        var ele = document.getElementById(str.concat(object_id));

        ele.classList.toggle("red");
}
// function ChangeHeart() {
//     if (this.classList.contains('red')){
//         this.classList.remove('red');
//         this.classList.add('black');
//     }
//     else{
//         this.classList.remove('black');
//         this.classList.add('red');
//     }
// }
// const likebutton = document.getElementsByClassName("like");
// for (var i=0 ; i < likebutton.length ; i++){
//     likebutton[i].addEventListener("click", function(){
//         likebutton[i].classList.toggle("red");
//     });
// }