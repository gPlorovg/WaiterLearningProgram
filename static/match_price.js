const sub_btn = document.querySelector(".submit_btn");
sub_btn.addEventListener("click", submit);
const turn_back_btn = document.querySelector(".turn_back");
turn_back_btn.addEventListener("click", () => {history.back();});

const next_btn = document.createElement("button");
next_btn.classList.add("submit_btn");
next_btn.textContent = "Next";
next_btn.addEventListener("click", () => {window.location.reload();});

const retry_btn = document.createElement("button");
retry_btn.classList.add("submit_btn");
retry_btn.textContent = "Retry";
retry_btn.addEventListener("click", retry);

for (const b of document.querySelectorAll(".down")) {
    b.addEventListener("click", move_down);
}

for (const b of document.querySelectorAll(".up")) {
    b.addEventListener("click", move_up);
}

const rows = document.querySelectorAll(".match_row")

function retry() {

}

function move_up(evt) {
    const movable = evt.currentTarget.parentElement;
    const new_id = parseInt(movable.parentElement.id) > 0 ? (parseInt(movable.parentElement.id) - 1) % rows.length :
        rows.length - 1;
    const new_row = document.getElementById(new_id.toString());
    console.log(movable);
    console.log(new_id);
    console.log(new_row)
    movable.parentElement.appendChild(new_row.children[1]);
    new_row.appendChild(movable);
}

function move_down(evt) {
    const movable = evt.currentTarget.parentElement;
    const new_id = (parseInt(movable.parentElement.id) + 1) % rows.length;
    const new_row = document.getElementById(new_id.toString());
    console.log(movable);
    console.log(new_id);
    console.log(new_row)
    movable.parentElement.appendChild(new_row.children[1]);
    new_row.appendChild(movable);
}

function submit() {
    const resp = {};
    const names_rows = {};

    for (const r of rows) {
        resp[r.children[0].textContent] = parseInt(r.children[1].children[1].textContent.slice(0,-1));
        names_rows[r.children[0].textContent] = r;
    }

    const true_ans = JSON.parse(window.localStorage["true_ans"]);
    for (const i in true_ans) {
        const name = true_ans[i]["name"];
        if (resp[name] === true_ans[i]["price"]) {
            names_rows[name].children[0].style["borderColor"] = "#27A713";
            names_rows[name].children[1].children[1].style["borderColor"] = "#27A713";
        } else {
            names_rows[name].children[0].style["borderColor"] = "#E91515";
            names_rows[name].children[1].children[1].style["borderColor"] = "#E91515";
        }
    }

    sub_btn.insertAdjacentElement("afterend", next_btn);
    sub_btn.insertAdjacentElement("afterend", retry_btn);
    sub_btn.style.display = "none";
}


