dust_color = document.getElementById("dust"); // 미세먼지
dust_stat = document.getElementById("dust_stat").innerText; // 미세먼지 상태

micro_dust_color = document.getElementById("micro_dust"); // 초미세먼지
micro_dust_stat = document.getElementById("micro_dust_stat").innerText; // 초미세먼지 상태

sun_color = document.getElementById("sun"); // 자외선
sun_stat = document.getElementById("sun_stat").innerText; // 자외선 상태

sunrise_color = document.getElementById("sunrise"); // 일출
sunrise_time = document.getElementById("sunrise_time").innerText; // 일출 시간

good = "좋음";
normal = "보통";
bad = "나쁨";
worst = "매우 나쁨";

// 미세먼지
if (dust_stat == good) {
    dust_color.style.backgroundColor = "var(--good_background-color)";
    dust_color.style.color = "var(--good_color)";
    console.log("미세먼지 좋음");
}else if (dust_stat == normal) {
    dust_color.style.backgroundColor = "var(--normal_background-color)";
    dust_color.style.color = "var(--normal_color)";
    console.log("미세먼지 보통");
}else if (dust_stat == bad) {
    dust_color.style.backgroundColor = "var(--bad_background-color)";
    dust_color.style.color = "var(--bad_color)";
    console.log("미세먼지 나쁨");
}else if (dust_stat == worst) {
    dust_color.style.backgroundColor = "var(--worst_background-color)";
    dust_color.style.color = "var(--worst_color)";
    console.log("미세먼지 매우 나쁨");
}

// 초미세먼지
if (micro_dust_stat == good) {
    micro_dust_color.style.backgroundColor = "var(--good_background-color)";
    micro_dust_color.style.color = "var(--good_color)";
    console.log("초미세먼지 좋음");
}else if (micro_dust_stat == normal) {
    micro_dust_color.style.backgroundColor = "var(--normal_background-color)";
    micro_dust_color.style.color = "var(--normal_color)";
    console.log("초미세먼지 보통");
}else if (micro_dust_stat == bad) {
    micro_dust_color.style.backgroundColor = "var(--bad_background-color)";
    micro_dust_color.style.color = "var(--bad_color)";
    console.log("초미세먼지 나쁨");
}else if (micro_dust_stat == worst) {
    micro_dust_color.style.backgroundColor = "var(--worst_background-color)";
    micro_dust_color.style.color = "var(--worst_color)";
    console.log("초미세먼지 매우 나쁨");
}

// 자외선
if (sun_stat == good) {
    sun_color.style.backgroundColor = "var(--good_background-color)";
    sun_color.style.color = "var(--good_color)";
    console.log("자외선 좋음");
}else if (sun_stat == normal) {
    sun_color.style.backgroundColor = "var(--normal_background-color)";
    sun_color.style.color = "var(--normal_color)";
    console.log("자외선 보통");
}else if (sun_stat == bad) {
    sun_color.style.backgroundColor = "var(--bad_background-color)";
    sun_color.style.color = "var(--bad_color)";
    console.log("자외선 나쁨");
}else if (sun_stat == worst) {
    sun_color.style.backgroundColor = "var(--worst_background-color)";
    sun_color.style.color = "var(--worst_color)";
    console.log("자외선 매우 나쁨");
}

weather = document.getElementById("weather").className;
frame_color = document.getElementById("weather_body");

console.log(weather);
console.log(frame_color);

if (weather == "비" || weather == "흐림") {
    frame_color.style.backgroundColor = "#8b8d90";
} else if(weather == "맑음" || weather == "구름조금" || weather == "구름많음") {
    frame_color.style.backgroundColor = "dodgerblue";
    // frame_color = "#58a3fe";
    // frame_color = "lightskyblue";
    // frame_color = "deepskyblue";
    // frame_color = "cornflowerblue";
    // frame_color = "skyblue";
} else if(weather == "눈") {
    frame_color.style.backgroundColor = "#87b4ed";
}