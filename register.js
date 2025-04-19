document.addEventListener("DOMContentLoaded", function () {
  const origin = document.getElementById("register").innerHTML;
  var registerForm = document.getElementById("register");
  var roleSelect = document.getElementById("roles");
  registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    register(new FormData(e.target));
  });
  async function register(formData) {
    var formObj = {};
    formData.forEach((value, key) => {
      formObj[key] = value;
    });
    var roleSelect = document.getElementById("roles");
    let response = await fetch('http://localhost:5000/register', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...formObj, role: roleSelect.value }),
    })
    .then(response => response.json());
    if (response["message"] === "Registration data received successfully") {
      alert("Registration was successfully");
    } else {
      alert("Registration was unsuccessfully, try again");
    }
  }
  roleSelect.addEventListener("change", (e) => {
    e.preventDefault();
    console.log("Changed to: " + roleSelect.value)
    registerForm.innerHTML = origin;
    registerForm.style.display = "block";
    if (roleSelect.value == "Patient") {
      registerForm.innerHTML += "<hr><h3>Role Specific Information:</h3><label for=\"ssn\">SSN:</label><input name=\"ssn\" id=\"ssn\" type=\"string\" minlength=\"11\" maxlength=\"11\" required><br><label for=\"dob\">Date of Birth</label><input name=\"dob\" id=\"dob\" type=\"date\" max=\"2015-01-01\"></input><br><label for\"gender\">Gender:</label><select name=\"gender\" id=\"gender\" required><option value=\"\">None</option><option value=\"Male\">Male</option><option value=\"Female\">Female</option></select><p><input type=\"submit\" value=\"Register\"></input>";
    } else if (roleSelect.value == "Doctor") {
      registerForm.innerHTML += "<hr><h3>Role Specific Information:</h3><label for=\"dr_id\">Doctor Id:</label><input name=\"dr_id\" id=\"dr_id\" type=\"string\" minlength=\"5\" maxlength=\"8\" required><br><label for=\"dr_type\">Type of Doctor:</label><input name=\"dr_type\" id=\"dr_type\" type=\"string\" maxlength=\"60\" required><br><p><input type=\"submit\" value=\"Register\"></input>";
    } else if (roleSelect.value == "Pharmacy") {
      registerForm.innerHTML += "<hr><h3>Role Specific Information:</h3><label for=\"pharma_id\">Pharmacy Id:</label><input name=\"pharma_id\" id=\"pharma_id\" type=\"string\" minlength=\"5\" maxlength=\"8\" required><br><label for=\"hours\">Hours:</label><input name=\"hours\" id=\"hours\" type=\"string\" maxlength=\"100\" required><br><p><input type=\"submit\" value=\"Register\"></input>";
    } else {
      registerForm.style.display = "none";
    }
  });
});
