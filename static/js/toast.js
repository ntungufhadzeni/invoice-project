
htmx.on("showMessage", (e) => {
  let x = document.getElementById("snackbar")

  x.innerHTML = e.detail.value

    // Add the "show" class to DIV
  x.className = "show";

    // After 5 seconds, remove the show class from DIV
    setTimeout(function(){
      x.className = x.className.replace("show", ""); }, 5000);
});

