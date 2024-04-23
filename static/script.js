function fun() {
  document.getElementById("login").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    if (form.get("username") === "" || form.get("password") === "") {
      return false;
    } else {
      e.target.submit();
    }
  });
}

function closeError() {
  document.getElementById("loginError").style.display = "none";
}

function toggleNavigation(state) {
  if (!state) document.getElementById("navbar").style.right = "0";
  else document.getElementById("navbar").style.right = "-100%";
}
