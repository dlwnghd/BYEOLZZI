
$(document).ready(function(){               // html 화면이 로딩되면 함수 실행
    
    // 챗봇 화면은 처음에 안보이게 해놓는다.
    $("#chatbot").hide();                      // 페이지를 열면 챗봇창 숨기기

    // '짐 꾸리는 중..' 버튼을 누르면 챗봇 화면이 열린다
    $("#chatbotbtn").click(function(){      // 클릭 이벤트 등록
        

        $("#wrapper").fadeOut(500);                // 대문 숨기고
        $("#chatbot").delay(500).fadeIn(1000);         // 챗봇창 화면에 표시
        
        

    });
});
