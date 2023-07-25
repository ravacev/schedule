let obtener = document.getElementById('fila0');

let elementos = obtener.getElementsByTagName('td');

let jobMod = new Array();

var cuadrilla_1=new Array("-","Christian Riveros","Miguel Pintos","Claudio Ramirez", "Gustavo Caceres", "Gaspar Monges");
var cuadrilla_2=new Array("-","Cesar Pestana", "Ronald Ruiz", "Omar Ozuna", "Jorge Allende","Adolfo Allende","Juan Medina","Osvaldo Vazquez","Ricardo Prieto", "Ivan Rusconi");
var cuadrilla_3=new Array("-","Derlis Arguello", "Hugo Talavera" , "Anderson Corrales", "Rafael Urunaga", "Arnaldo Martinez","Roni Aguilera","Gabriel Lopez","Blas Gonzalez","Loemgrim Lisboa");
var cuadrilla_4=new Array("-","Ovidio Fernandez","Rodrigo Miranda");
var cuadrilla_5=new Array("-","Roberto Ayala", "Haniel Espinola")
var cuadrilla_6=new Array("-","Carlos Benitez", "Aldo Aguilera", "Victor Caceres", "Cesar Candia", "Lider Martinez", "Victor Rolon", "Mario Ramirez", "Gustavo Pereira", "Victor Benega", "Juan Galvalisi")

var select_index = new Array("", "Nucleo", "Hansa", "Hansa INT", "Bulls", "Dunkel", "Aintech");

var todascuadrilla = [
   [],
   cuadrilla_1,
   cuadrilla_2,
   cuadrilla_3,
   cuadrilla_4,
   cuadrilla_5,
   cuadrilla_6
];

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

          var income_date = tr.cells[7].textContent.toString().split('-');
          var income_date =  income_date[2] + '-' + income_date[1] + '-' + income_date[0];

          var close_date = tr.cells[17].textContent.toString().split('-');
          var close_date =  close_date[2] + '-' + close_date[1] + '-' + close_date[0];

          var schedule_date = tr.cells[21].textContent.toString().split('-');
          var schedule_date =  schedule_date[2] + '-' + schedule_date[1] + '-' + schedule_date[0];

          $('#data').toggle();

          // const request = new XMLHttpRequest();
          // request.open(`POST`, `/agenda/${JSON.stringify(jobMod)}`);
          // request.send();

          jobMod = []
          
          document.getElementById('workID').value = tr.cells[0].innerText;
          document.getElementById("id_ot2").value = tr.cells[1].innerText;
          document.getElementById("num_ticket2").value = tr.cells[2].innerText;
          document.getElementById("name_nap2").value = tr.cells[3].innerText;
          document.getElementById("issue2").value = tr.cells[4].innerText;
          document.getElementById("fase2").value = tr.cells[5].innerText;

          document.getElementById("coord2").value = tr.cells[6].innerText;
          document.getElementById("datePicker2").value = income_date;

          document.getElementById("affect_clients2").value = tr.cells[8].innerText;
          document.getElementById("dias_pen2").value = tr.cells[9].innerText;
          document.getElementById("priority2").value = tr.cells[10].innerText;

          var index_team = select_index.indexOf(tr.cells[11].innerText);

          mis_cuadrilla=todascuadrilla[index_team] 
          //calculo el numero de cuadrilla 
          num_cuadrilla = mis_cuadrilla.length 
          //marco el número de cuadrilla en el select 
          document.dataSent.cuadrilla2.length = num_cuadrilla 
          //para cada cuadrilla del array, la introduzco en el select 
          for(i=0;i<num_cuadrilla;i++){ 
             document.dataSent.cuadrilla2.options[i].value=mis_cuadrilla[i] 
             document.dataSent.cuadrilla2.options[i].text=mis_cuadrilla[i] 
          }

          document.getElementById("team2").selectedIndex = index_team;
          document.getElementById("cuadrilla2").value = tr.cells[12].innerText;

          document.getElementById("dep2").value = tr.cells[13].innerText;
          document.getElementById("zone2").value = tr.cells[14].innerText;
          document.getElementById("barrio2").value = tr.cells[15].innerText;
          document.getElementById("status2").value = tr.cells[16].innerText;

          document.getElementById("cierre2").value = close_date;
          document.getElementById("reason2").value = tr.cells[18].innerText;
          
          document.getElementById("afectacion2").value = tr.cells[19].innerText;
          document.getElementById("comentario2").value = tr.cells[20].innerText;

          document.getElementById("agendamiento2").value = schedule_date;
        }
        else {
          console.log('Nuestra casilla de verificación no está marcada!');

        }
    });
});