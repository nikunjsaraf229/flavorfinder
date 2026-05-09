from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import model

app = FastAPI(title="Food Recommendation API")

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FoodItem(BaseModel):
    id: int
    name: str
    category: str
    ingredients: str
    diet: str
    description: str
    image: str

class RecommendationRequest(BaseModel):
    food_name: Optional[str] = None
    preference: Optional[str] = None

@app.get("/", response_model=dict)
def read_root():
    return {"message": "Welcome to the Food Recommendation API"}

@app.get("/foods", response_model=List[FoodItem])
def get_all_foods():
    """Returns the list of all available foods in the dummy dataset."""
    return model.get_all_foods()

@app.post("/recommend", response_model=List[FoodItem])
def get_recommendations(req: RecommendationRequest):
    """
    Returns food recommendations based on a specific food item's name,
    or a general preference string.
    """
    if req.food_name:
        recs = model.get_recommendations(req.food_name)
        return recs
    elif req.preference:
        recs = model.recommend_by_preference(req.preference)
        return recs
    return []
