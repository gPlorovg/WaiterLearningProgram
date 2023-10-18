const sub_btn = document.querySelector(".submit_btn");
sub_btn.addEventListener("click", submit);
const turn_back_btn = document.querySelector(".turn_back");
turn_back_btn.addEventListener("click", () => {history.back();});

const next_btn = document.createElement("button");
next_btn.classList.add("submit_btn");
next_btn.textContent = "Next";
next_btn.addEventListener("click", next);

const count_block = document.querySelector(".count");

const max_count = parseInt(count_block.children[2].textContent);

const inp_count_block = document.getElementById("inp_count_block");

const inp_count = document.getElementById("exam_count");

document.addEventListener("click", handle_click_outside);

count_block.addEventListener("click", () => {
        count_block.style.display = "none";
        inp_count_block.style.display = "block";
});

function handle_click_outside(event){
    if(!inp_count_block.contains(event.target) && !count_block.contains(event.target)) {
        inp_count_block.style.display = "none";
        count_block.style.display = "block";
        const new_count = parseInt(inp_count.value);
        if (1 <= new_count && new_count <= max_count) {
            window.localStorage["count"] =  inp_count.value;
            next();
        }
    }
}

const curr_count = document.getElementById("curr_count");
const section_ = document.getElementById("section");
const name_ = document.getElementById("name");

const check_container = document.querySelector(".checkbox_container");

const inp_price = document.getElementById("input_price");
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

   for (let c of Array.from(check_container.children)) {
       const c_inp = c.children[0];
       if (c_inp.checked) {
            if (true_ans["ingredients"].includes(c_inp.value)) {
                c_inp.setAttribute("style","border-color: #27A713;" +
                    "background-image: url(\"../static/icons/checkbox_true_mark.svg\") !important;")
            } else {
                mistake = true;
                c_inp.setAttribute("style","border-color: #E91515;" +
                    "background-image: url(\"../static/icons/checkbox_false_mark.svg\") !important;")
            }
       } else {
            if (true_ans["ingredients"].includes(c_inp.value)) {
                c_inp.style["backgroundImage"] = 'url("../static/icons/checkbox_true_mark.svg")';
                mistake = true;
            }
       }
    }
    if (!document.querySelector(".wrapper").contains(next_btn)) {
        sub_btn.insertAdjacentElement("afterend", next_btn);
    } else {
        next_btn.style.display = "block";
    }
    sub_btn.style.display = "none";
}

async function  next() {
    let url = window.location.href + "?exam_count=" + window.localStorage["count"];
    // url = check_mistake(url);
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
    for (const c of Array.from(check_container.children)) {
        c.style["borderColor"] = "#1E1E1E";
        c.style["backgroundImage"] = 'none';
    }

    check_container.innerHTML = "";
    for (const ing of data["ingredients"]) {
        const checkbox = document.createElement("label");
        checkbox.innerHTML = "<input type=\"checkbox\" class=\"checkbox\"/><text>";
        checkbox.children[0].setAttribute("value", ing.toString());
        checkbox.children[1].textContent = ing.toString();
        check_container.insertAdjacentElement("beforeend", checkbox);
    }
    window.localStorage["count"] = data["count"];
    window.localStorage["true_ans"] = data["true_ans"];
    true_ans = data["true_ans"];
}

async function complete() {
    // check_mistake("");
    const resp = await fetch(window.origin + "/wlp" + "/result", {
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

// function check_mistake(url="") {
//     let cocktails_mis = JSON.parse(window.localStorage["cocktails_mistakes"]);
//     results[parseInt(curr_count.textContent)] = !mistake;
//     if (mistake && !(cocktails_mis.includes(true_ans["id"]))) {
//         url += "&mistake=" + mistake + "&user_id=" + window.localStorage["user_id"];
//         cocktails_mis.push(true_ans["id"]);
//         window.localStorage["cocktails_mistakes"] = JSON.stringify(cocktails_mis);
//     }
//     return url;
// }