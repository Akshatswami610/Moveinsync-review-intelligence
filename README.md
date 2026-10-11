# 
# MoveInSync Review Intelligence

A Python-based data analysis project to investigate Google Play reviews of the MoveInSync employee commute app, identify potential causes of low ratings, and recommend data-driven product improvements.

Developed as part of the **MoveInSync Forward Deployed Engineer (Intern to FTE) candidate assignment**.

## Problem Statement

MoveInSync helps employees commute to and from work. The reliability of its mobile app affects booking, pickup information, vehicle tracking, and communication.

The objective of this project is to analyze public app reviews, understand recurring user complaints, identify areas for further investigation, and recommend which improvements should be prioritized.

## Objectives

- Analyze the distribution of star ratings.
- Calculate the average rating and percentage of low-rated reviews.
- Identify recurring complaint themes in 1- and 2-star reviews.
- Track rating patterns over time.
- Generate charts and CSV reports using Python.
- Translate findings into actionable product recommendations.

## Tech Stack

- **Python** — analysis and automation
- **Pandas** — data cleaning and analysis
- **Matplotlib** — data visualization
- **Regular expressions** — keyword-based complaint classification
- **PyCharm** — local development environment
- **Git and GitHub** — version control and project publishing

## Project Structure

```text
moveinsync-review-intelligence/
├── data/
│   └── moveinsync_reviews.csv
├── outputs/
│   ├── complaint_themes.png
│   ├── monthly_trends.png
│   ├── rating_distribution.png
│   ├── monthly_trends.csv
│   ├── negative_reviews_analysis.csv
│   ├── rating_summary.csv
│   └── theme_analysis.csv
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

The raw review dataset and individual review-text exports are excluded from version control. The structure above documents the local project; those excluded files may not be present in the public repository.

## Dataset

The analysis uses a CSV dataset of publicly available Google Play reviews collected using Python.

The dataset includes fields such as:

- `score` — review star rating
- `content` — review text
- `at` — review date
- `reviewId` — review identifier, when available

The analysis uses the collected sample rather than the complete population of MoveInSync users. Results should be interpreted within that limitation.

## Methodology

### 1. Data cleaning
- Load the review CSV using Pandas.
- Remove duplicate reviews when review identifiers are available.
- Convert rating and date fields into appropriate data types.
- Exclude invalid ratings and rows without valid dates.

### 2. Rating analysis
- Calculate the number and percentage of reviews for each star rating.
- Calculate the average rating of the collected sample.
- Measure the proportion of 1- and 2-star reviews.
- Generate a rating distribution chart.

### 3. Complaint analysis
- Focus on 1- and 2-star reviews.
- Use keyword-based rules to assign potential complaint categories.
- Count review mentions for each category.
- Export categorized reviews and a complaint frequency chart.

Categories include:

- Booking and scheduling
- GPS, ETA, and tracking
- App stability
- Login and OTP
- Notifications
- Transport and support
- UI and usability

A single review can match multiple categories.

### 4. Trend analysis
- Group reviews by month.
- Calculate monthly average ratings and low-rating percentages.
- Generate a chart showing average rating trends.

### 5. Recommendation development
Use the results to identify high-priority issues for further investigation. Recommendations should consider complaint frequency, severity, confidence in the evidence, and potential impact on the employee commute experience.

## Generated Outputs

| File | Description |
|---|---|
| `rating_summary.csv` | Review counts and percentages by star rating |
| `theme_analysis.csv` | Preliminary complaint category counts |
| `monthly_trends.csv` | Monthly rating and low-rating statistics |
| `negative_reviews_analysis.csv` | Low-rated reviews with assigned themes |
| `rating_distribution.png` | Star rating distribution chart |
| `complaint_themes.png` | Complaint category frequency chart |
| `monthly_trends.png` | Average rating trend chart |

## How to Run Locally

### Prerequisites

- Python 3.10 or later
- Git
- A local copy of the review CSV

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/moveinsync-review-intelligence.git
cd moveinsync-review-intelligence
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Add the dataset

Place your CSV at:

```text
data/moveinsync_reviews.csv
```

The raw dataset is not included in the public repository. Obtain or provide your own permitted copy before running the analysis.

### 5. Run the analysis

```bash
python main.py
```

The script creates the `outputs/` directory if needed and saves the analysis tables and charts there.

## Initial Findings and Interpretation

The initial analysis of the collected sample examines rating distribution, recurring complaint themes, and monthly trends.

The keyword-based classification is exploratory. Category counts should be checked against actual review text before being used to rank product priorities.

The results can help identify potential areas to investigate, including booking reliability, vehicle tracking, app stability, transport operations, login, notifications, and usability.

Specific recommendations should be finalized only after reviewing the generated outputs and validating the most important findings.

## Limitations

- The collected reviews are not necessarily representative of all app users.
- Public reviews can overrepresent unusually positive or negative experiences.
- Keyword classification can miss relevant complaints or assign incorrect categories.
- Categories overlap, so their counts should not be added together.
- Review text alone cannot establish the underlying technical or operational cause.
- Monthly comparisons may be affected by small sample sizes or incomplete months.
- Internal booking, tracking, notification, crash, and support data would be needed to validate root causes.

## Potential Next Steps

- Manually validate a sample of classified reviews.
- Improve classification using sentiment analysis or an AI-assisted workflow.
- Track emerging complaint themes through a recurring review-analysis process.
- Correlate public review themes with internal product and operations metrics.
- Measure whether implemented fixes reduce relevant complaints and improve recent ratings.

## Author

**Akshat Swami**
LinkedIn: Add your LinkedIn profile URL

---

This project was created to demonstrate data analysis, scripting, problem-solving, and evidence-based product recommendations for the MoveInSync FDE candidate assignment.
