document.addEventListener("DOMContentLoaded", function () {
    var addForm = document.getElementById("add");
    var medForm = document.getElementById("perscribe");
    var viewForm = document.getElementById("patient");
    var logoutButton = document.getElementById("logout");
    addForm.addEventListener("submit", (e) => {
      e.preventDefault();
      add(new FormData(e.target));
    });
    medForm.addEventListener("submit", (e) => {
      e.preventDefault();
      perscribe(new FormData(e.target));
    });
    viewForm.addEventListener("submit", (e) => {
      e.preventDefault();
      view(new FormData(e.target));
    });
    logoutButton.addEventListener("click", (e) => {
      e.preventDefault(); 
      sessionStorage.removeItem('id');
      window.location.href = "./index.html";
    });
    async function add(body) {
      var formObj = {};
      body.forEach((value, key) => {
        formObj[key] = value;
      });
      const response = await fetch("http://localhost:5000/add-patient", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...formObj, id: sessionStorage.getItem("id") }),
      })
      .then(response => response.json());
      console.log(response["message"]);
      if(response["message"] === "Doctor added the patient successfully") {
        alert("Doctor added the patient successfully.")
      } else if (response["message"] === "The patient already has a doctor") {
        alert("The patient already has a doctor.");
      } else if (response["message"] === "You already added this patient") {
        alert("You already added this patient.");
      } else {
        alert("That patient is not stored in our database.")
      }
    }
    async function perscribe(body) {
      var formObj = {};
      body.forEach((value, key) => {
        formObj[key] = value;
      });
      const response = await fetch("http://localhost:5000/perscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...formObj, id: sessionStorage.getItem("id") }),
      })
      .then(response => response.json());
      console.log(response["message"]);
      if (response["message"] === "The patient do not exist.") {
        alert("The patient is not in the database.");
      } else if (response["message"] === "Drug interaction too severe.") {
        alert("Use \"override\": true to force the assignment.");
      } else {
        alert("Success");
      }
    }
    async function view(body) {
      var formObj = {};
      body.forEach((value, key) => {
        formObj[key] = value;
      });
      const response = await fetch("http://localhost:5000/view-patient", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...formObj, id: sessionStorage.getItem("id") }),
      })
      .then(response => response.json());
      console.log(response["message"]);
      if(response["message"] === "Patient data received successfully") {
        let codeList = "<ul>";
        let medsList = "<ul>";
        for(const x of response["meds"]) {
          medsList += "<il><span>" + x + "</span></il>";
        }
        for(const y of response["codes"]) {
          codeList += "<il><span>" + y + "</span></il>";
        }
        codeList += "</ul>";
        medsList += "</ul>";
        var tb = document.getElementById("record");
        tb.innerHTML="<tr><th>SSN</th><th>Name</th><th>Gender</th><th>Phone #</th><th>Condition Code(s)</th><th>Perscription(s)</th></tr><tr><td>" + response["ssn"] + "</td><td>" + response["name"] + "</td><td>" + response["gender"] + "</td><td>" + response["phone"] + "</td><td>" + codeList + "</td><td>" + medsList + "</td></tr>";
        alert("That patient's information was successfully retieved.")
      } else if (response["message"] === "Patient is not assigned to you") {
        alert("That patient is not assigned to you.");
      } else {
        alert("That patient is not stored in our database.")
      }
    }
});
  