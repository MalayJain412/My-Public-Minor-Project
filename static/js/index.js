document.addEventListener('DOMContentLoaded', () => {
    const featureCards = document.querySelectorAll('.feature-card');

    featureCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.style.transform = 'scale(1.05) translateX(10px)';
        });

        card.addEventListener('mouseout', () => {
            card.style.transform = 'scale(1) translateX(0)';
        });
    });
});
