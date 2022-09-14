qForm = document.getElementById("qForm");
radios = document.getElementsByClassName("radios");
surveyForm = document.getElementById("surveyForm")
surveySelect = document.getElementById("surveySelect")

if (qForm) {
  qForm.addEventListener("submit", (e) => {
    e.preventDefault();
    for (let i = 0; i < radios.length; i++) {
      if ((radios[i].checked === true)) {
        console.log(radios[i].value)
        qForm.submit();
        return
      }
    }
    alert("Please select an option");
  });
}

if(surveyForm) {
  surveyForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (surveySelect.value === ""){
      return
    } else {
      surveyForm.submit()
    }
  })
}
