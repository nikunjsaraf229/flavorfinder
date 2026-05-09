import React, { useState, useEffect } from 'react';
import { Search, Loader2, Sparkles } from 'lucide-react';
import FoodCard from './components/FoodCard';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';

function App() {
  const [query, setQuery] = useState('');
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // Fetch initial recommended foods or all foods
  useEffect(() => {
    fetchAllFoods();
  }, []);

  const fetchAllFoods = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/foods`);
      const data = await response.json();
      setFoods(data.slice(0, 8)); // Just show a few initially
    } catch (error) {
      console.error("Error fetching foods:", error);
    }
    setLoading(false);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      fetchAllFoods();
      setHasSearched(false);
      return;
    }

    setLoading(true);
    setHasSearched(true);
    try {
      const response = await fetch(`${API_URL}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ preference: query }),
      });
      const data = await response.json();
      setFoods(data);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
    setLoading(false);
  };

  const handleTagClick = (tag) => {
    setQuery(tag);
    // Need to use the tag value directly here because state update is async
    setLoading(true);
    setHasSearched(true);
    fetch(`${API_URL}/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ preference: tag }),
    })
      .then(res => res.json())
      .then(data => {
        setFoods(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  return (
    <div className="app-container">
      <header>
        <h1>FlavorFinder</h1>
        <p className="subtitle">AI-Powered Food Recommendations</p>
      </header>

      <section className="search-section">
        <form className="search-bar-container" onSubmit={handleSearch}>
          <input
            type="text"
            className="search-input"
            placeholder="What are you craving? (e.g., spicy, creamy, pasta)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" className="search-button">
            {loading ? <Loader2 className="spin" size={20} /> : <Search size={20} />}
          </button>
        </form>

        <div className="popular-tags">
          <span className="tag" onClick={() => handleTagClick("Italian pasta")}>Italian Pasta</span>
          <span className="tag" onClick={() => handleTagClick("Spicy curry")}>Spicy Curry</span>
          <span className="tag" onClick={() => handleTagClick("Healthy vegan")}>Healthy Vegan</span>
          <span className="tag" onClick={() => handleTagClick("Classic American")}>Classic American</span>
        </div>
      </section>

      <section className="results-section">
        <h2 className="section-title">
          <Sparkles className="card-icon" /> 
          {hasSearched ? 'Your Recommendations' : 'Popular Dishes'}
        </h2>
        
        {loading ? (
          <div className="loading-spinner">
            <Loader2 className="spin" size={40} />
            <p style={{marginTop: '1rem'}}>Finding the best flavors for you...</p>
          </div>
        ) : foods.length > 0 ? (
          <div className="grid-container">
            {foods.map(food => (
              <FoodCard key={food.id} food={food} />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <Search size={48} style={{opacity: 0.5, marginBottom: '1rem'}} />
            <h3>No matches found</h3>
            <p>Try searching for different ingredients or cuisines.</p>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
