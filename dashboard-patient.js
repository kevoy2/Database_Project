document.addEventListener("DOMContentLoaded", function () {
    var docView = document.getElementById("doc");
    var medView = document.getElementById("med");
    var stockView = document.getElementById("view");
    var logoutButton = document.getElementById("logout");
    docView.addEventListener("click", (e) => {
      e.preventDefault(); 
      viewDoc();
    });
    medView.addEventListener("click", (e) => {
      e.preventDefault(); 
      viewMed();
    });
    stockView.addEventListener("submit", (e) => {
      e.preventDefault(); 
      viewStock(new FormData(e.target));
    });
    logoutButton.addEventListener("click", (e) => {
      e.preventDefault(); 
      sessionStorage.removeItem('id');
      window.location.href = "./index.html";
    });
    async function viewDoc() {
      const response = await fetch("http://localhost:5000/view-doctor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: sessionStorage.getItem("id") }),
      })
      .then(response => response.json());
      var tb = document.getElementById("portfolio");
      if (response["message"] === "Doctor data received successfully"){
        tb.innerHTML="<tr><th>Doctor ID</th><th>Name</th><th>Type</th><th>Phone #</th></tr><tr><td>" + response["id"] + "</td><td>" + response["name"] + "</td><td>" + response["type"] + "</td><td>" + response["phone"] + "</td></tr>";
      } else {
        tb.innerHTML="<h3 style=\"color:red\">YOUR DOCTOR IS NOT ASSIGNED</h3>";
      }
    }
    async function viewMed() {
      const response = await fetch("http://localhost:5000/view-perscription", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: sessionStorage.getItem("id") }),
      })
      .then(response => response.json());
      var tb = document.getElementById("record");
      if (response["message"] === "Drug data retrieved successfully"){
        let rows = "";
        for (let i = 0; i < response["resp"].length; i++) {
          rows += "<tr><td>" + response["resp"][i][0] + "</td><td>" + response["resp"][i][1] + "</td><td>" + response["resp"][i][2] + "</td><td>" + response["resp"][i][3] + "</td>";
        }
        tb.innerHTML="<tr><th>Drug ID</th><th>Generic Name</th><th>DEA Schedule</th><th>Common Uses</th></tr><tr>" + rows + "</tr>";
      } else {
        tb.innerHTML="<h3 style=\"color:red\">YOU HAVE NO PERSCRIPTIONS</h3>";
      }
    }
    async function viewStock(body) {
      var formObj = {};
      body.forEach((value, key) => {
        formObj[key] = value;
      });
      const response = await fetch("http://localhost:5000/view-stock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...formObj }),
      })
      .then(response => response.json());
      console.log(response["message"]);
      const chart = document.getElementById("chart");
      const details = {
        type: "bar",
        data: {
          labels: response["x"],
          datasets: [{
              label: "Drug(s)",
              data: response["y"],
              },
            ],
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: "Pharmacy Stock Chart",
                font: {
                  size: 24 
                },
              },
              legend: {
                display: false
              },
            },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Drug Name(s)'
              },
            },
            y: {
              title: {
                display: true,
                text: 'Quatity in Unit(s)'
              },
            },
          },
        },
      };
      var view = new Chart(chart, details);
      chart.style.display = "block";
    }
});
  