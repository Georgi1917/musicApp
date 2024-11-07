const logoutButton = document.getElementById("logout-button");

logoutButton.addEventListener("click", () => {
    document.getElementById('logout-form').submit();
})