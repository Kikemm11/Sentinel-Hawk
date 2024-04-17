function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var passwordToggle = document.getElementById("password-toggle");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        passwordToggle.className = "fas fa-eye-slash";
    } else {
        passwordInput.type = "password";
        passwordToggle.className = "fas fa-eye";
    }
}

function togglePasswordVisibility2() {
    var passwordInput = document.getElementById("password2");
    var passwordToggle = document.getElementById("password-toggle2");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        passwordToggle.className = "fas fa-eye-slash";
    } else {
        passwordInput.type = "password";
        passwordToggle.className = "fas fa-eye";
    }
}
