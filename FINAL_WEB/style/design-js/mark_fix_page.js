const select_first = document.getElementById('list');
select_first.innerHTML = '';

let group = JSON.parse(document.getElementById('g_l').textContent);
document.getElementById('g_l').remove();

group.forEach((item,index) => {
    const new_options = document.createElement('option');
    new_options.id = String(index)+"p";
    new_options.selected = 'true';
    new_options.value = String(item.name);
    new_options.textContent = String(item.name);
    select_first.appendChild(new_options);
});

function set_time(){

    const dates = document.getElementById('s_d');
    if (dates) {
        let date = document.getElementById('s_d').textContent;
        document.getElementById('s_d').remove();
        const dateObject = new Date(date);

        if (!isNaN(dateObject.getTime())) {
            document.getElementById('date_select').value = dateObject.toISOString().split('T')[0];
        } else {
            console.error("Некорректная дата");
        }

        const valueToSelect = String(document.getElementById('g_n').textContent);
        document.getElementById('g_n').remove();
        const options = select_first.options;

        for (let i = 0; i < options.length; i++) {
            if (options[i].value === valueToSelect) {
                options[i].selected = true;
                break;
            }
        }

        document.getElementById('ul_3').removeAttribute('hidden');
        document.getElementById('ul_3_t').removeAttribute('hidden');

        const select_second = document.getElementById('list_two');
        select_second.innerHTML = '';

        let subject_list = JSON.parse(document.getElementById('o_sh').textContent);
        document.getElementById('o_sh').remove();

        subject_list.forEach((item,index) => {
            const new_options = document.createElement('option');
            new_options.id = String(index)+"p";
            new_options.selected = 'true';
            new_options.textContent = String(item.number_pair)+" - "+String(item.name);
            select_second.appendChild(new_options);
        });
    }
}

document.getElementById('list_two').addEventListener('change', async function(e) {
    document.getElementById('ul_4_t').removeAttribute('hidden');
    document.getElementById('ul_4').removeAttribute('hidden');

    let stud_list = JSON.parse(document.getElementById('o_sg').textContent);
    document.getElementById('o_sg').remove();

    const select_third = document.getElementById('list_three');
    select_third.innerHTML = '';

    stud_list.forEach((item,index) => {
        const new_options = document.createElement('option');
        new_options.id = String(index)+"p";
        new_options.selected = 'true';
        new_options.textContent = String(item.student);
        select_third.appendChild(new_options);
    });

});

let third = document.getElementById('list_three');
if (third){
    document.getElementById('list_three').addEventListener('change', async function(e) {
        document.getElementById('ul_5').removeAttribute('hidden');
    });
}
document.addEventListener('DOMContentLoaded', function() {
    set_time();

    const submitButton = document.getElementById('change_button');
    
    if (submitButton) {
        submitButton.addEventListener('click', async function(e) {
            e.preventDefault();

            const dateSelect = document.getElementById('date_select').value;
            const groupList = document.getElementById('list').value;
            const pairList = document.getElementById('list_two').value;
            const studentList = document.getElementById('list_three').value;

            let s_n_s = pairList.split('-');
            let name_pair = String(s_n_s[1]).substring(1);
            let numberpair = String(s_n_s[0].slice(0,-1));

            if (!dateSelect || !groupList || !pairList || !studentList){
                alert('Пожалуйста, заполните все поля');
                return;
            }

            try{
                const response = await fetch('./mark_a_student', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        date_select: dateSelect,
                        group_select: groupList,
                        pair_name: name_pair,
                        student_name: studentList,
                        number_pair: numberpair
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('Ошибка от сервера:', errorData);
                    throw new Error(errorData.message || 'Network response was not ok');
                }

                const html = await response.text();
                
                document.documentElement.innerHTML = html;
                
                const scripts = document.getElementsByTagName('script');
                for (let script of scripts) {
                    if (script.src) {
                        const newScript = document.createElement('script');
                        newScript.src = script.src;
                        script.parentNode.replaceChild(newScript, script);
                    }
                }

            } catch (error) {
                console.error('Error:', error);
            } 
        });
    } else {
        console.error('Кнопка "Отметить" не найдена');
    }
});