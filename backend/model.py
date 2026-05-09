import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Generate Dummy Data
def get_dummy_data():
    data = [
        {"id": 1, "name": "Spaghetti Carbonara", "category": "Italian", "ingredients": "pasta, egg, pancetta, cheese, black pepper", "diet": "Non-Vegetarian", "description": "Classic creamy pasta dish with pancetta.", "image": "/images/pasta_dish.png"},
        {"id": 2, "name": "Margherita Pizza", "category": "Italian", "ingredients": "pizza dough, tomatoes, mozzarella, fresh basil, olive oil", "diet": "Vegetarian", "description": "Simple and classic Italian pizza.", "image": "/images/pizza_dish.png"},
        {"id": 3, "name": "Chicken Tikka Masala", "category": "Indian", "ingredients": "chicken, yogurt, tomato, onion, garlic, ginger, garam masala, cream", "diet": "Non-Vegetarian", "description": "Spicy and creamy curry with roasted chicken chunks.", "image": "/images/curry_dish.png"},
        {"id": 4, "name": "Palak Paneer", "category": "Indian", "ingredients": "spinach, paneer cheese, onion, tomato, garlic, garam masala", "diet": "Vegetarian", "description": "Creamy spinach curry with soft paneer cubes.", "image": "/images/curry_dish.png"},
        {"id": 5, "name": "Sushi Rolls", "category": "Japanese", "ingredients": "sushi rice, nori, fresh salmon, avocado, cucumber", "diet": "Pescatarian", "description": "Fresh and healthy bite-sized sushi rolls.", "image": "/images/sushi_dish.png"},
        {"id": 6, "name": "Ramen", "category": "Japanese", "ingredients": "ramen noodles, pork broth, pork belly, soft boiled egg, scallions", "diet": "Non-Vegetarian", "description": "Rich and comforting noodle soup.", "image": "/images/pasta_dish.png"},
        {"id": 7, "name": "Tacos al Pastor", "category": "Mexican", "ingredients": "corn tortillas, marinated pork, pineapple, onion, cilantro", "diet": "Non-Vegetarian", "description": "Savory and sweet Mexican street tacos.", "image": "/images/taco_dish.png"},
        {"id": 8, "name": "Guacamole & Chips", "category": "Mexican", "ingredients": "avocados, lime, onion, cilantro, jalapeno, tortilla chips", "diet": "Vegan", "description": "Fresh and tangy avocado dip.", "image": "/images/taco_dish.png"},
        {"id": 9, "name": "Vegan Buddha Bowl", "category": "Healthy", "ingredients": "quinoa, roasted sweet potato, chickpeas, kale, tahini dressing", "diet": "Vegan", "description": "Nutritious and balanced plant-based bowl.", "image": "/images/salad_dish.png"},
        {"id": 10, "name": "Grilled Salmon", "category": "Healthy", "ingredients": "salmon fillet, lemon, olive oil, asparagus, garlic", "diet": "Pescatarian", "description": "Light and protein-packed seafood dish.", "image": "/images/steak_dish.png"},
        {"id": 11, "name": "Beef Burger", "category": "American", "ingredients": "beef patty, burger bun, cheddar cheese, lettuce, tomato, onion", "diet": "Non-Vegetarian", "description": "Juicy and classic American cheeseburger.", "image": "/images/burger_dish.png"},
        {"id": 12, "name": "Caesar Salad", "category": "American", "ingredients": "romaine lettuce, croutons, parmesan cheese, caesar dressing", "diet": "Vegetarian", "description": "Crisp and garlicky classic salad.", "image": "/images/salad_dish.png"},
        {"id": 13, "name": "Ribeye Steak", "category": "American", "ingredients": "ribeye steak, butter, garlic, rosemary, asparagus", "diet": "Non-Vegetarian", "description": "Perfectly grilled rich and buttery steak.", "image": "/images/steak_dish.png"},
        {"id": 14, "name": "Vegetarian Pad Thai", "category": "Thai", "ingredients": "rice noodles, tofu, peanuts, bean sprouts, lime, tamarind", "diet": "Vegetarian", "description": "Sweet and tangy Thai noodle dish.", "image": "/images/pasta_dish.png"},
        {"id": 15, "name": "Tom Yum Soup", "category": "Thai", "ingredients": "shrimp, lemongrass, galangal, kaffir lime leaves, chili", "diet": "Pescatarian", "description": "Hot and sour aromatic Thai soup.", "image": "/images/curry_dish.png"},
        {"id": 16, "name": "Mushroom Risotto", "category": "Italian", "ingredients": "arborio rice, mushrooms, parmesan, white wine, broth, butter", "diet": "Vegetarian", "description": "Creamy and earthy Italian rice dish.", "image": "/images/pasta_dish.png"},
        {"id": 17, "name": "Fish and Chips", "category": "British", "ingredients": "cod, potatoes, beer batter, tartar sauce, lemon", "diet": "Pescatarian", "description": "Classic crispy fried fish with thick-cut chips.", "image": "/images/burger_dish.png"},
        {"id": 18, "name": "Chana Masala", "category": "Indian", "ingredients": "chickpeas, onion, tomato, ginger, garlic, spices", "diet": "Vegan", "description": "Hearty and spiced chickpea curry.", "image": "/images/curry_dish.png"},
    ]
    return pd.DataFrame(data)

df = get_dummy_data()

# Create a combined feature for recommendation
df['combined_features'] = df['category'] + " " + df['ingredients'] + " " + df['diet']

# 2. Train the Model (TF-IDF & Cosine Similarity)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# 3. Recommendation Function
def get_recommendations(food_name: str, num_recommendations: int = 4):
    try:
        # Get the index of the food that matches the name
        idx = df.index[df['name'].str.lower() == food_name.lower()].tolist()[0]
    except IndexError:
        return [] # Food not found
    
    # Get pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the foods based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the scores of the most similar foods (excluding itself)
    sim_scores = sim_scores[1:num_recommendations+1]
    
    # Get the food indices
    food_indices = [i[0] for i in sim_scores]
    
    # Return the top most similar foods
    return df.iloc[food_indices].to_dict('records')

def get_all_foods():
    return df.to_dict('records')

def recommend_by_preference(preference: str, num_recommendations: int = 4):
    # If user just types a generic preference instead of a specific food
    user_tfidf = tfidf.transform([preference])
    sim_scores = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    
    # Get indices sorted by score
    food_indices = sim_scores.argsort()[::-1][:num_recommendations]
    
    return df.iloc[food_indices].to_dict('records')
