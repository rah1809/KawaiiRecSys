import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .svd import train_svd_model, get_svd_recommendations
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.helpers import enrich_with_images

def get_content_based_recommendations(
    anime_df: pd.DataFrame,
    selected_anime: List[str],
    top_n: int = 10
) -> pd.DataFrame:
    """Get content-based recommendations based on selected anime."""
    # Create TF-IDF matrix for genres
    tfidf = TfidfVectorizer(stop_words='english')
    genre_matrix = tfidf.fit_transform(anime_df['genre'].fillna(''))
    
    # Get indices of selected anime
    selected_indices = anime_df[anime_df['name'].isin(selected_anime)].index
    
    if len(selected_indices) == 0:
        return pd.DataFrame()  # Return empty DataFrame if no matches
    
    # Calculate average similarity to selected anime
    selected_similarity = np.mean(cosine_similarity(genre_matrix[selected_indices], genre_matrix), axis=0)
    
    # Create recommendations DataFrame
    recommendations = anime_df.copy()
    recommendations['content_score'] = selected_similarity
    
    # Remove selected anime from recommendations
    recommendations = recommendations[~recommendations['name'].isin(selected_anime)]
    
    return recommendations.sort_values('content_score', ascending=False).head(top_n)

def hybrid_recommend(
    user_id: int,
    selected_anime: List[str],
    ratings_df: pd.DataFrame,
    anime_df: pd.DataFrame,
    top_n: int = 10,
    alpha: float = 0.6
) -> pd.DataFrame:
    """Get hybrid recommendations combining SVD and content-based approaches."""
    # Get SVD recommendations
    svd_model = train_svd_model(ratings_df)
    svd_recs = get_svd_recommendations(svd_model, user_id, anime_df, top_n)
    
    # Get content-based recommendations
    content_recs = get_content_based_recommendations(anime_df, selected_anime, top_n)
    
    if content_recs.empty:
        return svd_recs
    
    # Merge recommendations
    hybrid_recs = pd.merge(
        svd_recs[['anime_id', 'name', 'genre', 'predicted_rating']],
        content_recs[['anime_id', 'content_score']],
        on='anime_id',
        how='outer'
    ).fillna(0)
    
    # Normalize scores
    hybrid_recs['predicted_rating'] = (hybrid_recs['predicted_rating'] - hybrid_recs['predicted_rating'].min()) / \
                                     (hybrid_recs['predicted_rating'].max() - hybrid_recs['predicted_rating'].min())
    hybrid_recs['content_score'] = (hybrid_recs['content_score'] - hybrid_recs['content_score'].min()) / \
                                  (hybrid_recs['content_score'].max() - hybrid_recs['content_score'].min())
    
    # Calculate final score
    hybrid_recs['final_score'] = alpha * hybrid_recs['predicted_rating'] + (1 - alpha) * hybrid_recs['content_score']
    
    # Sort by final score and get top N
    hybrid_recs = hybrid_recs.sort_values('final_score', ascending=False).head(top_n)
    
    # Add image URLs using Jikan API
    hybrid_recs = enrich_with_images(hybrid_recs)
    
    return hybrid_recs 