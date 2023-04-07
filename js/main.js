function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

window.onload = (ev) => {
    let links = document.querySelectorAll("header #menu li a");
    let input = document.querySelector("header #menu input");

    for (let link of links) {
        link.onclick = (e) => {
            input.checked = !input.checked;
        };
    }

    // Number animations.
    if (document.querySelector("#numbers")) {
        let animated = false;
        var observer = new IntersectionObserver(function (entries) {
            if (entries[0].isIntersecting === true && !animated) {
                animateValue(document.querySelector("#numbers .col1 .number"), 0, 32, 1500);
                animateValue(document.querySelector("#numbers .col2 .number"), 0, 8, 500);
                animateValue(document.querySelector("#numbers .col3 .number"), 0, 16, 1000);
                animated = true;
            }
        }, { threshold: [0] });
        observer.observe(document.querySelector("#numbers"));
    }
};
