function add_event() {
    console.log("add event")
    // parsing
    var list = menu.replace(/&#x27;/g, "").replaceAll(" ", "").replace("[", "").replace("]", "").split(',')

    // check - 기존에 있는 메뉴인지
    // value 가져오기
    const newcolor = document.getElementById('색추가').value
    const newcream = document.getElementById('크림추가').value
    if (newcolor === "" && newcream === "") {
        confirm("아무것도 입력되지 않았습니다.")
        return
    }
    for (i in list) {
        // 기존에 있다면, 팝업창 띄움
        if (list[i] === newcolor || list[i] === newcream) {
            confirm("재확인해주세요")
            return
        }
    }
    const e = `/add_menu/${pk}`
    console.log(e)
    // $.ajax({
    //     url = 'add_menu',
    //     data: {
    //         'newcolor': newcolor,
    //         'newcream': newcream
    //     },
    //     dataType: "json",
    //     success :function(response){
    //         confirm(response.message)
    //         window.location.reload()
    //     },
    // })
}