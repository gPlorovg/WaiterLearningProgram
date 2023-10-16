const buttons = document.querySelectorAll(".game");
const turn_back_btn = document.querySelector(".turn_back");
turn_back_btn.addEventListener("click", () => {window.location = window.location.origin + "/wlp"});

for (let b of buttons) {
    b.addEventListener("click", () => {window.location = window.location.origin + window.location.pathname
        + "/" + b.id});
}
