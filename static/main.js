bar_btn = document.querySelector("#bar");
cocktails_btn = document.querySelector("#cocktails");
menu_btn = document.querySelector("#menu");

bar_btn.addEventListener("click", () => {window.location = window.location.origin + "/bar" +
    "?mistakes_count=" + JSON.parse(window.localStorage["drinks_mistakes"]).length;});
cocktails_btn.addEventListener("click", () => {window.location = window.location.origin + "/cocktails" +
    "?mistakes_count=" + JSON.parse(window.localStorage["cocktails_mistakes"]).length;});
menu_btn.addEventListener("click", () => {window.location = window.location.origin + "/menu" +
    "?mistakes_count=" + JSON.parse(window.localStorage["meal_mistakes"]).length;});
