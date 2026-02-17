# Student Dashboard

## Overview
The Student Dashboard is a Python-based application designed to help educators manage and analyze student performance in courses. This repository contains scripts for data cleaning, feature engineering, and analytics, as well as a test dataset of student assignments.

This repository was created for GHW: Data in February 2026. It is intended to be used for educational purposes. This project welcomes suggestions for improvements. 

## Features
- **Data Cleaning**: Scripts to preprocess and clean the dataset for analysis.
- **Analytics**: Tools to analyze student performance and generate insights.
- **Visualization**: Visualizations for better understanding of student data.

## Dataset
The dataset used in this project is located in the `data/` directory and includes:
- **computer_science_teacher_dataset_2026.csv**: Contains student IDs, names, class periods, assignment names, types, dates, scores, maximum scores, and submission statuses.

## Project Structure
```
StudentDashboard/
├── data/                          # Dataset files
│   └── computer_science_teacher_dataset_2026.csv
├── src/                           # Python scripts for data processing
│   ├── clean_data.py
│   ├── features.py
├── requirements.txt               # Python dependencies
├── dashboard.py                   # Streamlit dashboard
└── README.md                      # Project documentation
```

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/StudentDashboard.git
   cd StudentDashboard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Dashboard**
   ```bash
   streamlit run dashboard.py
   ```

## Contributing
Suggestions for improvements are welcome! Please feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
