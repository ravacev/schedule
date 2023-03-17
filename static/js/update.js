let obtener = document.getElementById('fila0');

let elementos = obtener.getElementsByTagName('td');

let jobMod = new Array();



document.querySelectorAll("input[type=image][name=update]").forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const isButton = e.target.nodeName === 'BUTTON';
        if (!isButton) {
          var tr = e.target.closest('tr');

          for (var i = 0; i < (elementos.length - 2); i++) {
              jobMod.push(tr.cells[i].innerText);
          }

          console.log(jobMod);

          const request = new XMLHttpRequest

          request.open(`POST`, `/agenda/${JSON.stringify(jobMod)}`);
          request.send();

          

          $('#data').toggle();

          

          document.getElementById("id_ot2").value = tr.cells[0].innerText;
          document.getElementById("num_ticket2").value = tr.cells[1].innerText;
          document.getElementById("name_nap2").value = tr.cells[2].innerText;
          document.getElementById("issue2").value = tr.cells[3].innerText;

          document.getElementById("coord2").value = tr.cells[5].innerText;

          document.getElementById("affect_clients2").value = tr.cells[7].innerText;
          document.getElementById("dias_pen2").value = tr.cells[8].innerText;

          document.getElementById("team2").value = tr.cells[10].innerText;
          document.getElementById("cuadrilla2").value = tr.cells[11].innerText;
          document.getElementById("dep2").value = tr.cells[12].innerText;
          document.getElementById("zone2").value = tr.cells[13].innerText;
          document.getElementById("barrio2").value = tr.cells[14].innerText;

          document.getElementById("fecha2").value = tr.cells[16].innerText;
          
          document.getElementById("afectacion2").value = tr.cells[18].innerText;

          jobMod = []

      
        }
        else {
          console.log('Nuestra casilla de verificación no está marcada!');

        }
    });
});