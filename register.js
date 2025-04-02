document.addEventListener("DOMContentLoaded", function () {
  const origin = document.getElementById("register").innerHTML;
  var registerForm = document.getElementById("register");
  registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    register(new FormData(e.target));
  });
  async function register(formData) {
    var formObj = {};
    formData.forEach((value, key) => {
      formObj[key] = value;
    });
    await fetch('http://localhost:5000/register', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...formObj }),
    })
    .then(response => response.text())
    .then(data => console.log(data));
  }
  var roleSelect = document.getElementById("roles");
  roleSelect.addEventListener("change", (e) => {
    e.preventDefault();
    console.log("Changed to: " + roleSelect.value)
    registerForm.innerHTML = origin;
    registerForm.style.display = "block";
    if (roleSelect.value == "Patient") {
      registerForm.innerHTML += "<hr><h3>Role Specific Information:</h3><label for=\"ssn\">SSN:</label><input name=\"ssn\" id=\"ssn\" type=\"string\" required><br><label for=\"name\">Name:</label><input name=\"name\" id=\"name\" type=\"string\" required><br><p><input type=\"submit\" value=\"Register\"></input>";
    } else if (roleSelect.value == "Doctor") {
      registerForm.innerHTML += "<hr><h3>Role Specific Information:</h3><label for=\"dr_id\">Doctor Id:</label><input name=\"dr_id\" id=\"dr_id\" type=\"string\" required><br><label for=\"dr_type\">Type of Doctor:</label><input name=\"dr_type\" id=\"dr_type\" type=\"string\" required><br><p><input type=\"submit\" value=\"Register\"></input>";
    } else if (roleSelect.value == "Pharmacy") {
      registerForm.innerHTML += "<hr><h3>Role Specific Information:</h3><label for=\"pharma_id\">Pharmacy Id:</label><input name=\"pharma_id\" id=\"pharma_id\" type=\"string\" required><br><label for=\"hours\">Hours:</label><input name=\"hours\" id=\"hours\" type=\"string\" required><br><p><input type=\"submit\" value=\"Register\"></input>";
    } else {
      registerForm.style.display = "none";
    }
  });
});
