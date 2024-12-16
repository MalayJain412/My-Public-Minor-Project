document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const profileImage = document.getElementById('profileImage');
    const transactionForm = document.getElementById('transactionForm');

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                profileImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    transactionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert("Transaction details submitted successfully!");
        // You can add your form submission logic here
    });
});
