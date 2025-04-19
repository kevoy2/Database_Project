document.addEventListener("DOMContentLoaded", function () {
    var loginForm = document.getElementById("stock");
    var stockView = document.getElementById("view");
    var logoutButton = document.getElementById("logout");
    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        stock(new FormData(e.target));
    });
    stockView.addEventListener("click", (e) => {
      e.preventDefault(); 
      view();
    });
    logoutButton.addEventListener("click", (e) => {
      e.preventDefault(); 
      sessionStorage.removeItem("id");
      window.location.href = "./index.html";
    });
    async function stock(body) {
        var formObj = {};
        body.forEach((value, key) => {
          formObj[key] = value;
        });
        console.log(formObj["quan"]);
        const response = await fetch("http://localhost:5000/add-stock", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ...formObj, pharma: sessionStorage.getItem("id") }),
        })
        .then(response => response.json());
        console.log(response["message"]);
    }
    async function view() {
      const response = await fetch("http://localhost:5000/view-stock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pharma: sessionStorage.getItem("id"), exempt: "" }),
      })
      .then(response => response.json());
      console.log(response["message"]);
      const chart = document.getElementById("chart");
      const details = {
        type: "bar",
        data: {
            labels: response["x"],
            datasets: [
            {
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
              }
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
  }
);
  