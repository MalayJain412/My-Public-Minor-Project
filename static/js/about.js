document.addEventListener("DOMContentLoaded", function () {
    const section = document.querySelector(".animated-section");

    function handleScroll() {
        const sectionPosition = section.getBoundingClientRect().top;
        const viewportHeight = window.innerHeight;

        if (sectionPosition < viewportHeight && sectionPosition > 0) {
            // Section is in view, move to center
            section.classList.add("center");
            section.classList.remove("right");
        } else if (sectionPosition <= 0) {
            // Section has been scrolled past, move to the right
            section.classList.remove("center");
            section.classList.add("right");
        } else {
            // Section is off-screen to the left
            section.classList.remove("center");
            section.classList.remove("right");
        }
    }

    // Attach the scroll event listener
    window.addEventListener("scroll", handleScroll);

    // Trigger animation on page load
    handleScroll();
});


document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll(".platform-approach-content");

    function handleScrollAnimation() {
        sections.forEach((section) => {
            const sectionTop = section.getBoundingClientRect().top;
            const sectionBottom = section.getBoundingClientRect().bottom;
            const viewportHeight = window.innerHeight;

            const contentLeft = section.querySelector(".approach-description-container");
            const contentRight = section.querySelector(".approach-image-container");

            if (sectionTop < viewportHeight && sectionBottom > 0) {
                // When section enters viewport
                contentLeft.classList.add("visible-center");
                contentRight.classList.add("visible-center");
                contentLeft.classList.remove("move-outwards");
                contentRight.classList.remove("move-outwards");
            } else if (sectionTop > viewportHeight || sectionBottom < 0) {
                // When section moves out of viewport
                contentLeft.classList.remove("visible-center");
                contentRight.classList.remove("visible-center");
                contentLeft.classList.add("move-outwards");
                contentRight.classList.add("move-outwards");
            }
        });
    }

    window.addEventListener("scroll", handleScrollAnimation);

    // Initial check on load
    handleScrollAnimation();
});


