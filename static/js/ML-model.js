$('#predictionForm').on('submit', function (e) {
    e.preventDefault(); // Prevent form from refreshing the page

    $.ajax({
        url: '/predict',
        type: 'POST',
        data: $(this).serialize(),
        success: function (response) {
            // Update predicted diners
            $('#predictedDiners').text(response.predicted_diners);

            // Update scaled quantities table
            $('#scaledQuantities').empty();
            for (let item in response.scaled_quantities) {
                $('#scaledQuantities').append(`
                    <tr>
                        <td>${item}</td>
                        <td>${response.scaled_quantities[item]}</td>
                    </tr>
                `);
            }

            // Update individual ingredients
            $('#ingredients').empty();
            for (let dish in response.ingredients) {
                if (typeof response.ingredients[dish] === 'string') {
                    $('#ingredients').append(`
                        <div class="ingredient-item">
                            <strong>${dish}:</strong> ${response.ingredients[dish]}
                        </div>
                    `);
                } else {
                    let innerList = '<ul>';
                    for (let ing in response.ingredients[dish]) {
                        innerList += `<li>${ing}: ${response.ingredients[dish][ing]}</li>`;
                    }
                    innerList += '</ul>';

                    $('#ingredients').append(`
                        <div class="ingredient-item">
                            <strong>${dish}:</strong>
                            ${innerList}
                        </div>
                    `);
                }
            }

            // Update aggregated ingredients table
            $('#aggregatedIngredients').empty();
            for (let ingredient in response.aggregated_ingredients) {
                $('#aggregatedIngredients').append(`
                    <tr>
                        <td>${ingredient}</td>
                        <td>${response.aggregated_ingredients[ingredient]}</td>
                    </tr>
                `);
            }

            $('#repeated_cnt').text(response.repeated_count);

            // Show results
            $('#results').show();
            $('#error').hide();
        },
        error: function (xhr) {
            $('#error').text(xhr.responseJSON.error).show();
            $('#results').hide();
        }
    });
});
