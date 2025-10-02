let count = 0;
let direction = 1;
let colors = ["#f94144",
            "#f3722c",
            "#f8961e",
            "#f9844a",
            "#f9c74f",
            "#90be6d",
            "#43aa8b",
            "#4d908e",
            "#577590",
            "#277da1"];

function set_color_for_one(){
    return colors[count];
}


function swap_color_all_li(){
    let circles = document.querySelectorAll('.circles li');
    circles.forEach ( circle => {
        circle.style.transition = 'background-color 10s'; 
        circle.style.backgroundColor = set_color_for_one();
        count+=direction;
    });

    if (count >= colors.length) {
        direction = -1;
        count = colors.length - 1;
    } else if (count < 0) {
        direction = 1;
        count = 0;
    }
}

setInterval(swap_color_all_li,20000);