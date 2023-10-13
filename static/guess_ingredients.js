const sub_btn = document.querySelector(".submit_btn");
sub_btn.addEventListener("click", submit);
const turn_back_btn = document.querySelector(".turn_back");
turn_back_btn.addEventListener("click", () => {history.back();});
const checkboxes = document.querySelectorAll(".checkbox");

const next_btn = document.createElement("button");
next_btn.classList.add("submit_btn");
next_btn.textContent = "Next";
next_btn.addEventListener("click", () => {window.location.reload();});

function submit() {
    for (let c of checkboxes) {
        // if (JSON.parse(window.localStorage["true_ans"]).includes(c.value)) {
        //         c.style["backgroundImage"] = 'url("../static/icons/checkbox_true_mark.svg")';
        // } else {
        //         c.style["backgroundImage"] = 'url("../static/icons/checkbox_false_mark.svg")';
        // }
        if (c.checked) {
            if (JSON.parse(window.localStorage["true_ans"]).includes(c.value)) {
                c.style["borderColor"] = "#27A713";
                c.style["backgroundImage"] = 'url("../static/icons/checkbox_true_mark.svg")';
            } else {
                c.style["borderColor"] = "#E91515";
                c.style["backgroundImage"] = 'url("../static/icons/checkbox_false_mark.svg")';
            }
        } else {
            if (JSON.parse(window.localStorage["true_ans"]).includes(c.value)) {
                c.style["backgroundImage"] = 'url("../static/icons/checkbox_true_mark.svg")';
            }
        }
    }
    sub_btn.insertAdjacentElement("afterend", next_btn);
    sub_btn.style.display = "none";
}


