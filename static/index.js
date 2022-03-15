document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#edit').onclick = () => edit_post();
});

function edit_post() {
  document.querySelector('h5').value = 'Bye!';

}
