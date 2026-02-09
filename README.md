# 🎬 Movie Recommender System | ML + Streamlit

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![API](https://img.shields.io/badge/TMDB_API-01B4E4?style=for-the-badge&logo=the-movie-database&logoColor=white)](https://www.themoviedb.org/documentation/api)

An interactive web application that leverages **Machine Learning** to provide personalized movie suggestions. By analyzing content metadata, the system helps users discover their next favorite film with ease.

---

## 🚀 Key Features
* **Smart Recommendations:** Instant suggestions based on content-based filtering logic.
* **Visual Richness:** Real-time movie posters and details fetched via **TMDB API**.
* **Genre Discovery:** Dedicated section to browse the **Top 10 movies** by genre.
* **Enhanced UX:** Featuring a **Light/Dark mode** toggle and a custom navigation bar.
* **Live Deployment:** Hosted on **Streamlit Cloud** for instant accessibility.

---

## 🧠 Technical Workflow
1.  **Model Training:** Developed in **Google Colab** using **Pandas** for feature engineering.
2.  **Recommendation Logic:** Utilizes **Cosine Similarity** to compute mathematical distance between movie attributes (cast, plot, genres).
3.  **Frontend:** Built with **Streamlit** to create a responsive and intuitive dashboard.
4.  **Integration:** Connects to the **TMDB API** for dynamic metadata and high-quality imagery.

---

## 🛠️ Tech Stack
* **Language:** Python
* **ML Libraries:** Scikit-learn, Pandas, NumPy
* **Web Framework:** Streamlit
* **Environment:** Google Colab, VS Code
* **API:** The Movie Database (TMDB)

---

## 📂 Project Structure
```bash
├── app.py                  # Flask Web Server
├── Movie_rec.ipynb         # Model Building & Preprocessing
├── movies_df.pkl           # Processed Dataset
├── similarity.pkl          # Similarity Matrix
├── utils/                  # Debugging & Verification Scripts
└── templates/              # UI Layouts

---

## ⚙️ Installation & Setup
```bash
# Clone the repository
git clone [https://github.com/Rudra-Gupta15/movie-recommender.git](https://github.com/Rudra-Gupta15/movie-recommender.git)

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
