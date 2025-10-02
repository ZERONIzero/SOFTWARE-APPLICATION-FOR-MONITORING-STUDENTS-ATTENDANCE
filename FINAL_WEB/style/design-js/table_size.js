let pairs=String(document.getElementById('pair_mas').textContent).split(',').map(pair => pair.trim());
let dates=String(document.getElementById('info_dates').textContent).split(',').map(date => date.trim().replace(/-/g,'.')).map(date => {
    let parts = date.split('.');
    return `${parts[2]}.${parts[1]}.${parts[0]}`;
});
let info = JSON.parse(document.getElementById('info_schedule').textContent);

window.addEventListener('resize', () => {
    checkWindowSize();
});


function checkWindowSize() {

    if (window.performance && window.performance.navigation.type === window.performance.navigation.TYPE_BACK_FORWARD) {
        window.location.href = '/menu';
    }

    window.onpopstate = function(event) {
        window.location.href = '/menu';
    };

    window.addEventListener('load', function() {
        history.pushState({ page: 'schedule' }, '', window.location.href);
    });

    window.addEventListener('beforeunload', function(e) {
        if (window.performance.navigation.type === window.performance.navigation.TYPE_BACK_FORWARD) {
            window.location.href = '/menu';
        }
    });

    if (window.innerWidth < 1250) {
        removeScreen();
        createROW();
        let tables = document.getElementsByTagName('table');
        Array.from(tables).forEach((table) => {
            // table.style.backgroundColor = '#353535';
            table.style.border = '2px solid #404040';
            table.style.borderRadius = "20px";
        });
    } else {
        removeScreen();
        createCOL();
        let tables = document.getElementsByTagName('table');
        Array.from(tables).forEach((table) => {
            // table.style.backgroundColor = '#353535';
            table.style.border = '2px solid #404040';
            table.style.borderRadius = "20px";
        });
    }
    setTableHeight();
    
    const tableDate = dates[0].split('.');
    const formattedDate = `${tableDate[2]}-${tableDate[1]}-${tableDate[0]}`;
    document.getElementById('week_date_select').value = formattedDate;
    
    const dateObj = new Date(tableDate[2], tableDate[1] - 1, tableDate[0]);
    const firstDayOfYear = new Date(dateObj.getFullYear(), 0, 1);
    const pastDays = (dateObj - firstDayOfYear) / 86400000;
    let currentWeek = Math.ceil((pastDays + firstDayOfYear.getDay() + 1) / 7);
    currentWeek = currentWeek < 10 ? '0' + currentWeek : currentWeek;
    const weekStr = dateObj.getFullYear() + '-W' + currentWeek;
    document.getElementById('weekPicker').value = weekStr;

}

function removeScreen(){
    let body_table = document.getElementById("body_tb");
    body_table.innerHTML = '';
}

function createCOL() {
    let body_table = document.getElementById("body_tb");
    body_table.classList.add('row-cols-3');
    let days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];

    days.forEach((day, index) => {
        body_table.innerHTML += `
            <div class="col-md-4">
                <table class="table table-bordered table-hover">
                    <caption align="top" id=${index}>${day} ${dates[index]}</caption>
                    <thead>
                        <tr>
                            <th scope="col">Время</th>
                            <th scope="col">Предмет</th>
                            <th scope="col">Аудитория</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr id="${index}-1">
                            <td>${pairs[0]}</td>
                        </tr>
                        <tr id="${index}-2">
                            <td>${pairs[1]}</td>
                        </tr>
                        <tr id="${index}-3">
                            <td>${pairs[2]}</td>
                        </tr>
                        <tr id="${index}-4">
                            <td>${pairs[3]}</td>
                        </tr>
                        <tr id="${index}-5">
                            <td>${pairs[4]}</td>
                        </tr>
                        <tr id="${index}-6">
                            <td>${pairs[5]}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    });

    for (let m=0; m < info[0].length ;m++){
        info[m].forEach((item,index)=>{
            let cellName = document.createElement('td');
            cellName.textContent = item.name;
            document.getElementById(`${m}-${index + 1}`).appendChild(cellName);

            let cellRoom = document.createElement('td');
            let linkmodal = document.createElement('a');
            linkmodal.textContent = item.room;
            linkmodal.href = '#';
            linkmodal.setAttribute('data-bs-toggle','modal');
            linkmodal.setAttribute('data-bs-target', `#modal-list_stud_${m}-${index + 1}`);
            linkmodal.style.textDecoration = 'none';
            linkmodal.style.color = 'inherit';
            cellRoom.appendChild(linkmodal);
            document.getElementById(`${m}-${index + 1}`).appendChild(cellRoom);

            let modalHtml = 
            `<div class="modal fade modal-lg" id="modal-list_stud_${m}-${index + 1}" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${item.name}<br> В ${item.room} аудитории</h5>
                        </div>
                        <div class="modal-body">
                            <div class="justify-content-center" style="width: 100%;">
                                ${item.stud_list ? 
                                    `<table class="table table-bordered">
                                        <tbody>
                                            ${item.stud_list.split(',')
                                                .reduce((rows, student, index) => {
                                                    if (index % 2 === 0) {
                                                        rows.push([student.trim()]);
                                                    } else {
                                                        rows[rows.length - 1].push(student.trim());
                                                    }
                                                    return rows;
                                                }, [])
                                                .map(row => `
                                                    <tr>
                                                        <td class="text-sm-start" style="width: 50%">${row[0]}</td>
                                                        <td class="text-sm-start" style="width: 50%">${row[1] || ''}</td>
                                                    </tr>
                                                `).join('')
                                            }
                                        </tbody>
                                    </table>` 
                                    : 'Список студентов пуст'
                                }
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button class="btn btn-secondary" data-bs-dismiss="modal" type="button">Закрыть</button>
                        </div>
                    </div>
                </div>
            </div>`;
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);

        })
    }

    if (document.getElementById('info_schedule')) {
        document.getElementById('info_schedule').remove();
    }

    Array.from(document.getElementsByTagName('td')).forEach((td)=>{
        td.style.paddingLeft='2px';
        td.style.paddingRight='2px';
        td.style.paddingTop='4px';
        td.style.paddingBottom='4px';
        td.style.fontSize = '10px';
    });

    Array.from(document.getElementsByTagName('th')).forEach((th)=>{
        th.style.paddingLeft='2px';
        th.style.paddingRight='2px';
        th.style.paddingTop='4px';
        th.style.paddingBottom='4px';
        th.style.fontSize = '10px';
    });

    if (document.getElementById('pair_mas')) {
        document.getElementById('pair_mas').remove();
    }

    if (document.getElementById('info_dates')) {
        document.getElementById('info_dates').remove();
    }
}

function createROW() {
    let body_table = document.getElementById("body_tb");
    body_table.className = body_table.className.replace('row-cols-3', '');
    
    let days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];

    days.forEach((day, index) => {
        body_table.innerHTML += `
            <div>
                <table class="table table-bordered table-hover col">
                    <caption align="top" id=${index} >${day} ${dates[index]}</caption>
                    <thead>
                        <tr>
                            <th scope="col">Время</th>
                            <th scope="col">Предмет</th>
                            <th scope="col">Аудитория</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr id="${index}-1">
                            <td>${pairs[0]}</td>
                        </tr>
                        <tr id="${index}-2">
                            <td>${pairs[1]}</td>
                        </tr>
                        <tr id="${index}-3">
                            <td>${pairs[2]}</td>
                        </tr>
                        <tr id="${index}-4">
                            <td>${pairs[3]}</td>
                        </tr>
                        <tr id="${index}-5">
                            <td>${pairs[4]}</td>
                        </tr>
                        <tr id="${index}-6">
                            <td>${pairs[5]}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    });

    for (let m=0; m < info[0].length ;m++){
        info[m].forEach((item,index)=>{
            let cellName = document.createElement('td');
            cellName.textContent = item.name;
            document.getElementById(`${m}-${index + 1}`).appendChild(cellName);

            let cellRoom = document.createElement('td');
            let linkmodal = document.createElement('a');
            linkmodal.textContent = item.room;
            linkmodal.href = '#';
            linkmodal.setAttribute('data-bs-toggle','modal');
            linkmodal.setAttribute('data-bs-target', `#modal-list_stud_${m}-${index + 1}`);
            linkmodal.style.textDecoration = 'none';
            linkmodal.style.color = 'inherit';
            cellRoom.appendChild(linkmodal);
            document.getElementById(`${m}-${index + 1}`).appendChild(cellRoom);

            let modalHtml = 
            `<div class="modal fade modal-lg" id="modal-list_stud_${m}-${index + 1}" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${item.name}<br> В ${item.room} аудитории</h5>
                        </div>
                        <div class="modal-body">
                            <div class="justify-content-center" style="width: 100%;">
                                ${item.stud_list ? 
                                    `<table class="table table-bordered">
                                        <tbody>
                                            ${item.stud_list.split(',')
                                                .reduce((rows, student, index) => {
                                                    if (index % 2 === 0) {
                                                        rows.push([student.trim()]);
                                                    } else {
                                                        rows[rows.length - 1].push(student.trim());
                                                    }
                                                    return rows;
                                                }, [])
                                                .map(row => `
                                                    <tr>
                                                        <td class="text-sm-start" style="width: 50%">${row[0]}</td>
                                                        <td class="text-sm-start" style="width: 50%">${row[1] || ''}</td>
                                                    </tr>
                                                `).join('')
                                            }
                                        </tbody>
                                    </table>` 
                                    : 'Список студентов пуст'
                                }
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button class="btn btn-secondary" data-bs-dismiss="modal" type="button">Закрыть</button>
                        </div>
                    </div>
                </div>
            </div>`;
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);
        })
    }


    if (document.getElementById('info_schedule')) {
        document.getElementById('info_schedule').remove();
    }

    Array.from(document.getElementsByTagName('td')).forEach((td)=>{
        td.style.paddingLeft='2px';
        td.style.paddingRight='2px';
        td.style.fontSize = '10px';
    });

    Array.from(document.getElementsByTagName('th')).forEach((th)=>{
        th.style.paddingLeft='2px';
        th.style.paddingRight='2px';
        th.style.fontSize = '10px';
    });

    if (document.getElementById('pair_mas')) {
        document.getElementById('pair_mas').remove();
    }

    if (document.getElementById('info_dates')) {
        document.getElementById('info_dates').remove();
    }
}

function setTableHeight() {
    let tables = document.querySelectorAll('#body_tb table');
    if (tables.length > 0) {
        let firstTableHeight = tables[0].offsetHeight;
        tables.forEach((table) => {
            table.style.height = `${firstTableHeight}px`;
        });
    }
    
    if (tables.length > 0) {
        let firstTd = tables[0].querySelector('td');
        let firstTdHeight = firstTd.offsetHeight;
        let firstTdWidth = firstTd.offsetWidth;

        tables.forEach((table) => {
            let tds = table.querySelectorAll('td');
            tds.forEach((td, index) => {
                if ((index + 1) % 3 === 0) {
                    td.style.height = `${firstTdHeight}px`;
                    td.style.width = `${firstTdWidth}px`;
                }
            });
        });
    }
}