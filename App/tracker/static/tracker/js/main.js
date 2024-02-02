const dateInput = document.getElementById('dateInput');
dateInput.addEventListener('change', (event) => {
  const selectedDate = event.target.value;
  document.getElementById(
    'display'
  ).innerHTML = `Selected date: ${selectedDate}`;
});
