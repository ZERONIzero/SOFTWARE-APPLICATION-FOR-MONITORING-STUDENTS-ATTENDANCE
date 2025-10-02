// function Test_field(){
//     let pass = document.getElementById("pass");
//     let r_pass = document.getElementById("r_pass");

//     if (pass.value.trim() === ''){
//         alert("Пожалуйста, заполните поле email");
//         return;
//     }

//     if (r_pass.value.trim() === ''){
//         alert("Пожалуйста, заполните поле old password");
//         return;
//     }

//     let data = {
//         pass : pass.value,
//         r_pass : r_pass.value
//     };

//     fetch('/student/setting',{
//         method: 'POST',
//         headers : {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)
//     })
// }

// window.onload = function() {
//     let btn = document.getElementById("btn_reset");
//     btn.addEventListener("submit",function(e){
//         e.preventDefault();
//         Test_field()
//     });
// }