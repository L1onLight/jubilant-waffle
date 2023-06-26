if (window.location.href.includes("?code")) {
    const regForm = document.getElementById("registerForm");
    const logForm = document.getElementById("loginForm");
    regForm.classList.remove("hidden");
    logForm.classList.add("hidden");
    console.log(window.location.href);
}

const urlParams = new URLSearchParams(window.location.search);
const codeValue = urlParams.get("code");
console.log(urlParams, codeValue);
document.getElementById("restoreCode").value = codeValue;
