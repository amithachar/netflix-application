// ===============================
// Horizontal Scroll Enhancement
// ===============================

document.querySelectorAll(".carousel").forEach((carousel) => {
    carousel.addEventListener("wheel", (e) => {
        e.preventDefault();
        carousel.scrollLeft += e.deltaY;
    });
});

// ===============================
// Scroll Buttons (Optional)
// ===============================

document.querySelectorAll(".scroll-btn-left").forEach(btn => {
    btn.addEventListener("click", function () {
        const carousel = this.parentElement.querySelector(".carousel");
        carousel.scrollBy({ left: -400, behavior: "smooth" });
    });
});

document.querySelectorAll(".scroll-btn-right").forEach(btn => {
    btn.addEventListener("click", function () {
        const carousel = this.parentElement.querySelector(".carousel");
        carousel.scrollBy({ left: 400, behavior: "smooth" });
    });
});

// ===============================
// Card Hover Effect
// ===============================

document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("mouseenter", () => {
        card.style.transform = "scale(1.08)";
        card.style.zIndex = "10";
        card.style.transition = "0.3s ease";
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "scale(1)";
        card.style.zIndex = "1";
    });
});

// ===============================
// Sidebar Expand on Hover
// ===============================

const sidebar = document.querySelector(".sidebar");

if (sidebar) {
    sidebar.addEventListener("mouseenter", () => {
        sidebar.style.width = "200px";
    });

    sidebar.addEventListener("mouseleave", () => {
        sidebar.style.width = "70px";
    });
}

// ===============================
// Hero Auto Slider (Optional)
// ===============================

let currentSlide = 0;
const heroSlides = document.querySelectorAll(".hero-slide");

if (heroSlides.length > 0) {
    setInterval(() => {
        heroSlides.forEach(slide => slide.style.display = "none");

        currentSlide++;
        if (currentSlide >= heroSlides.length) {
            currentSlide = 0;
        }

        heroSlides[currentSlide].style.display = "block";
    }, 5000);
}

// ===============================
// Mobile Responsive Fix
// ===============================

function checkMobile() {
    if (window.innerWidth < 768) {
        document.querySelectorAll(".carousel").forEach(carousel => {
            carousel.style.gap = "10px";
        });
    }
}

window.addEventListener("resize", checkMobile);
checkMobile();
