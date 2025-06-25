function showToast(text, color = "#22c55e") {
  Toastify({
    text: text,
    duration: 3000,
    gravity: "top",
    position: "right",
    backgroundColor: color
  }).showToast();
}
