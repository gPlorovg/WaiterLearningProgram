const buttons = document.querySelectorAll("button")
for (let b of buttons) {
    b.addEventListener("click", () => {window.location = window.location + "/" + b.id})
}