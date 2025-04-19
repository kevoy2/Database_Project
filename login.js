document.addEventListener("DOMContentLoaded", function () {
    var loginForm = document.getElementById("login");
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      login(new FormData(e.target));
    });
    async function login(body) {
      var formObj = {};
      body.forEach((value, key) => {
        formObj[key] = value;
      });
      const response = await fetch('http://localhost:5000/login', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...formObj }),
      })
      .then(response => response.json());
      console.log(response);
      console.log(response["state"]);
      console.log(response["role"]);
      if(response["state"] == "t" && response["role"] == "Patient") {
        sessionStorage.setItem("id", formObj["id"]);
        window.location.href = "./dashboard-patient.html";
      } else if(response["state"] == "t" && response["role"] == "Doctor") {
        sessionStorage.setItem("id", formObj["id"]);
        window.location.href = "./dashboard-doctor.html";
      } else if(response["state"] == "t" && response["role"] == "Pharmacy") {
        sessionStorage.setItem("id", formObj["id"]);
        window.location.href = "./dashboard-pharma.html";
      } else {
        alert("Your login was unsuccessful. Please, try again.")
      }
    }
  });
  