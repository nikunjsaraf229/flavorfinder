import React from 'react';
import { Utensils, Leaf, Beef, Fish } from 'lucide-react';

export default function FoodCard({ food }) {
  // Determine icon based on diet
  const getDietIcon = (diet) => {
    switch (diet.toLowerCase()) {
      case 'vegetarian':
      case 'vegan':
      case 'healthy':
        return <Leaf className="card-icon" size={24} />;
      case 'pescatarian':
        return <Fish className="card-icon" size={24} />;
      case 'non-vegetarian':
      default:
        return <Beef className="card-icon" size={24} />;
    }
  };

  return (
    <div className="food-card">
      <div className="card-image-placeholder">
        {getDietIcon(food.diet)}
      </div>
      <div className="card-content">
        <div className="card-category">{food.category}</div>
        <h3 className="card-title">{food.name}</h3>
        <p className="card-description">{food.description}</p>
        <div className="card-footer">
          <span className="diet-badge">{food.diet}</span>
          <span className="ingredients-preview" title={food.ingredients}>
            {food.ingredients}
          </span>
        </div>
      </div>
    </div>
  );
}
