var cuadrilla_1=new Array("-","Christian Riveros","Miguel Pintos","Claudio Ramirez", "Gustavo Caceres", "Gaspar Monges");
var cuadrilla_2=new Array("-","Cesar Pestana", "Ronald Ruiz", "Omar Ozuna", "Jorge Allende","Adolfo Allende","Juan Medina","Osvaldo Vazquez","Ricardo Prieto", "Ivan Rusconi");
var cuadrilla_3=new Array("-","Derlis Arguello", "Hugo Talavera" , "Anderson Corrales", "Rafael Urunaga", "Arnaldo Martinez","Roni Aguilera","Gabriel Lopez","Blas Gonzalez","Loemgrim Lisboa");
var cuadrilla_4=new Array("-","Ovidio Fernandez","Rodrigo Miranda");
var cuadrilla_5=new Array("-","Roberto Ayala", "Haniel Espinola")
var cuadrilla_6=new Array("-","Carlos Benitez", "Aldo Aguilera", "Victor Caceres", "Cesar Candia", "Lider Martinez", "Victor Rolon", "Mario Ramirez", "Gustavo Pereira", "Victor Benega", "Juan Galvalisi")

var todascuadrilla = [
   [],
   cuadrilla_1,
   cuadrilla_2,
   cuadrilla_3,
   cuadrilla_4,
   cuadrilla_5,
   cuadrilla_6
];

function cambia_cuadrilla(){ 
   //tomo el valor del select del team elegido 
   var team 
   team = document.sentData.team[document.sentData.team.selectedIndex].value 
   //miro a ver si el team está definido 
   if (team != 0) { 
      //si estaba definido, entonces coloco las opciones de la cuadrilla correspondiente. 
      //selecciono el array de cuadrilla adecuado 
      mis_cuadrilla=todascuadrilla[team] 
      //calculo el numero de cuadrilla 
      num_cuadrilla = mis_cuadrilla.length 
      //marco el número de cuadrilla en el select 
      document.sentData.cuadrilla.length = num_cuadrilla 
      //para cada cuadrilla del array, la introduzco en el select 
      for(i=0;i<num_cuadrilla;i++){ 
         document.sentData.cuadrilla.options[i].value=mis_cuadrilla[i] 
         document.sentData.cuadrilla.options[i].text=mis_cuadrilla[i] 
      }	
   }else{ 
      //si no había cuadrilla seleccionada, elimino las cuadrilla del select 
      document.sentData.cuadrilla.length = 1 
      //coloco un guión en la única opción que he dejado 
      document.sentData.cuadrilla.options[0].value = "-" 
      document.sentData.cuadrilla.options[0].text = "-" 
   } 
   //marco como seleccionada la opción primera de cuadrilla 
   document.sentData.cuadrilla.options[0].selected = true 
} 

function cambia_team(){ 
   //tomo el valor del select del team elegido 
   var team2
   team2 = document.dataSent.team2[document.dataSent.team2.selectedIndex].value 
   //miro a ver si el team está definido 
   if (team2 != 0) { 
      //si estaba definido, entonces coloco las opciones de la cuadrilla correspondiente. 
      //selecciono el array de cuadrilla adecuado 
      mis_cuadrilla=todascuadrilla[team2] 
      //calculo el numero de cuadrilla 
      num_cuadrilla = mis_cuadrilla.length 
      //marco el número de cuadrilla en el select 
      document.dataSent.cuadrilla2.length = num_cuadrilla 
      //para cada cuadrilla del array, la introduzco en el select 
      for(i=0;i<num_cuadrilla;i++){ 
         document.dataSent.cuadrilla2.options[i].value=mis_cuadrilla[i] 
         document.dataSent.cuadrilla2.options[i].text=mis_cuadrilla[i] 
      }	
   }else{ 
      //si no había cuadrilla seleccionada, elimino las cuadrilla del select 
      document.dataSent.cuadrilla2.length = 1 
      //coloco un guión en la única opción que he dejado 
      document.dataSent.cuadrilla2.options[0].value = "-" 
      document.dataSent.cuadrilla2.options[0].text = "-" 
   } 
   //marco como seleccionada la opción primera de cuadrilla 
   document.dataSent.cuadrilla2.options[0].selected = true 
}  