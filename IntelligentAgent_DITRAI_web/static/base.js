document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const successAlert = document.querySelector('#success-alert');

    form.addEventListener('submit', function(event) {
      event.preventDefault();
      // Envía el formulario mediante AJAX
      fetch(event.target.action, {
        method: event.target.method,
        body: new FormData(event.target)
      }).then(function(response) {
        if (response.ok) {
          // Muestra el mensaje de éxito y limpia el formulario
          successAlert.classList.remove('d-none');
          form.reset();
        } else {
          console.error('Error al enviar el formulario');
        }
      });
    });
  });