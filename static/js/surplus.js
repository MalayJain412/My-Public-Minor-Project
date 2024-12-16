const foodItems = [
    'Pav Bhaji', 'Dosa', 'Idli', 'Puri Bhaji', 'Poha', 'Upma', 'Chole', 'Aloo Gobi', 'Rajma', 'Paneer Butter Masala',
    'Dal Tadka', 'Bhindi Fry', 'Palak Paneer', 'Butter Chicken', 'Methi Thepla', 'Pav Bhaji', 'Aloo Paratha',
    'Baingan Bharta', 'Dal Tadka', 'Chole', 'Aloo Gobi', 'Bhindi Fry', 'Paneer Butter Masala', 'Gobi Manchurian',
    'Kadhi Pakora', 'Chana Masala', 'Dum Aloo', 'Pulao', 'Roti', 'Paratha', 'Naan', 'Rice', 'Jalebi', 'Gulab Jamun',
    'Kheer', 'Halwa'
];

document.addEventListener('DOMContentLoaded', () => {
    const quantityInput = document.getElementById('quantity');
    const inputCardsContainer = document.getElementById('input-cards-container');
    const continueButton = document.querySelector('.unique-continue-button-XYZ123');
    const sendEmailButton = document.querySelector('.unique-send-email-button-XYZ123');
    const surplusForm = document.getElementById('surplus-form');
    const surplusResults = document.getElementById('surplus-results').querySelector('tbody');

    continueButton.addEventListener('click', () => {
        const qty = parseInt(quantityInput.value);
        inputCardsContainer.innerHTML = '';
        const currentDateTime = new Date().toISOString().slice(0, 16);

        for (let i = 0; i < qty; i++) {
            const inputCard = document.createElement('div');
            inputCard.className = 'unique-input-card-XYZ123 card';
            inputCard.style.width = '300px';
            inputCard.style.margin = '10px';
            inputCard.innerHTML = `
                <div class="card-body">
                    <label for="foodItem-${i}" class="unique-label-XYZ123 form-label">Food Item:</label>
                    <select name="foodItem-${i}" id="foodItem-${i}" class="unique-select-XYZ123 form-select mb-2">
                        <option value="">Select Food Item</option>
                        ${foodItems.map(item => `<option value="${item}">${item}</option>`).join('')}
                    </select>
                    <div class="d-flex mb-2">
                        <div class="form-group me-2 flex-grow-1">
                            <label for="quantity-${i}" class="unique-label-XYZ123 form-label">Quantity:</label>
                            <input type="number" name="quantity-${i}" id="quantity-${i}" class="unique-select-XYZ123 form-control" placeholder="Enter quantity">
                        </div>
                        <div class="form-group flex-grow-1">
                            <label for="unit-${i}" class="unique-label-XYZ123 form-label">Unit:</label>
                            <select name="unit-${i}" id="unit-${i}" class="unique-select-XYZ123 form-select" style="height:50px">
                                <option value="">Select Unit</option>
                                <option value="kg">kg</option>
                                <option value="pieces">pieces</option>
                                <option value="liter">liter</option>
                                <option value="plates">plates</option>
                            </select>
                        </div>
                        <div class="form-group me-2 flex-grow-1" style="margin-left:30%;">
                            <label for="price-${i}" class="unique-label-XYZ123 form-label">Total Price:</label>
                            <input type="number" name="price-${i}" id="price-${i}" class="unique-select-XYZ123 form-control" placeholder="Enter amount">
                        </div>
                    </div>
                    <label for="expiry-${i}" class="unique-label-XYZ123 form-label">Expiry Date & Time:</label>
                    <input type="datetime-local" name="expiry-${i}" id="expiry-${i}" class="unique-select-XYZ123 form-control" min="${currentDateTime}">
                </div>
            `;
            inputCardsContainer.appendChild(inputCard);
        }
    });

    surplusForm.addEventListener('submit', (e) => {
        e.preventDefault();
        surplusResults.innerHTML = '';
        const inputs = inputCardsContainer.querySelectorAll('.unique-input-card-XYZ123');
        inputs.forEach((inputCard, index) => {
            const foodItem = inputCard.querySelector(`#foodItem-${index}`).value;
            const quantity = inputCard.querySelector(`#quantity-${index}`).value;
            const unit = inputCard.querySelector(`#unit-${index}`).value;
            const price = inputCard.querySelector(`#price-${index}`).value;
            const expiry = inputCard.querySelector(`#expiry-${index}`).value;
            const row = document.createElement('tr');
            row.innerHTML = `<td>${foodItem}</td><td>${quantity}</td><td>${unit}</td><td>${price}</td><td>${expiry}</td>`;
            surplusResults.appendChild(row);
        });
    });

    sendEmailButton.addEventListener('click', () => {
        $('#emailSentModal').modal('show'); setTimeout(() => {
            document.getElementById('loadingSpinner').classList.add('d-none');
            document.getElementById('emailSuccessMessage').classList.remove('d-none');
            setTimeout(() => {
                location.reload();
            }, 3000); // Refresh the page 3 seconds after showing the success message
        }, 2000); // Simulate 2 seconds of loading time 
    });
});
