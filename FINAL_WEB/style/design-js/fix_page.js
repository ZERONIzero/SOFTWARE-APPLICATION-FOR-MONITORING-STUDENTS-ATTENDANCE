const date = document.getElementById('s_d').textContent;
document.getElementById('s_d').remove();
const dateObject = new Date(date);

if (!isNaN(dateObject.getTime())) {
    document.getElementById('date_select').value = dateObject.toISOString().split('T')[0];
} else {
    console.error("Некорректная дата");
}

document.getElementById('ul_2').removeAttribute('hidden');
document.getElementById('ul_2_t').removeAttribute('hidden');

const select_first = document.getElementById('list');
select_first.innerHTML = '';

let data = JSON.parse(document.getElementById('o_l').textContent);

document.getElementById('o_l').remove();

data.forEach((item,index) => {
    const new_options = document.createElement('option');
    new_options.id = String(index)+"p";
    new_options.selected = 'true';
    new_options.textContent = String(item.number_pair)+" - "+String(item.name)+" - "+String(item.group_name);
    select_first.appendChild(new_options);
});

let select_free = JSON.parse(document.getElementById('r_l').textContent);
document.getElementById('r_l').remove();


document.getElementById('list').addEventListener('change', async function(e) {
    document.getElementById('ul_3_t').removeAttribute('hidden');
    document.getElementById('ul_3').removeAttribute('hidden');
    const select_second = document.getElementById('room_list');
    select_second.innerHTML = '';
    var value = String(e.target.value).slice(0,1);
    select_free[value-1].forEach((item,index)=>{
        const new_options_two = document.createElement('option');
        new_options_two.id = String(index)+"r";
        new_options_two.value = item;
        new_options_two.textContent = String(item);
        select_second.appendChild(new_options_two);
    })

});

document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('change_button');
    
    if (submitButton) {
        submitButton.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const dateSelect = document.getElementById('date_select').value;
            const pairList = document.getElementById('list').value;

            let s_n_s = pairList.split('-');

            let name_pair = String(s_n_s[1]).substring(1).slice(0, -1);     

            const freeRooms = document.getElementById('room_list').value;
            
            if (!dateSelect || !pairList || !freeRooms) {
                alert('Пожалуйста, заполните все поля');
                return;
            }
            
            try {
                const response = await fetch('./change_audience', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        date_select: dateSelect,
                        pair_number: pairList.slice(0, 1),
                        pair_name: name_pair,
                        new_room: freeRooms
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
        console.error('Кнопка "Изменить" не найдена');
    }
});