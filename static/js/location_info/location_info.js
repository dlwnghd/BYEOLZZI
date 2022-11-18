  /* * * * * * * * *  여기서부터 여행지 div js * * * * * * * * */
function location_info_js(maxSlide) {
  
  let currSlide = 1;  // 버튼 클릭할 때 마다 현재 슬라이드가 어디인지 알려주기 위한 변수

  for (let i = 0; i < maxSlide; i++) {
    if (i == 0) {$(".slide_pagination").append(`<li class="active">•</li>`)}
    else {$(".slide_pagination").append(`<li>•</li>`)}
  }

  function nextMove() {
    currSlide++;
    // 마지막 슬라이드 이상으로 넘어가지 않게 하기 위해서
    if (currSlide <= maxSlide) {
      const offset = $(".slide").width() * (currSlide - 1);                                   // 슬라이드를 이동시키기 위한 offset 계산
      $(".slide_item").each(function(i, v){v.setAttribute("style", `left: ${-offset}px`);});  // 각 슬라이드 아이템의 left에 offset 적용
      $(".slide_pagination > li").each(function(i, v){v.classList.remove("active");});        // 슬라이드 이동 시 현재 활성화된 pagination 변경
      $(".slide_pagination > li:eq(" + (currSlide - 1) + ")").addClass("active");             // 슬라이드 이동 시 현재 활성화된 pagination 변경

    } else {currSlide--;}
  }
  function prevMove() {
    currSlide--;
    // 1번째 슬라이드 이하로 넘어가지 않게 하기 위해서
    if (currSlide > 0) {
      const offset = $(".slide").width() * (currSlide - 1);                                   // 슬라이드를 이동시키기 위한 offset 계산
      $(".slide_item").each(function(i, v){v.setAttribute("style", `left: ${-offset}px`);});  // 각 슬라이드 아이템의 left에 offset 적용
      $(".slide_pagination > li").each(function(i, v){v.classList.remove("active");});        // 슬라이드 이동 시 현재 활성화된 pagination 변경
      $(".slide_pagination > li:eq(" + (currSlide - 1) + ")").addClass("active");             // 슬라이드 이동 시 현재 활성화된 pagination 변경

    } else {currSlide++;}
  }

  // 버튼 엘리먼트에 클릭 이벤트 추가하기
  $(".slide_next_button").on("click", () => {nextMove();});   // 이후 버튼 누를 경우 현재 슬라이드를 변경
  $(".slide_prev_button").on("click", () => {prevMove();});   // 이후 버튼 누를 경우 현재 슬라이드를 변경

  // 각 페이지네이션 클릭 시 해당 슬라이드로 이동하기
  for (let i = 0; i < maxSlide; i++){
     // 각 페이지네이션마다 클릭 이벤트 추가하기
    $(".slide_pagination > li").on("click", () => {
      currSlide = i + 1;    // 클릭한 페이지네이션에 따라 현재 슬라이드 변경해주기(currSlide는 시작 위치가 1이기 때문에 + 1)
      const offset = $(".slide").width() * (currSlide - 1);                                   // 슬라이드를 이동시키기 위한 offset 계산
      $(".slide_item").each(function(i, v){v.setAttribute("style", `left: ${-offset}px`);});  // 각 슬라이드 아이템의 left에 offset 적용
      $(".slide_pagination > li").each(function(i, v){v.classList.remove("active");});        // 슬라이드 이동 시 현재 활성화된 pagination 변경
      $(".slide_pagination > li:eq(" + (currSlide - 1) + ")").addClass("active");             // 슬라이드 이동 시 현재 활성화된 pagination 변경
    }); 
  }

  // 드래그(스와이프) 이벤트를 위한 변수 초기화
  let startPoint = 0;
  let endPoint = 0;

  $(".slide").mousedown(function(e) {
    console.log("mousedown", e.pageX);
    startPoint = e.pageX; // 마우스 드래그 시작 위치 저장
  });

  $(".slide").mouseup(function(e) {
    console.log("mouseup", e.pageX);
    endPoint = e.pageX; // 마우스 드래그 끝 위치 저장
    if (startPoint < endPoint){
      // 마우스가 오른쪽으로 드래그 된 경우
      console.log("prev move");
      prevMove();
    } else if (startPoint > endPoint){
      // 마우스가 왼쪽으로 드래그 된 경우
      console.log("next move");
      nextMove();
    }
  });
}

// 여행지정보 함수
function location_info_crawling(NerList) {   

  // 아래 for문까지는 네이버여행지에 있는 지역명과 사용자가 입력한 지역명을 일치시켜주는 작업.
  let naver_dic = { "강원" : "01", "강릉시" : "01150", "고성군" : "01820", "동해시" : "01170", "삼척시" : "01230", "속초시" : "01210", "양구군" : "01800", "양양군" : "01830", "영월군" : "01750", "원주시" : "01130", "인제군" : "01810", "정선군" : "01770", "철원군" : "01780", "춘천시" : "01110", "태백시" : "01190", "평창군" : "01760", "홍천군" : "01720", "화천군" : "01790", "횡성군" : "01730", "경기" : "02", "가평군" : "02820", "고양시" : "02280", "과천시" : "02290", "광명시" : "02210", "광주시" : "02610", "구리시" : "02310", "군포시" : "02410", "김포시" : "02570", "남양주시" : "02360", "동두천시" : "02250", "부천시" : "02190", "성남시" : "02130", "수원시" : "02110", "시흥시" : "02390", "안산시" : "02270", "안성시" : "02550", "안양시" : "02170", "양주시" : "02630", "양평군" : "02830", "여주시" : "02670", "연천군" : "02800", "오산시" : "02370", "용인시" : "02460", "의왕시" : "02430", "의정부시" : "02150", "이천시" : "02500", "파주시" : "02480", "평택시" : "02220", "포천시" : "02650", "하남시" : "02450", "화성시" : "02590", "경남" : "03", "거제시" : "03310", "거창군" : "03880", "고성군" : "03820", "김해시" : "03250", "남해군" : "03840", "밀양시" : "03270", "사천시" : "03240", "산청군" : "03860", "양산시" : "03330", "의령군" : "03720", "진주시" : "03170", "창녕군" : "03740", "창원시" : "03120", "통영시" : "03220", "하동군" : "03850", "함안군" : "03730", "함양군" : "03870", "합천군" : "03890", "경북" : "04", "경산시" : "04290", "경주시" : "04130", "고령군" : "04830", "구미시" : "04190", "군위군" : "04720", "김천시" : "04150", "문경시" : "04280", "봉화군" : "04920", "상주시" : "04250", "성주군" : "04840", "안동시" : "04170", "영덕군" : "04770", "영양군" : "04760", "영주시" : "04210", "영천시" : "04230", "예천군" : "04900", "울릉군" : "04940", "울진군" : "04930", "의성군" : "04730", "청도군" : "04820", "청송군" : "04750", "칠곡군" : "04850", "포항시" : "04110", "광주" : "05", "광산구" : "05200", "남구" : "05155", "동구" : "05110", "북구" : "05170", "서구" : "05140", "대구" : "06", "남구" : "06200", "달서구" : "06290", "달성군" : "06710", "동구" : "06140", "북구" : "06230", "서구" : "06170", "수성구" : "06260", "중구" : "06110", "대전" : "07", "대덕구" : "07230", "동구" : "07110", "서구" : "07170", "유성구" : "07200", "중구" : "07140", "부산" : "08", "강서구" : "08440", "금정구" : "08410", "기장군" : "08710", "남구" : "08290", "동구" : "08170", "동래구" : "08260", "부산진구" : "08230", "북구" : "08320", "사상구" : "08530", "사하구" : "08380", "서구" : "08140", "수영구" : "08500", "연제구" : "08470", "영도구" : "08200", "중구" : "08110", "해운대구" : "08350", "서울" : "09", "강남구" : "09680", "강동구" : "09740", "강북구" : "09305", "강서구" : "09500", "관악구" : "09620", "광진구" : "09215", "구로구" : "09530", "금천구" : "09545", "노원구" : "09350", "도봉구" : "09320", "동대문구" : "09230", "동작구" : "09590", "마포구" : "09440", "서대문구" : "09410", "서초구" : "09650", "성동구" : "09200", "성북구" : "09290", "송파구" : "09710", "양천구" : "09470", "영등포구" : "09560", "용산구" : "09170", "은평구" : "09380", "종로구" : "09110", "중구" : "09140", "중랑구" : "09260", "세종" : "17", "울산" : "10", "남구" : "10140", "동구" : "10170", "북구" : "10200", "울주군" : "10710", "중구" : "10110", "인천" : "11", "강화군" : "11710", "계양구" : "11245", "남동구" : "11200", "동구" : "11140", "미추홀구" : "11177", "부평구" : "11237", "서구" : "11260", "연수구" : "11185", "옹진군" : "11720", "중구" : "11110", "전남" : "12", "강진군" : "12810", "고흥군" : "12770", "곡성군" : "12720", "광양시" : "12230", "구례군" : "12730", "나주시" : "12170", "담양군" : "12710", "목포시" : "12110", "무안군" : "12840", "보성군" : "12780", "순천시" : "12150", "신안군" : "12910", "여수시" : "12130", "영광군" : "12870", "영암군" : "12830", "완도군" : "12890", "장성군" : "12880", "장흥군" : "12800", "진도군" : "12900", "함평군" : "12860", "해남군" : "12820", "화순군" : "12790", "전북" : "13", "고창군" : "13790", "군산시" : "13130", "김제시" : "13210", "남원시" : "13190", "무주군" : "13730", "부안군" : "13800", "순창군" : "13770", "완주군" : "13710", "익산시" : "13140", "임실군" : "13750", "장수군" : "13740", "전주시" : "13110", "정읍시" : "13180", "진안군" : "13720", "제주" : "14", "서귀포시" : "14130", "제주시" : "14110", "충남" : "15", "계룡시" : "15250", "공주시" : "15150", "금산군" : "15710", "논산시" : "15230", "당진시" : "15270", "보령시" : "15180", "부여군" : "15760", "서산시" : "15210", "서천군" : "15770", "아산시" : "15200", "예산군" : "15810", "천안시" : "15130", "청양군" : "15790", "태안군" : "15825", "홍성군" : "15800", "충북" : "16", "괴산군" : "16760", "단양군" : "16800", "보은군" : "16720", "영동군" : "16740", "옥천군" : "16730", "음성군" : "16770", "제천시" : "16150", "증평군" : "16745", "진천군" : "16750", "청주시" : "16110", "충주시" : "16130", };
  let location_no = "";
  for(location_name in naver_dic){
      if(location_name.includes(NerList)){        // 사용자가 입력한 지역이 저장되어있는 지역명에 포함되어 있는 경우
        location_no = naver_dic[location_name] ;  // 포함되어있는지 확인
        break;
      }
      else if(NerList.includes(location_name)) {  // 사용자가 입력한 지역명에 저장되어있는 지역명이 포함되어 있는 경우
        location_no = naver_dic[location_name] ;  // 포함되어있는지 확인
        break;
      }
  }
  let url = `https://travel.naver.com/domestic/${location_no}/summary`;   // 크롤링 url

  $("#iframe").attr("src", "location_info?url=" + url)  // iframe에 url을 넘기면 urls.py 로 서버 통신 가능.


  /*

  // 관광공사 api //
  let serviceKey = '기간만료';  // 인증키 
  let pageNo = 1;              // 페이지 번호 
  let numOfRows = 30;          // 한페이지에 몇개의 결과물을 가져올지. 
  let MobileOS = 'ETC';        // OS 구분 : IOS (아이폰), AND (안드로이드), WIN (윈도우폰), ETC(기타) 
  let MobileApp = 'AppTest';   // 서비스명 
  let keyword = NerList;       // 여행지 키워드 
  let url = `https://apis.data.go.kr/B551011/KorService/searchKeyword?serviceKey=${serviceKey}&numOfRows=${numOfRows}&pageNo=${pageNo}&MobileOS=${MobileOS}&MobileApp=${MobileApp}&_type=json&listYN=Y&arrange=C&keyword=${keyword}`;

  $.ajax({
    url : url,
    type : "get",
    success: function(data, status){

      let img_i = 0;
      let location_div = '<div class="slide slide_wrap" id="location_info_slide"><div class="slide_prev_button slide_button">◁</div><div class="slide_next_button slide_button">▷</div><ul class="slide_pagination"></ul></div>';
      $(".result_container").prepend(location_div);   // 슬라이드로 사용할 div 를 추가해줌 
      $(".iframe_area").hide()                        // 기존에 있는 iframe 을 감춰줌 
      console.log('★★★★★')
      // data.response.body.items.item.length // 이건 item 갯수 확인하는거
      for(i=0; i < data.response.body.items.item.length; i++ ){
        if(data.response.body.items.item[i].firstimage != ""){      // 이미지가 비어있지 않으면 이라는 조건문
          let l_title = data.response.body.items.item[i].title;     // 타이틀 저장
          let l_img = data.response.body.items.item[i].firstimage;  // 이미지 저장
          let location_info_div = '<div class="slide_item"><h1>' + l_title + '</h1><img src="' + l_img + '"></div>';    // 타이틀과 이미지를 새로운 div, img 태그에 넣어줌
          $("#location_info_slide").prepend(location_info_div);     // 타이틀과 이미지를 담은 태그를 슬라이드용 div태그에 넣어줌.
          img_i++;                  // append 는 뒤에, prepend 는 앞에 요소를 추가함
        }
      }
      location_info_js(img_i);    // 위에 추가한 태그들이 js 적용받을수 있게 함수로 js를 실행해줌. (js함수 안에서는 꼭 J쿼리로 해야함 JS 로 하면 추가된 태그에 도큐먼트 태그로 접근할수 없음.)
    },
  });
  */
};

/* * * * * * * * *  여기까지 여행지 div js * * * * * * * * */