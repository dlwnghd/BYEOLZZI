
$(document).ready(function(){               // html 화면이 로딩되면 함수 실행
    
    // 챗봇 화면은 처음에 안보이게 해놓는다.
    $("#chatbot").hide();                      // 페이지를 열면 챗봇창 숨기기

    // '짐 꾸리는 중..' 버튼을 누르면 챗봇 화면이 열린다
    $("#chatbotbtn").click(function(){      // 클릭 이벤트 등록
        

        $("#wrapper").fadeOut(500);                // 대문 숨기고
        $("#chatbot").delay(500).fadeIn(1000);         // 챗봇창 화면에 표시
    });

    // SEND 버튼을 누르거나
    $("#sendbtn").click(function(){
        send_message();
    });

    // ENTER key 가 눌리면
    $("#chattext").keyup(function(event){
        if(event.keyCode == 13){
            send_message();
        }
    });
});

function send_message(){
    const chattext = $("#chattext").val().trim();
    console.log("여기까지 왔소")
    console.log("chattext" + chattext)

    // 입력한 메세지가 없으면 리턴
    if(chattext == ""){
        $("#chattext").focus();
        return;
    }
    
    // 입력한 채팅 출력
    let addtext = "<div style='margin:15px 0;text-align:right;'> <span style='padding:3px 10px;background-color:#3388cc;border-radius:3px;font-size:12px;'>" + chattext + "</span></div>";
    $("#chatbody").append(addtext); 
    console.log("addtext" + addtext)
    console.log("여기까지 왔소22")

    // API 서버에 보낼 데이터 준비
    const jsonData = {
        query: chattext,
        bottype: "WebClient"
    };

    $.ajax({
        url: 'http://127.0.0.10:5000/query/TEST',
        type: "POST",
        data: JSON.stringify(jsonData),
        dataType: "JSON",  // 응답받을 데이터 타입
        contentType: "application/json; charset=utf-8", //postman 에서 header 지정해준 그것
        crossDomain: true,
        success: function(response){
            console.log("Intent:" + response.Intent)
            // response.Answer 에 챗봇 응답메세지가 담겨 있음
            console.log(response.AnswerContents)
            $chatbody = $("#chatbody");
            let answercontents = response.AnswerContents
            let choicecontents = null
            let botcontents = null

            // 답변 출력
            bottext = "<div style='margin:15px 0;text-align:left;'><span style='padding:3px 10px;background-color:#DDD;border-radius:3px;font-size:12px;'>" + response.Answer + "</span></div>";
            $chatbody.append(bottext);
            console.log("answercontents:" + answercontents)
            console.log("NER:" + response.NER)
            console.log("NerList : ", response.NerList)
            
            if (response.Intent == '주변검색'){
                for (var i = 0; i < answercontents.length; i++){
                    botcontents = "<div style='margin:15px 0;text-align:left;'><span class='around_contents' style='padding:3px 10px;background-color:#DDD;border-radius:3px;font-size:12px;'>" + answercontents[i].title + "</span></div>";
                    $chatbody.append(botcontents);
                }
                
                $(".around_contents").click(function(){
                    let area_choice = $(this).text();
                    for (var i = 0; i < answercontents.length; i++){
                        if (answercontents[i].title == area_choice){
                            choicecontents = answercontents[i];
                        }
                    }
                    let localname = response.NerList[0];
                    let areachoice = choicecontents.title;
                    let addr = choicecontents.addr;
                    let mapx = choicecontents.mapx;
                    let mapy = choicecontents.mapy;

                    console.log("localname:", localname)

                    $("#iframe").attr("src", "aroundshow?localname=" + localname + "&areachoice=" + areachoice + "&addr=" + addr + "&mapx=" + mapx + "&mapy=" + mapy);

                })

            }
            
            else if (response.Intent == '길찾기'){
                let findway_list = JSON.stringify(response.NerList)
                console.log("findway_list : ", findway_list)
                
                // 좌표값을 requests 를 통해서 받아오기
                $.ajax({
                    url: 'navi',
                    type: 'get',
                    data: {
                        'findway_list': findway_list
                    },
                    dataType: 'json',
                    success: function(data){
                        
                        // 이건 B_location이 2개 잡힐 때,
                        if(data.endlong){

                            //받아온 데이터
                            let startlat = data.startlat
                            let startlong = data.startlong
                            let endlat = data.endlat
                            let endlong = data.endlong
                            console.log("받아온 startlat : ", startlat)

                            //src를 통해서 urls -> views 를 거쳐 데이터 전송하는 메소드
                            goToIframe(startlat, startlong, endlat, endlong)
                        }
                    }
                });
            }
            else if (response.Intent == '교통현황'){
                contents = "<br><table style='background-color:#DDD;border-radius:3px;font-size:12px;'><tr><td colspan='4'>[상행]</td></tr><tr><th>구간</th><th>거리</th><th>시속</th><th>상태</th></tr>"
                for (i = 0; i < answercontents['up'].length; i++){
                    // console.log("잘 뽑히니??",answercontents['up'][i]['section'], answercontents['up'][i]['distance'], 
                    // answercontents['up'][i]['speed'], answercontents['up'][i]['conditions'])
    
                    contents = contents + "<tr>"+
                    "<td>"+ answercontents['up'][i]['section']+"</td>"+
                    "<td>"+ answercontents['up'][i]['distance']+"</td>"+
                    "<td>"+ answercontents['up'][i]['speed']+"</td>"+
                    "<td>"+ answercontents['up'][i]['conditions']+"</td>" + "</tr>"
                    
                }
                contents = contents + "</table><br><br><table style='background-color:#DDD;border-radius:3px;font-size:12px;'><tr><td colspan='4'>[하행]</td></tr><tr><th>구간</th><th>거리</th><th>시속</th><th>상태</th></tr>"
    
                for (i = 0; i < answercontents['down'].length; i++){
                    // console.log("잘 뽑히니??",answercontents['down'][i]['section'], answercontents['down'][i]['distance'], 
                    // answercontents['down'][i]['speed'], answercontents['down'][i]['conditions'])
    
                    contents = contents + "<tr>"+
                    "<td>"+ answercontents['down'][i]['section']+"</td>"+
                    "<td>"+ answercontents['down'][i]['distance']+"</td>"+
                    "<td>"+ answercontents['down'][i]['speed']+"</td>"+
                    "<td>"+ answercontents['down'][i]['conditions']+"</td>" + "</tr>"
                    
                }
    
                answercontents = contents + "</table>"
                botcontents = "<div style='margin:15px 0;text-align:left;'>" + answercontents + "</div>";
                $chatbody.append(botcontents);

                $.ajax({
                    url:'highway',
                    type:'get',
                    data: {
                        'data' : response.NerList[0]
                    },
                    dataType: 'json',
                    
                    success: function(response){
                        console.log('허거허거허걱거헉1111111111')
                        console.log(response.data)
                        let $iframe = $('#iframe')
                        $iframe.attr('src','heeji?data='+response.data)
                        console.log('여기까지왔어어어어ㅓ엉ㅇ')
                    }
                });
            }
            
            // 스크롤 조정하기
            $chatbody.animate({scrollTop: $chatbody.prop('scrollHeight')});

            // 먼저 입력했던 내용은 지워줘야 함
            $("#chattext").val("");
            $("#chattext").focus();

            }
        })
    } // end 

function goToIframe(startlat, startlong, endlat, endlong){
    // document.getElementById("iframe").src = "movenavi?startlat=",startlat,"&startlong=",startlong,"&endlat=", endlat, "&endlong=", endlong;
    $("#iframe").attr("src", "applynavi?startlat="+startlat+"&startlong="+startlong+"&endlat="+endlat+"&endlong="+endlong);
}
