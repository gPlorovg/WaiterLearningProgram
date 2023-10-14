const sub_btn = document.querySelector(".submit_btn");
sub_btn.addEventListener("click", submit);
const turn_back_btn = document.querySelector(".turn_back");
turn_back_btn.addEventListener("click", () => {history.back();});

const next_btn = document.createElement("button");
next_btn.classList.add("submit_btn");
next_btn.textContent = "Next";
next_btn.addEventListener("click", next);

const inp_price = document.getElementById("input_price");
const inp_volume = document.getElementById("input_volume");
const radios = document.querySelectorAll(".radio");
const true_ans = JSON.parse(window.localStorage["true_ans"]);
let mistake = false;
function submit() {
    if (parseInt(inp_price.value) === true_ans["price"]) {
        inp_price.style["borderColor"] = "#27A713";
    } else {
        inp_price.style["borderColor"] = "#E91515";
        mistake = true;
    }

    if (parseInt(inp_volume.value) === true_ans["volume"]) {
        inp_volume.style["borderColor"] = "#27A713";
    } else {
        inp_volume.style["borderColor"] = "#E91515";
        mistake = true;

    }

    let ans_radio = Node;
    let true_radio = Node;
    for (let r of radios) {
        if (r.checked) {
            ans_radio = r;
        }
        if (r.value === true_ans["serving_short"]) {
            true_radio = r;
            true_radio.style["borderColor"] = "#27A713";
        }
    }
    sub_btn.insertAdjacentElement("afterend", next_btn);
    sub_btn.style.display = "none";
    if (ans_radio === true_radio) {
        ans_radio.style["backgroundImage"] = 'url("../static/icons/radio_true_mark.svg")';
    } else {
        ans_radio.style["borderColor"] = "#E91515";
        ans_radio.style["backgroundImage"] = 'url("../static/icons/radio_false_mark.svg")';
        mistake = true;
    }
}

function next() {
    const url = window.location.href + "?exam_count=" + window.localStorage["count"] + "&mistake=" + mistake
        + "&user_id=" + window.localStorage["user_id"];
    const resp = fetch(url);
}