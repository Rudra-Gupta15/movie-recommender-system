# 🎬 Movie Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A **Content-Based Movie Recommendation System** built using Python and Flask. This application analyzes movie metadata (genres, keywords, and overviews) to suggest films similar to a user's selection using mathematical similarity scoring.

---

## 🚀 Key Features
* **Instant Recommendations:** Suggests similar movies based on content metadata.
* **Vectorized Processing:** Uses `CountVectorizer` for efficient text-to-vector transformation.
* **Similarity Engine:** Powered by **Cosine Similarity** for high-accuracy matching.
* **Web Interface:** Interactive UI built with Flask for a seamless user experience.
* **Validation Tools:** Custom utility scripts for debugging dataset and genre consistency.

---

## 🧠 How It Works
1. **Data Engineering:** Features like genres, cast, and keywords are merged into a single "tags" column.
2. **Text Vectorization:** The system converts text tags into a 5000-dimensional vector space.
3. **Similarity Matrix:** It calculates the cosine distance between vectors:
   $$similarity = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$
4. **Deployment:** The model is serialized using `Pickle` for fast loading within the Flask app.

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Data Science:** Pandas, NumPy, Scikit-learn
- **Frontend:** HTML5, CSS3
- **DevOps:** Pickle (Serialization)

---

## 📂 Project Structure
```bash
├── app.py                  # Flask Web Server
├── Movie_rec.ipynb         # Model Building & Preprocessing
├── movies_df.pkl           # Processed Dataset
├── similarity.pkl          # Similarity Matrix
├── utils/                  # Debugging & Verification Scripts
└── templates/              # UI Layouts
