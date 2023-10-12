const sub_btn = document.querySelector(".submit_btn");
sub_btn.addEventListener("click", submit);
const turn_back_btn = document.querySelector(".turn_back");
turn_back_btn.addEventListener("click", () => {history.back();});
const radios = document.querySelectorAll(".radio");

const next_btn = document.createElement("button");
next_btn.classList.add("submit_btn");
next_btn.textContent = "Next";
next_btn.addEventListener("click", () => {window.location.reload();});

function submit() {
    let ans_radio = Node;
    let true_radio = Node;
    for (let r of radios) {
        if (r.checked) {
            ans_radio = r;
        }
        if (r.value === window.localStorage["true_ans"]) {
            true_radio = r;
        }
    }
    sub_btn.insertAdjacentElement("afterend", next_btn);
    sub_btn.style.display = "none";
    true_radio.style["borderColor"] = "#27A713";
    if (ans_radio === true_radio) {
        ans_radio.style["backgroundImage"] = 'url("../static/icons/radio_true_mark.svg")';
    } else {
        ans_radio.style["borderColor"] = "#E91515";
        ans_radio.style["backgroundImage"] = 'url("../static/icons/radio_false_mark.svg")';
    }
}


