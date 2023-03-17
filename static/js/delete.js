let obtenerFila = document.getElementById('fila0');

let elementosFila = obtenerFila.getElementsByTagName('td');

let jobData = new Array();

document.querySelectorAll("input[type=image][name=delete]").forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const isButton = e.target.nodeName === 'BUTTON';
        if (!isButton) {
          var tr = e.target.closest('tr');

          for (var i = 0; i < (elementosFila.length - 2); i++) {
              jobData.push(tr.cells[i].innerText);
          }

          console.log(jobData);

          const request = new XMLHttpRequest

          request.open(`POST`, `/agenda/${JSON.stringify(jobData)}`);
          request.send();

          jobData = []
          
      
        }
        else {
          console.log('Nuestra casilla de verificación no está marcada!');

        }
    });
});