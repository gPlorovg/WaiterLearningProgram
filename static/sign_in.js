btn = document.querySelector(".submit_btn");
name_ = document.querySelector("#inp_name");
password_ = document.querySelector("#inp_password");
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
            window.localStorage["drinks_mistakes"] = data["drinks_mistakes"];
            window.localStorage["meal_mistakes"] = data["meal_mistakes"];
            window.localStorage["cocktails_mistakes"] = data["cocktails_mistakes"];
            window.location = window.location.origin + "/main";
            break;
        case 401:
            error(name_.parentElement);
            error(password_.parentElement);
            break;
        default:
            window.location = window.location.origin + "/error" + "?status_code=" + resp.status;
            break;
    }
}

function error(el) {
    el.style["borderColor"] = "red";
}