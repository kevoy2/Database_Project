document.addEventListener("DOMContentLoaded", function () {
    var loginForm = document.getElementById("login");
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      login(new FormData(e.target));
    });
    function login(body) {
      send(body);
      if(body.get("roles") == "Doctor") {
        console.log("Doctor");
        window.location.href = "./dashboard-doctor.html";
      } else if (body.get("roles") == "Patient") {
        console.log("Patient");
        window.location.href = "./dashboard-patient.html";
      } else {
        console.log("Pharmacy");
        window.location.href = "./dashboard-pharma.html";
      }
    }
    async function send(formData) {
      var formObj = {};
      formData.forEach((value, key) => {
        formObj[key] = value;
      });
      await fetch('http://localhost:5000/login', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...formObj }),
      })
      .then(response => response.text())
      .then(data => console.log(data));
    }
  });
  