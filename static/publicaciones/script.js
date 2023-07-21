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

    // Obtener el token CSRF desde la cookie
    var csrftoken = getCookie('csrftoken');

    // Realizar la solicitud POST al backend utilizando Ajax
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/actualizar_fecha/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken); // Agregar el token CSRF al encabezado
    xhr.send(JSON.stringify({ fechaFormateada: fechaFormateada }));
    xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
        // La solicitud fue exitosa, mostrar la respuesta del servidor
        var respuestaServidor = document.getElementById('respuestaServidor');
        respuestaServidor.textContent = 'Respuesta del servidor: ' + xhr.responseText;
        } else {
        // Ocurrió un error en la solicitud
        alert('Error al procesar la fecha de ingreso en el backend.');
        }
    }
    };
});

// Función para obtener el valor del token CSRF desde la cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
        }
    }
    }
    return cookieValue;
}