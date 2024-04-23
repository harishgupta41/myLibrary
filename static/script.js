document.getElementById("login").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    if(form.get("username") === "" || form.get("password") === ""){
        return false;
    }else{
        e.target.submit();
    }
})