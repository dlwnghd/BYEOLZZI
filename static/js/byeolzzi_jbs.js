
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
            // response.Answer 에 챗봇 응답메세지가 담겨 있음
            $chatbody = $("#chatbody");
            let answercontents = response.AnswerContents

            // 답변 출력
            bottext = "<div style='margin:15px 0;text-align:left;'><span style='padding:3px 10px;background-color:#DDD;border-radius:3px;font-size:12px;'>" + response.Answer + "</span></div>";
            $chatbody.append(bottext);
            console.log("answercontents:" + answercontents)
            console.log("answer:" + response.answer)
            console.log("NER:" + response.NER)
            console.log("NerList[0]:" + response.NerList[0])
            console.log("NerList[1]:" + response.NerList[1])
            // <span style='padding:3px 10px;background-color:#DDD;border-radius:3px;'>
            li_full=""
            if(response.Intent=="축제"){
                for(i = 0; i<answercontents.length ; i++){
                    let table = `
                        <tr>
                            <td colspan="2">
                                <img src=`+answercontents[i]["image_small"]+` style="width:100px; height:100px;">
                            </td>
                        </tr>
                        <tr>
                            <td>
                                축제명 : 
                            </td>
                            <td>
                                `+answercontents[i]["title"]+`
                            </td>
                        </tr>
                        <tr>
                        <td>
                            시작일 : 
                        </td>
                        <td>
                            `+answercontents[i]["startDate"]+`
                        </td>
                    </tr>
                    `
                    li_full=li_full+table
                    }
        
                    fes_add="<table align='center' style='background-color:#DDD;border-radius:3px; font-size:12px;'><tr></tr>"+li_full+"</table>"
                    botcontents = "<div style='margin:15px 0;text-align:left;'>" + fes_add + "</div>";
                    $chatbody.append(botcontents);
                    console.log("여기까지 왔소33")
                    // for (var i = 0; i > answercontents.length(); i++){
                    //     botcontents += "<div style='margin:15px 0;text-align:left;'><span style='padding:3px 10px;background-color:#DDD;border-radius:3px;'>" + answercontents[i] + "</span></div>";
                    // } 
                    // console.log("bottext" + bottext)
        
                    // botcontents = "<div style='margin:15px 0;text-align:left;'><span style='padding:3px 10px;background-color:#DDD;border-radius:3px;'>" + answercontents + "</span></div>";
                    // $chatbody.append(botcontents);
                    // console.log("여기까지 왔소33"
                    
                    $.ajax({
                        url:'festival',
                        type:'get',
                        data: {
                            'ner' : response.NerList[0],
                            'met_code' : response.met_code,
                            'loc_code' : response.loc_code
                        },
                        dataType: 'json',
                        success: function(context){
                        ner = context.ner
                        met_code = context.met_code
                        loc_code = context.loc_code
                        console.log("드디어 여기까지")
                        let $iframe = $('#iframe')
        
                        console.log('$iframe.src 전: ',$iframe.attr('src'))
        
                        $iframe.attr('src','festivals/?ner='+ner+'&met_code='+met_code+'&loc_code='+loc_code)
        
                        console.log('$iframe.src 후: ', $iframe.attr('src'))
                        console.log('여기까지 왔소희지희지')
                    }});
            }
            

            // 스크롤 조정하기
            $chatbody.animate({scrollTop: $chatbody.prop('scrollHeight')});

            // 먼저 입력했던 내용은 지워줘야 함
            $("#chattext").val("");
            $("#chattext").focus();

        },

    })

} // end 
