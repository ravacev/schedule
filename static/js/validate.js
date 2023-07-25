function myValidateIn() {

    var team = document.getElementById('team').value;

    var income_date = document.getElementById("datePicker").value.split('-');
    var income_date =  income_date[0] + '-' + income_date[1] + '-' + income_date[2];

    var close_date = document.getElementById("cierre").value;
    var schedule_date = document.getElementById("agendamiento").value;

    if (team == '6' && schedule_date != '') {
        alert('OTs de Aintech sin fecha de agendamiento, favor verifique!')

        return false;
    }
    
    if ((schedule_date == '')) {
        //pass
    } else if ((schedule_date >= income_date)) {
        // pass
    } else {
        alert("Ingrese una fecha de agendamiento valida!");

        return false;
    }
    
    if ((close_date == '')) {
        //pass
    } else if ((close_date >= income_date) && (close_date == schedule_date )) {
        //pass
    } else {
        alert("Ingrese una fecha de cierre valida!");

        return false;
    }


}

function myValidateOut() {

    var team = document.getElementById('team2').value;

    var income_date = document.getElementById("datePicker2").value.split('-');
    var income_date =  income_date[0] + '-' + income_date[1] + '-' + income_date[2];

    var close_date = document.getElementById("cierre2").value;
    var schedule_date = document.getElementById("agendamiento2").value;

    console.log(schedule_date);
    console.log(income_date);
    console.log(close_date);

    if (team == '6' && schedule_date != '') {
        alert('OTs de Aintech sin fecha de agendamiento, favor verifique!');

        return false;
    }

    if ((schedule_date == '')) {
        //pass
    } else if ((schedule_date >= income_date)) {
        // pass
    } else {
        alert("Ingrese una fecha de agendamiento valida!");

        return false;
    }
    
    if ((close_date == '')) {
        //pass
    } else if ((close_date >= income_date) && (close_date == schedule_date )) {
        //pass
    } else {
        alert("Ingrese una fecha de cierre valida!");

        return false;
    }


}