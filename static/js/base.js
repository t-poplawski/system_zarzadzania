document.addEventListener('DOMContentLoaded', () => {
    const dropdownTrigger = document.querySelector('.dropdown-trigger button');
    const dropdown = document.querySelector('.dropdown');

    dropdownTrigger.addEventListener('click', () => {
        dropdown.classList.toggle('is-active');
    });

    document.addEventListener('click', (event) => {
        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove('is-active');
        }
    });
});
