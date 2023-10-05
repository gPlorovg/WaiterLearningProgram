btn = document.querySelector(".submit_btn");
email_ = document.querySelector("#inp_email");
name_ = document.querySelector("#inp_name");
password_ = document.querySelector("#inp_password");
btn.addEventListener("click", send_data)

async function send_data() {
    const req = {
        email: email_.value,
        name: name_.value,
        password: password_.value
    }
    const resp = await fetch(window.origin + "/sign_up", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        body: JSON.stringify(req)
    });

    switch (resp.status) {
        case 200:
            window.location = window.location.origin;
            break;
        case 409:
            error(email_.parentElement);
            break;
        default:
            window.location = window.location.origin + "/error" + "?status_code=" + resp.status;
            break;
    }
}

function error(el) {
    el.style["border-color"] = "red";
}