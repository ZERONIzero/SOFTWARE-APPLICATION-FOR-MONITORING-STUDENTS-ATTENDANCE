let selectedDate;

function getWeekDates(monday) {
    const dates = [];
    for(let i = 0; i < 7; i++) {
        const date = new Date(monday);
        date.setDate(monday.getDate() + i);
        dates.push(date.toISOString().split('T')[0]);
    }
    return dates;
}

function nextWeek() {
    let currentDate = new Date(document.getElementById('week_date_select').value);
    currentDate.setDate(currentDate.getDate() + 7);
    document.getElementById('week_date_select').value = currentDate.toISOString().split('T')[0];
    document.getElementById('weekForm').submit();
}

function backWeek() {
    let currentDate = new Date(document.getElementById('week_date_select').value);
    currentDate.setDate(currentDate.getDate() - 7);
    document.getElementById('week_date_select').value = currentDate.toISOString().split('T')[0];
    document.getElementById('weekForm').submit();
}

function handleWeekChange(weekValue) {
    const [year, week] = weekValue.split('-W');
    const monday = getFirstDayOfWeek(year, week);
    const weekDates = getWeekDates(monday);
    selectedDate = weekDates[1];
    document.getElementById("week_date_select").value = selectedDate;
}

function getFirstDayOfWeek(year, week) {
    const firstDayOfYear = new Date(year, 0, 0);
    const dayOffset = (week - 1) * 7;
    firstDayOfYear.setDate(firstDayOfYear.getDate() + dayOffset);
    const dayOfWeek = firstDayOfYear.getDay();    
    const monday = new Date(firstDayOfYear);
    if (dayOfWeek == 0) {
        monday.setDate(firstDayOfYear.getDate() + 1);
    } else if (dayOfWeek > 1) {
        monday.setDate(firstDayOfYear.getDate() - 1);
    }
    
    return monday;
}
