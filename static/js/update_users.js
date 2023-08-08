let obtener = document.getElementById('fila0');

let elementos = obtener.getElementsByTagName('td');

let keys = ["UsersID", "username", "email", "admin"]; 

let user = new Array();

document.querySelectorAll("input[type=image][name=update]").forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const isButton = e.target.nodeName === 'BUTTON';
        if (!isButton) {
          var tr = e.target.closest('tr');

          for (var i = 0; i < (elementos.length - 2); i++) {
              user.push(tr.cells[i].innerText);
          }

          console.log(user);

          $('#data').toggle();


          for (let index = 0; index < user.length; index++) {
            document.getElementById(keys[index]).value = tr.cells[index].innerText;
          }

          user = []
        }
        else {
          console.log('Nuestra casilla de verificación no está marcada!');

        }
    });
});