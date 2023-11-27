document.addEventListener('DOMContentLoaded', function() {
const parallax = document.querySelector(".parallax");

window.addEventListener("mousemove", (e) => {
    const x = ((e.pageX) / 100)*3;
    const y = ((e.pageY) / 100)*3;

    parallax.style.transform = `translateX(${x}px) translateY(${y}px)`;
});
});