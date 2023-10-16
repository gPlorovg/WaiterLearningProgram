const sub_btn = document.querySelector(".submit_btn");
sub_btn.addEventListener("click", submit);
const turn_back_btn = document.querySelector(".turn_back");
turn_back_btn.addEventListener("click", () => {history.back();});

const next_btn = document.createElement("button");
next_btn.classList.add("submit_btn");
next_btn.textContent = "Next";
next_btn.addEventListener("click", next);

const curr_count = document.getElementById("curr_count");
const section_ = document.getElementById("section");
const name_ = document.getElementById("name");

const description = document.querySelector(".description");

const inp_price = document.getElementById("input_price");
const radios = document.querySelectorAll(".radio");
let true_ans = JSON.parse(window.localStorage["true_ans"]);
let mistake = false;
let results = {};
function submit() {
    if (parseInt(inp_price.value) === true_ans["price"]) {
        inp_price.style["borderColor"] = "#27A713";
    } else {
        inp_price.style["borderColor"] = "#E91515";
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
    if (!document.querySelector(".wrapper").contains(next_btn)) {
        sub_btn.insertAdjacentElement("afterend", next_btn);
    } else {
        next_btn.style.display = "block";
    }
    sub_btn.style.display = "none";
    if (ans_radio === true_radio) {
        ans_radio.setAttribute("style", "background-image: url(\"../static/icons/radio_true_mark.svg\") !important;" +
            "border-color: #27A713;")
    } else {
        // ans_radio.style["borderColor"] = "#E91515";
        ans_radio.setAttribute("style", "background-image: url(\"../static/icons/radio_false_mark.svg\") !important;" +
            "border-color: #E91515;")
        // ans_radio.style["backgroundImage"] = 'url("../static/icons/radio_false_mark.svg")';
        mistake = true;
    }
}

async function  next() {
    results[parseInt(curr_count.textContent)] = !mistake;
    let url = window.location.href + "?exam_count=" + window.localStorage["count"]
    if (mistake && !(window.localStorage["drinks_mistakes"].includes(true_ans["id"]))) {
        url += "&mistake=" + mistake + "&user_id=" + window.localStorage["user_id"];
    }
    const resp = await fetch(url);
    if (resp.status === 200) {
        const data = await resp.json();
        update_page(data);
        next_btn.style.display = "none";
        sub_btn.style.display = "block";
    } else if (resp.status === 201) {
        const data = await resp.json();
        update_page(data);

        const complete_btn = document.createElement("button");
        complete_btn.classList.add("submit_btn");
        complete_btn.textContent = "Complete";
        complete_btn.addEventListener("click", complete);
        next_btn.insertAdjacentElement("afterend", complete_btn);
        next_btn.style.display = "none";
    }
}

function update_page(data) {
    curr_count.textContent = data["count"];
    section_.textContent = data["section"];
    name_.textContent = data["name"];

    inp_price.style["borderColor"] = "#1E1E1E";
    inp_price.value = "";
    description.textContent = data["description"];
    for (const r of radios) {
        r.style["borderColor"] = "#1E1E1E";
        r.style["backgroundImage"] = 'none';
    }
    for (const [i, r] of radios.entries()) {
        const key = Object.keys(data["serving"])[i];
        r.value = key;
        r.parentElement.children[1].textContent = data["serving"][key];
    }
    window.localStorage["count"] = data["count"];
    window.localStorage["true_ans"] = data["true_ans"];
    true_ans = data["true_ans"];
}

async function complete() {
    results[curr_count.textContent] = !mistake;
    const resp = await fetch(window.origin + "/result", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(results)
    });
    if (resp.status === 200) {
        document.body.innerHTML = await resp.text();
    }
}