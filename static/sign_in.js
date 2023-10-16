const btn = document.querySelector(".submit_btn");
const name_ = document.querySelector("#inp_name");
const password_ = document.querySelector("#inp_password");
btn.addEventListener("click", send_data)

async function send_data() {
    const req = {
        name: name_.value,
        password: password_.value
    }
    const resp = await fetch(window.origin + "/sign_in", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        body: JSON.stringify(req)
    });
    console.log(resp.status);
    switch (resp.status) {
        case 200:
            const data = await resp.json();
            console.log(data);
            window.localStorage["drinks_mistakes"] = JSON.stringify(data["drinks_mistakes"]);
            window.localStorage["meal_mistakes"] = JSON.stringify(data["meal_mistakes"]);
            window.localStorage["cocktails_mistakes"] = JSON.stringify(data["cocktails_mistakes"]);
            window.localStorage.setItem("user_id", data["id"]);
            window.location = window.location.origin + "/main";
            break;
        case 401:
            error(name_);
            error(password_);
            break;
        default:
            window.location = window.location.origin + "/error" + "?status_code=" + resp.status;
            break;
    }
}

function error(el) {
    if (el.getAttribute("data-toggle") === "True") {
        el.style["borderColor"] = "red";
        const err_label = document.createElement("label");
        err_label.classList.add("err_label")
        err_label.textContent = "Wrong " + el.getAttribute("name") + "!";
        el.parentElement.insertAdjacentElement("afterbegin", err_label);
        el.setAttribute("data-toggle", "False")
    }
}