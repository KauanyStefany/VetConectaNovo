document.addEventListener('DOMContentLoaded', function () {
  const tutorRadio = document.getElementById('tutor');
  const veterinarioRadio = document.getElementById('veterinario');
  const crmvField = document.getElementById('crmv-field');

  function toggleCrmvField() {
    if (veterinarioRadio.checked) {
      crmvField.style.display = 'block';
      document.getElementById('crmv').setAttribute('required', 'required');
    } else {
      crmvField.style.display = 'none';
      document.getElementById('crmv').removeAttribute('required');
    }
  }

  tutorRadio.addEventListener('change', toggleCrmvField);
  veterinarioRadio.addEventListener('change', toggleCrmvField);

  // Inicializa o campo corretamente ao carregar a página
  toggleCrmvField();
});