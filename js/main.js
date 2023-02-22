window.onload = (ev) => {
    let links = document.querySelectorAll("header #menu li a");
    let input = document.querySelector("header #menu input");
    for (let link of links) {
        link.onclick = (e) => {
            input.checked = !input.checked;
        };
    }
};
