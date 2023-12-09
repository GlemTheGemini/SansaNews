document.getElementById('actualizarFechaBtn').addEventListener('click', function() {
    var fechaActual = new Date();
    var year = fechaActual.getFullYear();
    var month = fechaActual.getMonth() + 1;
    var day = fechaActual.getDate();
    var hours = fechaActual.getHours();
    var minutes = fechaActual.getMinutes();
    var seconds = fechaActual.getSeconds();

    var monthString = month < 10 ? '0' + month : String(month);
    var dayString = day < 10 ? '0' + day : String(day);
    var hoursString = hours < 10 ? '0' + hours : String(hours);
    var minutesString = minutes < 10 ? '0' + minutes : String(minutes);
    var secondsString = seconds < 10 ? '0' + seconds : String(seconds);

    var fechaFormateada = year + '-' + monthString + '-' + dayString + '_' + hoursString + '-' + minutesString + '-' + secondsString;

    localStorage.setItem('fechaIngreso', fechaFormateada);
    alert("Fecha actualizada")
});