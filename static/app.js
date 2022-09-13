qForm = document.getElementById("qForm");
radios = document.getElementsByClassName("radios");

if (qForm) {
  qForm.addEventListener("submit", (e) => {
    e.preventDefault();
    for (let i = 0; i < radios.length; i++) {
      if ((radios[i].checked === true)) {
        qForm.submit();
        return
      }
    }
    alert("Please select an option");
  });
}
