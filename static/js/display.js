$('#dataHide').hide()
$('#data').hide()

$(function(){

    

    $('#show').click(function(){
      $('#dataHide').toggle();
      
      document.getElementById("datePicker").disabled = true;
      document.getElementById("datePicker").value = new Date().toISOString().substring(0, 10);
    });

    $('#reset').click(function(){
      $('#dataHide').hide()
    
    });

    $('#reset2').click(function(){
      $('#data').hide();
    
    });


})