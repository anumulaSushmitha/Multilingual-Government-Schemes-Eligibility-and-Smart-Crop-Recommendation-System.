 Multilingual Government Schemes Eligibility & Smart Crop Recommendation System

![Python](https://img.shields.io/badge/Python-3.9-blue)
![ML](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green)
![Framework](https://img.shields.io/badge/Framework-Flask-orange)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey) 

The Farmer Portal is a cloud-based intelligent system that helps farmers make informed decisions by combining:

* 🌱 Crop Recommendation using Machine Learning
* 🏛️ Government Scheme Eligibility Detection
* 🤖 Multilingual Chatbot Assistance

 Features

 Crop Recommendation System

* Predicts best crops based on:

  * Nitrogen (N), Phosphorus (P), Potassium (K)
  * Temperature, Humidity, pH, Rainfall
* Model used: **Random Forest**
* Accuracy: **~99.5%**
 🏛️ Government Scheme Eligibility
* Determines eligibility using:
  * Age
  * Income
  * Landholding
* Suggests schemes like:

  * PM-KISAN
  * Crop Insurance
  * Soil Health Card
 Multilingual Chatbot
* Provides real-time answers
* Supports:
  * English
  * Telugu
  * Hindi
 PDF Generation
* Generates downloadable reports including:
  * Recommended crops
  * Eligible schemes
 Problem Statement
Farmers face difficulties in:
* Choosing suitable crops
* Accessing government schemes
* Using non-user-friendly systems

 Existing systems lack **integration, multilingual support, and real-time assistance**.
Objectives

* Build a **smart farmer support system**
* Use **ML for accurate crop prediction**
* Provide **scheme eligibility recommendations**
* Enable **real-time chatbot interaction**
* Support **multiple languages**
 System Architecture
 Input Layer
math
X = [N, P, K, T, H, pH, R]
Modules

* Crop Recommendation → Random Forest
* Scheme Eligibility → Rule-Based Logic
* Chatbot → Query Processing

Output
(Crop Recommendation, Eligible Schemes, PDF, Chatbot Response)
 Dataset
Input Features:

* Nitrogen (N)
* Phosphorus (P)
* Potassium (K)
* Temperature
* Humidity
* Soil pH
* Rainfall
 Output:

* Crop Label (Recommended Crop)
 Methodology

| Model               | Accuracy |
| ------------------- | -------- |
| Random Forest       | 99.5% ✅  |
| Naive Bayes         | 99.2%    |
| Decision Tree       | 98.6%    |
| Logistic Regression | 94.5%    |

**Random Forest selected for best performance**
 Results

* ✅ High prediction accuracy
* ✅ Accurate scheme eligibility
* ✅ Real-time chatbot responses
* ✅ PDF report generation
 Tech Stack

* **Frontend:** HTML, CSS
* **Backend:** Python (Flask)
* **Machine Learning:** Scikit-learn
* **Database:** SQLite
 Project Structure

├── app.py
├── templates/
├── static/
├── model/
├── dataset/
├── chatbot/
├── utils/
└── README.md
 Conclusion

The system:

*  Provides accurate crop recommendations
*  Identifies suitable government schemes
*  Offers multilingual support

 A **complete decision support system for farmers**
 Future Scope

*  Mobile application
*  Voice-based chatbot
*  Weather API integration
*  More language support
 References

* Dahiphale et al. (2025) – Smart Farming
* Rajpoot et al. (2025) – Scheme Recommendation
* Bhargavi & Jagannathan (2023) – Crop ML System
* Géron (2022) – Machine Learning
* Mitchell (1997) – Machine Learning
 How to Run
bash
# Clone repository
git clone https://github.com/your-username/your-repo-name.git

# Go to project folder
cd your-repo-name

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
Acknowledgment

Developed as part of an academic project to support **smart farming and farmer decision-making**.
 Support
If you like this project, give it a ⭐ on GitHub!
If you want, I can next:
* Create **requirements.txt**
* Generate **GitHub repo description**
* Help you **upload step-by-step to GitHub**

Just tell me 👍
