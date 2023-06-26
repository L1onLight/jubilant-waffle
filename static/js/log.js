if (document.getElementById("registerForm")) {
    const regForm = document.getElementById("registerForm");
    const logForm = document.getElementById("loginForm");
    const logBtn = document.getElementById("logBtn");
    const regBtn = document.getElementById("regBtn");
    logBtn.addEventListener("click", transformForm);
    regBtn.addEventListener("click", transformForm);

    function transformForm(event) {
        event.preventDefault();

        if (regForm.classList.contains("hidden")) {
            regForm.classList.remove("hidden");
            logForm.classList.add("hidden");
        } else {
            regForm.classList.add("hidden");
            logForm.classList.remove("hidden");
        }
    }
}

var pass1 = document.getElementById("id_password");
var pass2 = document.getElementById("password-rep");

function checkPasswordMatch() {
    var pass1 = document.getElementById("id_password").value;
    var pass2 = document.getElementById("password_rep").value;

    var errorDiv = document.getElementById("error-div");
    errorDiv.innerHTML = "";

    // Clear any previous error message

    if (pass1 !== pass2 && pass1 !== "" && pass2 !== "") {
        var errorMessage = document.createElement("span");
        errorMessage.textContent = "Passwords do not match.";
        errorDiv.appendChild(errorMessage);
    }
}
document
    .getElementById("id_password")
    .addEventListener("input", checkPasswordMatch);
document
    .getElementById("password_rep")
    .addEventListener("input", checkPasswordMatch);

console.log(document.getElementById("error-div-reg").innerHTML.trim());
if (document.getElementById("error-div-reg").innerHTML.trim() !== "") {
    // Do something here
    const regForm = document.getElementById("registerForm");
    const logForm = document.getElementById("loginForm");
    // For example, display an alert
    transformFormAuto();
    function transformFormAuto() {
        if (regForm.classList.contains("hidden")) {
            regForm.classList.remove("hidden");
            logForm.classList.add("hidden");
        } else {
            regForm.classList.add("hidden");
            logForm.classList.remove("hidden");
        }
    }
}

const loginForm = document.getElementById("loginForm");
if (
    window.location.href.includes("login") &&
    window.location.href.includes("register") &&
    loginForm.className !== "hidden"
) {
    console.log("Hello");
    const regForm = document.getElementById("registerForm");
    const logForm = document.getElementById("loginForm");

    if (regForm.classList.contains("hidden")) {
        regForm.classList.remove("hidden");
        logForm.classList.add("hidden");
    }
    function removeRegisterFromUrl(event) {
        event.preventDefault(); // Prevent the default behavior of the link
        let modifiedUrl = window.location.href.replace("/register", "");
        window.location.replace(modifiedUrl);
    }

    // Add an event listener to the specified item
    const specifiedItem = document.getElementById("logBtn");
    specifiedItem.addEventListener("click", removeRegisterFromUrl);
}
