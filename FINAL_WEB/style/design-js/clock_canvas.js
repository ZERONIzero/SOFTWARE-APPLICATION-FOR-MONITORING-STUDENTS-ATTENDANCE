let canvas = document.getElementById("clock-label");
let ctx = canvas.getContext("2d");

canvas.style.width="80%";
canvas.style.marginTop = "20px";
canvas.style.marginLeft = "auto";
canvas.style.marginRight = "auto";
canvas.style.border = "2px solid white";
canvas.style.borderRadius = "20px";

let url_to_font_name = "/font/Naziona.otf";
let font_name = new FontFace('Number_clock', `url(${url_to_font_name})`);

let fontSize;

function clear(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function start(){
    clear();
    let date = new Date();
    let hours = date.getHours();
    let minutes = date.getMinutes();

    if (String(minutes).length < 2){
        minutes = "0"+String(minutes);
    }
    if (String(hours).length < 2){
        hours = "0"+String(hours);
    }

    fontSize = canvas.width / 5;

    let time = String(hours)+" : "+String(minutes);
    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.strokeStyle = "white";
    ctx.lineWidth = 1;
    ctx.font = `${fontSize}px Number_clock`;
    ctx.textAlign = "center";
    ctx.fillText(time,parseInt(canvas.width)/2,(2*parseInt(canvas.height))/4);
    ctx.fill();

    let year = date.getFullYear();
    let month = parseInt(date.getMonth())+1;
    let day = date.getDate();

    if (String(month).length < 2){
        month = "0"+String(month);
    }
    if (String(day).length < 2){
        day = "0"+String(day);
    }
    
    let date_together = String(day)+"."+String(month)+"."+String(year);

    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.strokeStyle = "white";
    ctx.lineWidth = 1;
    fontSize = canvas.width / 10;
    ctx.font = `${fontSize}px Number_clock`;
    ctx.textAlign = "center";
    ctx.fillText(date_together,parseInt(canvas.width)/2,(3*parseInt(canvas.height))/4);
    ctx.fill();
    window.requestAnimationFrame(start);
}

window.addEventListener('resize', () => {
    checkWindowSize();
    updateButtonSizes();
});

function checkWindowSize() {
    if (window.innerWidth < 1250) {
        removeInfoTab();
        create_m_info();
    } else {
        createInfoTab();
        destroy_m_info();
    }
}

let savedInfoTab = null;
let savedInfoTabM = null;

function removeInfoTab() {
    const infoTab = document.getElementById("info-tab");
    if (infoTab) {
        savedInfoTab = infoTab.cloneNode(true);
        infoTab.remove();
    }
}

function destroy_m_info() {
    const infoTab_m = document.getElementById("m_nav");
    if (infoTab_m) {
        savedInfoTabM = infoTab_m.cloneNode(true);
        infoTab_m.remove();
    }
}


function createInfoTab() {
    if (savedInfoTab && !document.getElementById("info-tab")) {
        const row = document.querySelector('.row.flex-nowrap');
        row.insertBefore(savedInfoTab, row.firstChild);
        
        canvas = document.getElementById("clock-label");
        ctx = canvas.getContext("2d");
        
        canvas.style.width = "80%";
        canvas.style.marginTop = "20px";
        canvas.style.marginLeft = "auto";
        canvas.style.marginRight = "auto";
        canvas.style.border = "2px solid white";
        canvas.style.borderRadius = "20px";
        
    }
}

function create_m_info() {
    if (savedInfoTabM && !document.getElementById("m_nav")) {
        const page = document.getElementsByName("body");
        page.insertBefore(savedInfoTabM,page.firstChild);
    }
}

font_name.load().then(function(loadedFont) {
    document.fonts.add(loadedFont);
    start();
}).catch(function(error) {
    console.error('Font loading failed:', error);
});

function updateButtonSizes() {
    let w_height = window.innerHeight - 20;

    document.getElementById("function-tab").style.paddingLeft = "0px";
    document.getElementById("function-tab").style.paddingRight = "0px";

    document.getElementById("container-btn").style.height = "100%";
    document.getElementById("container-btn").style.width = "100%";

    let button_schedule = document.getElementById("col-1");
    button_schedule.style.paddingLeft = "0px";
    button_schedule.style.paddingRight = "0px";

    let button_setting = document.getElementById("col-2");
    button_setting.style.paddingLeft = "0px";
    button_setting.style.paddingRight = "0px";

    let button_add = document.getElementById("col-3");
    button_add.style.paddingLeft = "0px";
    button_add.style.paddingRight = "0px";

    let button_room = document.getElementById("col-4");
    button_room.style.paddingLeft = "0px";
    button_room.style.paddingRight = "0px";

    resetButtonStyles(button_schedule);
    resetButtonStyles(button_setting);
    resetButtonStyles(button_add);
    resetButtonStyles(button_room);

    button_schedule.style.textDecoration = "none";
    button_setting.style.textDecoration = "none";
    button_add.style.textDecoration = "none";
    button_room.style.textDecoration = "none";

    button_schedule.style.backgroundColor = "#f94144";
    button_schedule.style.borderRadius = "20px";

    button_setting.style.backgroundColor = "#277DA1";
    button_setting.style.borderRadius = "20px";

    button_add.style.backgroundColor = "#F8961E";
    button_add.style.borderRadius = "20px";

    button_room.style.backgroundColor = "#90BE6D";
    button_room.style.borderRadius = "20px";

    if (window.innerWidth < 1250){

        button_schedule.style.height = "300px";
        button_schedule.style.width = "100%";

        let margin_px_w_m = parseInt((button_schedule.offsetWidth-300)/2);

        button_schedule.style.width = "300px";
        button_schedule.style.marginLeft = "auto" ;
        button_schedule.style.marginRight = "auto" ;
        button_schedule.style.marginBottom = String(margin_px_w_m*2)+"px";


        button_setting.style.height = "300px";
        button_setting.style.width = "100%";

        button_setting.style.width = "300px";
        button_setting.style.marginLeft = "auto";
        button_setting.style.marginRight = "auto";
        button_setting.style.marginBottom = String(margin_px_w_m*2)+"px";


        button_add.style.height = "300px";
        button_add.style.width = "100%";

        button_add.style.width = "300px";
        button_add.style.marginLeft = "auto";
        button_add.style.marginRight = "auto";
        button_add.style.marginBottom = String(margin_px_w_m*2)+"px";
        
        button_room.style.height = "300px";
        button_room.style.width = "100%";

        button_room.style.width = "300px";
        button_room.style.marginLeft = "auto";
        button_room.style.marginRight = "auto";
        button_room.style.marginBottom = String(margin_px_w_m*2)+"px";

    } else {

        button_schedule.style.height = String(Math.round(w_height / 2)) + "px";
        let margin_px_h = parseInt(button_schedule.offsetHeight) / 5;
        button_schedule.style.height = String(margin_px_h * 3) + "px";
        button_schedule.style.marginTop = String(margin_px_h) + "px";
        button_schedule.style.marginBottom = String(margin_px_h) + "px";
        let margin_px_w = parseInt(button_schedule.offsetWidth-10);
        button_schedule.style.width = String(margin_px_h * 3) + "px";
        button_schedule.style.marginLeft = String((margin_px_w - button_schedule.offsetWidth) / 2) + "px";
        button_schedule.style.marginRight = String((margin_px_w - button_schedule.offsetWidth) / 2) + "px";
        
        document.getElementById("icon-btn1").style.width = "80%";
        document.getElementById("icon-btn1").style.height = document.getElementById("icon-btn1").offsetWidth;
        document.getElementById("icon-btn1").style.marginLeft = "20%";
        document.getElementById("icon-btn1").style.marginTop = "8%";

        button_setting.style.height = String((w_height / 2)) + "px";
        let margin_px_h1 = parseInt(button_setting.offsetHeight) / 5;
        button_setting.style.height = String(margin_px_h1 * 3) + "px";
        button_setting.style.marginTop = String(margin_px_h1) + "px";
        button_setting.style.marginBottom = String(margin_px_h1) + "px";
        let margin_px_w1 = parseInt(button_setting.offsetWidth-10);
        button_setting.style.width = String(margin_px_h1 * 3) + "px";
        button_setting.style.marginLeft = String((margin_px_w1 - button_setting.offsetWidth) / 2) + "px";
        button_setting.style.marginRight = String((margin_px_w1 - button_setting.offsetWidth) / 2) + "px";

        document.getElementById("icon-btn2").style.width = "80%";
        document.getElementById("icon-btn2").style.height = document.getElementById("icon-btn2").offsetWidth;
        document.getElementById("icon-btn2").style.marginLeft = "20%";
        document.getElementById("icon-btn2").style.marginTop = "8%";

        button_add.style.height = String((w_height / 2)) + "px";
        let margin_px_h2 = parseInt(button_add.offsetHeight) / 5;
        button_add.style.height = String(margin_px_h2 * 3) + "px";
        button_add.style.marginTop = String(margin_px_h2) + "px";
        button_add.style.marginBottom = String(margin_px_h2) + "px";
        let margin_px_w2 = parseInt(button_add.offsetWidth-10);
        button_add.style.width = String(margin_px_h2 * 3) + "px";
        button_add.style.marginLeft = String((margin_px_w2 - button_add.offsetWidth) / 2) + "px";
        button_add.style.marginRight = String((margin_px_w2 - button_add.offsetWidth) / 2) + "px";

        document.getElementById("icon-btn3").style.width = "80%";
        document.getElementById("icon-btn3").style.height = document.getElementById("icon-btn3").offsetWidth;
        document.getElementById("icon-btn3").style.marginLeft = "20%";
        document.getElementById("icon-btn3").style.marginTop = "8%";

        button_room.style.height = String((w_height / 2)) + "px";
        let margin_px_h3 = parseInt(button_room.offsetHeight) / 5;
        button_room.style.height = String(margin_px_h3 * 3) + "px";
        button_room.style.marginTop = String(margin_px_h3) + "px";
        button_room.style.marginBottom = String(margin_px_h3) + "px";
        let margin_px_w3 = parseInt(button_room.offsetWidth-10);
        button_room.style.width = String(margin_px_h3 * 3) + "px";
        button_room.style.marginLeft = String((margin_px_w3 - button_room.offsetWidth) / 2) + "px";
        button_room.style.marginRight = String((margin_px_w3 - button_room.offsetWidth) / 2) + "px";

        document.getElementById("icon-btn4").style.width = "80%";
        document.getElementById("icon-btn4").style.height = document.getElementById("icon-btn4").offsetWidth;
        document.getElementById("icon-btn4").style.marginLeft = "20%";
        document.getElementById("icon-btn4").style.marginTop = "8%";

    }
}

window.addEventListener('load', () => {
    checkWindowSize();
    updateButtonSizes();
});

function resetButtonStyles(button) {
    button.removeAttribute("style");
    button.className = "";
}