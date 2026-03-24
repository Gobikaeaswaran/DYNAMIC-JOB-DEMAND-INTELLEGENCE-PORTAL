# DYNAMIC JOB DEMAND INTELLIGENCE PORTAL (DJDIP)

An interactive, real-time oriented dashboard for visualizing job market trends, salaries, and skill gaps using Streamlit and Plotly.

## 🚀 Overview

DJDIP provides a comprehensive view of the current job market, enabling users to slice data by location, job title, experience level, and specific technical skills. It features dynamic visualizations and a "what-if" analysis tool to help job seekers understand their market value based on their current skill set.

## ✨ Features

- **Interactive Market Filters:** Filter by posting date, experience range, location, and job title.
- **KPI Dashboard:** Real-time metrics for open jobs, median salary, average experience, and skill variety.
- **Visual Analytics:**
  - **Salary Trends:** Weekly median salary trends with job count overlays.
  - **Job Density Heatmap:** Visualizes job availability across different locations and roles.
  - **Skill Gap Radar:** Compares market demand for top skills against the user's personal skill set.
- **What-if Analysis:** Instant estimation of job matches and salary ranges based on custom skill selections.
- **High Performance:** Uses Streamlit's caching mechanism for instant response times.

## 🛠️ Technology Stack

- **Frontend/App Framework:** [Streamlit](https://streamlit.io/)
- **Data Visualization:** [Plotly Express](https://plotly.com/python/plotly-express/) & [Plotly Graph Objects](https://plotly.com/python/graph-objects/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)

## 🏃 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Gobikaeaswaran/DYNAMIC-JOB-DEMAND-INTELLEGENCE-PORTAL.git
   cd DYNAMIC-JOB-DEMAND-INTELLEGENCE-PORTAL
   ```

2. Install dependencies:
   ```bash
   pip install streamlit pandas numpy plotly
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📊 Data Source
This demo currently uses a cached synthetic data generator that simulates 3,000+ job postings with realistic salary ranges and skill requirements. The architecture is designed to be easily swappable with a live database or API backend.

## 📝 License
This project is open-source and available under the MIT License.
