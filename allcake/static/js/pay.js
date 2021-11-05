var IMP = window.IMP;
IMP.init('imp60585611');
//주문 페이지에 가맹점 식별코드를 이용하여 IMP 객체를 초기화합니다.


function requestPay(order_id, amount) {
    var merchant_uid = AjaxInitTransaction(order_id);

    if (merchant_uid !== '') {
        // IMP.request_pay(param, callback) (결제창 호출) 순서대로 param, callback함수
        IMP.request_pay(
            //param
            // pay_method 필수라는데, 일단 비워둔다. buyer_tell 또한 필수라는데, 비우고 시도.
            {
                merchant_uid: merchant_uid,
                name: "Allcakes",
                amount: amount
            },function (rsp){
                if (rsp.success) {
                    // 결제 성공 시 로직
                    AjaxImpTransaction(order_id, rsp.merchant_uid, rsp.imp_uid, rsp.paid_amount);
                    // 결제 내용 api호출 통한 검증, 실제 결제금액과 DB의 가격 비교
                    // 가상계좌 입금을 생각하면 응답 객체의 status도 저장해줘야 할듯.
                    // 이러한 위변조 문제 좀더 생각해보기.

                    // 결론: DB와 가격비교 해주고, 필수는 아니나, 서버와 통신까지 하면 좋을듯, 어차피 거래정보 확인 필요시
                    // 호출할 수 있어야 함.
                }
                else {
                    var msg = "결제에 실패했습니다.";
                    msg += '에러내용: ' + rsp.error_msg;
                    console.log(msg);
                }
            }
        );
    }



    
}


function AjaxInitTransaction(order_id) {
    var merchant_uid = '';
    var request = $.ajax({
        method:"POST",
        url: order_init_transaction_url,
        async: false,
        data: {
            order_id: order_id,
            csrfmiddlewaretoken: csrf_token
        }
    });
    request.done(function (data){
        if (data.works) {
            merchant_uid = data.merchant_uid
        }
    });
    request.fail(function (jqXHR, textStatus) {
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        }
        else if (jqXHR.status == 403) {
            alert("로그인이 되지 않았습니다.");
        }
        else {
            alert("거래 생성에 실패했습니다.");
        }
    });
    // 공백 혹은 주문번호 return
    return merchant_uid;
}

function AjaxImpTransaction(order_id, merchant_uid, imp_uid, amount) {
    var request = $.ajax({
        method:"POST",
        url: order_validation_url,
        async: false,
        data: {
            order_id: order_id,
            merchant_uid: merchant_uid,
            imp_uid: imp_uid,
            amount: amount,
            csrfmiddlewaretoken: csrf_token
        }
    });
    request.done(function (data) {
        if (data.works) {
            $(location).attr('href', location.origin+order_complete_url+'?order_id='+order_id);
        }
    });
    request.fail(function (jqXHR, textStatus) {
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        }
        else if (jqXHR.status == 403) {
            alert("로그인이 되지 않았습니다.");
        }
        else if (jqXHR.status == 402) {
            alert("위변조가 감지되었습니다.");
            // 이 경우 결제 자동 취소하도록 하기.
        }
        else {
            alert("유효하지 않은 거래입니다.");
        }
    });
}

// 아직 구현 남은 부분: 1. 결제정보 조회 api호출하기(requests 사용),
// 2. 위변조시 결제 자동취소,
// 3. 간단한거지만, 결제완료 메세지 만들기