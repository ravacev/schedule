$('#dataHide').hide()
$('#data').hide()


document.onkeyup = function () {
  var e = e || window.event; // for IE to cover IEs window event-object
  if(e.altKey && e.which == 65) {
    $('#dataHide').toggle();
  }
}


$(function(){
    

    $('#show').click(function(){
      $('#dataHide').toggle();
      
      // document.getElementById("datePicker").disabled = true;
      document.getElementById("datePicker").value = new Date().toISOString().substring(0, 10);
    });

    $('#reset').click(function(){
      $('#dataHide').hide()
    
    });

    $('#reset2').click(function(){
      $('#data').hide();
    
    });


})