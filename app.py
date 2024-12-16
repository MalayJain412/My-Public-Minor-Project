from flask import Flask, request, render_template, jsonify
import numpy as np
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import gzip

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Load the compressed pickle file
compressed_file_name1 = 'model1.pkl.gz'
with gzip.open(compressed_file_name1, 'rb') as file:
    model1 = pickle.load(file)


# Load the compressed pickle file
compressed_file_name2 = "model2.pkl.gz"
with gzip.open(compressed_file_name2, 'rb') as file:
    model2 = pickle.load(file)


# Function to convert 'Expected Diners Range' to numeric features (for model 1)
def convert_range_to_features(range_str):
    if pd.isna(range_str) or range_str == '':
        return np.nan, np.nan, np.nan  # Handle missing values
    lower, upper = map(int, range_str.split('-'))
    return lower, upper, upper - lower  # Return lower, upper, and range width

# Function to preprocess custom input data for model 1
def preprocess_custom_data(input_data):
    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Encode 'Weekend' and 'Holiday' to numerical values (if not already done)
    input_df['Weekend'] = input_df['Weekend'].map({'Yes': 1, 'No': 0})
    input_df['Holiday'] = input_df['Holiday'].map({'Yes': 1, 'No': 0})

    # Feature Engineering (same as during training)
    input_df['Event Duration Squared'] = input_df['Event Duration (hours)'] ** 2
    input_df['Expected Diners Lower'], input_df['Expected Diners Upper'], input_df['Expected Diners Range Width'] = zip(
        *input_df['Expected Diners Range'].apply(convert_range_to_features)
    )

    # Drop the 'Expected Diners Range' column
    input_df.drop(columns=['Expected Diners Range'], inplace=True)

    # Binning Event Duration
    bins = [0, 5, 10, 15, 20]
    labels = ['Short', 'Medium', 'Long', 'Very Long']
    input_df['Event Duration Binned'] = pd.cut(input_df['Event Duration (hours)'], bins=bins, labels=labels)

    # Frequency Encoding for Weather
    weather_freq = input_df['Weather'].value_counts()
    input_df['Weather_Frequency'] = input_df['Weather'].map(weather_freq)

    return input_df

# Function to handle prediction (preprocessing + prediction) for model 1
def predict_diners(input_data):
    # Preprocess the custom input data
    preprocessed_data = preprocess_custom_data(input_data)

    # Use the model to predict the number of diners
    predicted_diners = model1.predict(preprocessed_data)

    return predicted_diners[0]  # Return the predicted number of diners

# Function to scale quantities
def scale_quantities(predicted_quantities, diners):
    base_quantities = {
        'Paneer Tikka': 50, 'Stuffed Mushrooms': 45, 'Mini Samosas': 40, 
        'Veg Spring Rolls': 40, 'Hara Bhara Kabab': 50, 'Corn Chaat': 35, 
        'Mini Quiches': 60, 'Sev Puri': 50, 'Veg Seekh Kebab': 45, 
        'Hummus and Pita': 10, 'Dhokla': 40, 'Bruschetta': 30, 'Onion Bhaji': 45,
        'Bhel Puri': 50, 'Papdi Chaat': 40, 'Aloo Tikki': 45
    }

    units = {
        'Paneer Tikka': 'plates', 'Stuffed Mushrooms': 'plates', 'Mini Samosas': 'plates', 
        'Veg Spring Rolls': 'plates', 'Hara Bhara Kabab': 'plates', 'Corn Chaat': 'plates',
        'Mini Quiches': 'plates', 'Sev Puri': 'plates', 'Veg Seekh Kebab': 'plates', 
        'Hummus and Pita': 'kg', 'Dhokla': 'plates', 'Bruschetta': 'plates', 'Onion Bhaji': 'plates',
        'Bhel Puri': 'plates', 'Papdi Chaat': 'plates', 'Aloo Tikki': 'plates'
    }

    scaled_quantities = {}
    no_unit_qt={}
    for item, fraction in predicted_quantities.items():
        base_quantity = base_quantities[item]
        unit = units[item]
        scaled_quantity = (fraction * base_quantity * diners) / 50  # Adjust for the number of diners
        scaled_quantities[item] = f"{round(scaled_quantity, 2)} {unit}"
        no_unit_qt[item]=round(scaled_quantity, 2)

    return scaled_quantities,no_unit_qt

# Function to predict the quantities for menu items using model 2
def predict_quantities_for_menu(diners, event, season, time_of_day, menu_items):
    # Create a dummy input for the second model (you would have actual features)
    input_data = pd.DataFrame({
        'event': [event],  # Event type code
        'season': [season],  # Season type code
        'time_of_day': [time_of_day],  # Time of day code
        'diners': [diners]
    })

    # Predict the quantities for each menu item
    predicted_quantities = model2.predict(input_data)[0]

    # Scale the predicted quantities based on the number of diners
    scaled_quantities = scale_quantities(dict(zip(menu_items, predicted_quantities)), diners)
    return scaled_quantities

food_ingredients = {
    'Paneer Tikka': {
        'Paneer (Cottage Cheese)': '80 grams',
        'Curd (Yogurt)': '30 grams',
        'Ginger Garlic Paste': '5 grams',
        'Lemon Juice': '5 grams',
        'Red Chili Powder': '2 grams',
        'Garam Masala': '1 gram',
        'Turmeric Powder': '1 gram',
        'Cumin Powder': '1 gram',
        'Coriander Powder': '1 gram',
        
    },
    'Stuffed Mushrooms': {
        'Large Button Mushrooms': '2 pieces',
        'Cream Cheese': '20 grams',
        'Chopped Onions': '10 grams',
        'Garlic': '2 grams',
        'Spinach (Chopped)': '10 grams',
        'Mozzarella Cheese': '15 grams',
        
        
        'Olive Oil': '5 grams',
        'Italian Herbs': '1 gram'
    },
    'Mini Samosas': {
        'Samosa Pastry': '2 sheets',
        'Mashed Potatoes': '50 grams',
        'Green Peas': '10 grams',
        'Chopped Onions': '10 grams',
        'Ginger-Garlic Paste': '5 grams',
        'Cumin Seeds': '1 gram',
        'Red Chili Powder': '2 grams',
        'Garam Masala': '1 gram',
        'Fresh Coriander': '5 grams',
        
    },
    'Veg Spring Rolls': {
        'Spring Roll Sheets': '2 sheets',
        'Cabbage (Shredded)': '20 grams',
        'Carrot (Shredded)': '10 grams',
        'Bean Sprouts': '10 grams',
        'Capsicum (Shredded)': '10 grams',
        'Chopped Onions': '5 grams',
        'Ginger': '2 grams',
        'Soy Sauce': '5 grams',
        
        'Oil for frying': '15 grams'
    },
    'Hara Bhara Kabab': {
        'Boiled Spinach': '30 grams',
        'Boiled Potatoes': '40 grams',
        'Paneer': '20 grams',
        'Green Chilies': '1 piece',
        'Ginger-Garlic Paste': '3 grams',
        'Corn Flour': '5 grams',
        'Bread Crumbs': '5 grams',
        'Cumin Powder': '1 gram',
        'Garam Masala': '1 gram',
        
    },
    'Corn Chaat': {
        'Sweet Corn (Boiled)': '50 grams',
        'Chopped Tomatoes': '10 grams',
        'Chopped Onions': '10 grams',
        'Chopped Cucumber': '10 grams',
        'Coriander Leaves': '5 grams',
        'Chaat Masala': '1 gram',
        'Black Salt': '1 gram',
        'Lemon Juice': '5 grams',
        'Pomegranate Seeds': '5 grams',
        'Green Chilies': '1 piece'
    },
    'Mini Quiches': {
        'Shortcrust Pastry (Mini Size)': '1 piece',
        'Eggs': '1 piece',
        'Cream': '15 grams',
        'Milk': '15 grams',
        'Cheese (Cheddar or Mozzarella)': '20 grams',
        'Chopped Onions': '5 grams',
        'Chopped Bell Peppers': '5 grams',
        
        
        'Herbs (Thyme or Oregano)': '1 gram'
    },
    'Sev Puri': {
        'Puri': '5 pieces',
        'Sev (Thin Fried Noodles)': '20 grams',
        'Boiled Potatoes (Mashed)': '30 grams',
        'Chopped Onions': '10 grams',
        'Chopped Tomatoes': '10 grams',
        'Tamarind Chutney': '5 grams',
        'Green Chutney': '5 grams',
        'Chaat Masala': '1 gram',
        'Coriander Leaves': '5 grams',
        
    },
    'Veg Seekh Kebab': {
        'Mixed Vegetables (Carrot, Peas, Corn)': '40 grams',
        'Paneer': '30 grams',
        'Breadcrumbs': '10 grams',
        'Onion': '10 grams',
        'Ginger-Garlic Paste': '3 grams',
        'Green Chilies': '1 piece',
        'Red Chili Powder': '1 gram',
        'Garam Masala': '1 gram',
        'Coriander Leaves': '5 grams',
        'Oil for grilling': '5 grams'
    },
    'Hummus and Pita': {
        'Chickpeas (Boiled)': '50 grams',
        'Tahini (Sesame Paste)': '10 grams',
        'Olive Oil': '5 grams',
        'Garlic': '1 gram',
        'Lemon Juice': '5 grams',
        
        'Cumin Powder': '1 gram',
        'Pita Bread': '1 small piece (30-40 grams)',
        'Paprika': '1 gram',
        'Fresh Parsley': '2 grams'
    },
    'Dhokla': {
        'Gram Flour (Besan)': '40 grams',
        'Curd (Yogurt)': '20 grams',
        'Eno Fruit Salt': '1 gram',
        'Ginger Paste': '3 grams',
        'Green Chilies (Chopped)': '1 piece',
        
        'Turmeric Powder': '1 gram',
        'Mustard Seeds': '1 gram',
        'Cumin Seeds': '1 gram',
        'Fresh Coriander': '5 grams'
    },
    'Bruschetta': {
        'Bread Slices (Ciabatta or Baguette)': '2 small slices',
        'Chopped Tomatoes': '20 grams',
        'Chopped Basil': '5 grams',
        'Olive Oil': '5 grams',
        'Garlic': '1 clove (chopped)',
        'Balsamic Vinegar': '2 grams',
        
        
        'Parmesan Cheese': '5 grams',
        'Oregano': '1 gram'
    },
    'Onion Bhaji': {
        'Onions (Thinly Sliced)': '50 grams',
        'Chickpea Flour (Besan)': '30 grams',
        'Rice Flour': '10 grams',
        'Baking Powder': '1 gram',
        'Chopped Green Chilies': '1 piece',
        'Chopped Fresh Coriander': '5 grams',
        'Cumin Seeds': '1 gram',
        'Turmeric Powder': '1 gram',
        'Red Chili Powder': '2 grams',
        
    },
    'Bhel Puri': {
        'Puffed Rice': '30 grams',
        'Sev': '10 grams',
        'Chopped Tomatoes': '10 grams',
        'Chopped Onions': '10 grams',
        'Tamarind Chutney': '5 grams',
        'Green Chutney': '5 grams',
        'Pomegranate Seeds': '5 grams',
        'Chaat Masala': '1 gram',
        'Fresh Coriander': '5 grams',
        'Lemon Juice': '5 grams'
    },
    'Papdi Chaat': {
        'Papdi (Crispy Crackers)': '6 pieces',
        'Boiled Potatoes': '30 grams',
        'Chickpeas (Boiled)': '20 grams',
        'Yogurt': '20 grams',
        'Tamarind Chutney': '5 grams',
        'Green Chutney': '5 grams',
        'Chaat Masala': '1 gram',
        'Fresh Coriander': '5 grams',
        'Pomegranate Seeds': '5 grams',
        
    },
    'Aloo Tikki': {
        'Boiled Potatoes': '50 grams',
        'Chopped Onions': '10 grams',
        'Green Chilies': '1 piece',
        'Ginger-Garlic Paste': '3 grams',
        'Cumin Powder': '1 gram',
        'Red Chili Powder': '2 grams',
        
        'Bread Crumbs': '10 grams',
        'Fresh Coriander': '5 grams',
        'Oil for frying': '10 grams'
    }
}
@app.route('/')
def index():
    return render_template('index.html')  # Default main page

@app.route('/about')
def about():
    return render_template('about.html')  # About page

@app.route('/ml_model')
def ml_model():
    return render_template('ML-model.html')  # Render the ML model input page


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect inputs for Model 1
        event_duration = float(request.form.get('event_duration'))
        weekend = request.form.get('weekend')
        holiday = request.form.get('holiday')
        weather = request.form.get('weather')
        location_type = request.form.get('location_type')
        expected_diners_range = request.form.get('expected_diners_range')

        # Prepare input data for Model 1
        input_data_example = {
            'Event Duration (hours)': event_duration,
            'Weekend': weekend,
            'Holiday': holiday,
            'Weather': weather,
            'Location Type': location_type,
            'Expected Diners Range': expected_diners_range,
        }

        # Predict diners using Model 1
        predicted_diners = predict_diners(input_data_example)

        # Collect inputs for Model 2
        event = int(request.form.get('event'))
        season = int(request.form.get('season'))
        time_of_day = int(request.form.get('time_of_day'))
        menu_items_input = request.form.get('menu_items')
        menu_items = [item.strip() for item in menu_items_input.split(',')]

        # Predict quantities using Model 2
        scaled_quantities, no_unit_qt = predict_quantities_for_menu(
            predicted_diners, event, season, time_of_day, menu_items
        )

        # Prepare results
        results = {
            'predicted_diners': round(float(predicted_diners), 2),  # Convert to native float
            'scaled_quantities': {key: str(value) for key, value in scaled_quantities.items()},  # Ensure serialization
            'ingredients': {},
            'aggregated_ingredients': {}         
        }

        # Initialize a dictionary to store aggregated ingredients
        aggregated_ingredients = {}
        repeated_cnt_no=0
        # Calculate ingredient quantities
        for food_item, value in no_unit_qt.items():
            if food_item in food_ingredients:
                # Individual ingredients for each food item
                results['ingredients'][food_item] = {
                    ingredient: f"{round(float(value * int(q.split()[0])), 2)} {q.split()[1]}"
                    for ingredient, q in food_ingredients[food_item].items()
                }

                # Aggregate ingredient quantities
                for ingredient, quantity in food_ingredients[food_item].items():
                    q = quantity.split(sep=" ")
                    ingredient_quantity = value * int(q[0])

                    if ingredient in aggregated_ingredients:
                        aggregated_ingredients[ingredient][0] += ingredient_quantity
                        repeated_cnt_no+=1
                    else:
                        aggregated_ingredients[ingredient] = [ingredient_quantity, q[1]]   
                  
            else:
                results['ingredients'][food_item] = "Not in ingredients dictionary"
            

        results['repeated_count'] = f"{repeated_cnt_no} Items"

        # Add aggregated ingredients to results
        results['aggregated_ingredients'] = {
            ingredient: f"{round(float(quantity[0]), 2)} {quantity[1]}"
            for ingredient, quantity in aggregated_ingredients.items()
        }

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/surplus_management')
def surplus_management():
    return render_template('Surplus.html')  # Surplus management page

@app.route('/help')
def help():
    return render_template('Help.html')  # Help page

@app.route('/profile')
def profile():
    return render_template('profile.html')  # Profile page

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Dashboard page

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')  # Pricing page


if __name__ == '__main__':
    app.run(debug=True)
