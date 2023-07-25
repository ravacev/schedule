let obtenerFila = document.getElementById('fila0');

let elementosFila = obtenerFila.getElementsByTagName('td');

let jobData = new Array();

let action = '';

function myFunction() {
  action = 'Desea eliminar la tarea?';
}

document.querySelectorAll("input[type=image][name=delete]").forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const isButton = e.target.nodeName === 'BUTTON';
        if ((!isButton ) && (confirm(action) == true)) {
          var tr = e.target.closest('tr');

          for (var i = 0; i < (elementosFila.length - 2); i++) {
              jobData.push(tr.cells[i].innerText);
          }

          console.log(jobData);

          const request = new XMLHttpRequest();
          request.open(`POST`, `/agenda/${JSON.stringify(jobData)}`);
          request.send();
          jobData = []
          setTimeout(function(){
            location.reload();
          }, 1000);
        }
        else {
          console.log('Nuestra casilla de verificación no está marcada!');

        }
    });
});