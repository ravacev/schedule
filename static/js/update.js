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

          // const request = new XMLHttpRequest();

          // request.open(`POST`, `/agenda/${JSON.stringify(jobMod)}`);
          // request.send(jobMod);

          $('#data').toggle();
          jobMod = []

          document.getElementById("id_ot").value = tr.cells[0].innerText;
          document.getElementById("num_ticket").value = tr.cells[1].innerText;
          document.getElementById("name_nap").value = tr.cells[2].innerText;
          document.getElementById("issue").value = tr.cells[3].innerText;
          document.getElementById("phase").value = tr.cells[4].innerText;

          document.getElementById("coord").value = tr.cells[5].innerText;
          document.getElementById("dateDemand").value = tr.cells[6].innerText;
          document.getElementById("affect_clients").value = tr.cells[7].innerText;
          document.getElementById("dias_pen").value = tr.cells[8].innerText;
          document.getElementById("priority").value = tr.cells[9].innerText;

          document.getElementById("team").value = tr.cells[10].innerText;
          document.getElementById("cuadrilla").value = tr.cells[11].innerText;
          document.getElementById("dep").value = tr.cells[12].innerText;
          document.getElementById("zona").value = tr.cells[13].innerText;
          document.getElementById("barrio").value = tr.cells[14].innerText;
          document.getElementById("status").value = tr.cells[15].innerText;

          document.getElementById("dateDone").value = tr.cells[16].innerText;
          document.getElementById("reason").value = tr.cells[17].innerText;
          
          document.getElementById("downUsers").value = tr.cells[18].innerText;
        }
        else {
          console.log('Nuestra casilla de verificación no está marcada!');

        }
    });
});