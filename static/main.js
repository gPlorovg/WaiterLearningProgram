bar_btn = document.querySelector("#bar");
cocktails_btn = document.querySelector("#cocktails");
menu_btn = document.querySelector("#menu");

bar_btn.addEventListener("click", () => {window.location = window.location.origin + "/bar";});
cocktails_btn.addEventListener("click", () => {window.location = window.location.origin + "/cocktails";});
menu_btn.addEventListener("click", () => {window.location = window.location.origin + "/menu";});
