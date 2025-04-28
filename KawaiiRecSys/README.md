# 🎌 KawaiiRecSys - Anime Recommendation System

A hybrid anime recommendation system that combines collaborative filtering (SVD) and content-based approaches to provide personalized anime recommendations.

## 🏗️ Project Structure

```
KawaiiRecSys/
├── data/               # Data files (anime.csv, ratings.csv)
├── notebooks/          # Jupyter notebooks for exploration
├── src/               # Core recommendation logic
│   ├── __init__.py
│   ├── svd.py         # SVD-based collaborative filtering
│   └── hybrid.py      # Hybrid recommendation system
├── streamlit_app/     # Streamlit web application
│   ├── __init__.py
│   └── app.py         # Main application file
├── utils/             # Utility functions
│   ├── __init__.py
│   └── helpers.py     # Helper functions
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## 🚀 Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/KawaiiRecSys.git
cd KawaiiRecSys
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:
```bash
cd streamlit_app
streamlit run app.py
```

## 🎯 Features

- Hybrid recommendation system combining:
  - Collaborative filtering (SVD)
  - Content-based filtering
- Netflix-style UI with beautiful anime cards
- Genre-based color coding
- Adjustable recommendation weights
- Random anime quotes

## 🤖 How It Works

1. **Collaborative Filtering (SVD)**
   - Uses the Surprise library's SVD implementation
   - Learns user preferences from ratings data
   - Predicts ratings for unseen anime

2. **Content-Based Filtering**
   - Uses TF-IDF vectorization of anime genres
   - Calculates cosine similarity between anime
   - Recommends similar anime based on genre content

3. **Hybrid Approach**
   - Combines both methods using a weighted average
   - Adjustable alpha parameter (0.0 to 1.0)
   - Default: 60% collaborative, 40% content-based

## 📊 Data

The system uses two main datasets:
- `anime.csv`: Contains anime metadata (name, genre, etc.)
- `ratings.csv`: Contains user ratings for anime

## 🛠️ Development

- Use Jupyter notebooks in the `notebooks/` directory for exploration
- Add new features in the appropriate module
- Follow the existing project structure for consistency

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 