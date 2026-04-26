# Canadian Economic Pulse

An automated pipeline that fetches live Canadian inflation data from the Bank of Canada, stores it in a database, and generates an Excel report automatically.

---

## The Problem

Tracking Canadian inflation manually takes hours in Excel. This pipeline does it in seconds with one command.

---

## How It Works

Step 1 - fetch_data.py fetches live data from Bank of Canada API and saves it to a database

Step 2 - generate_report.py reads the database and creates an Excel report with insights

---

## Tech Used

- Python
- pandas
- SQLite
- requests
- openpyxl
- Git and GitHub

---

## How to Run It

Install the libraries:
pip install pandas requests openpyxl

Fetch the data:
python fetch_data.py

Generate the report:
python generate_report.py

---

## What the Report Shows

- Latest Canadian inflation rate
- Month over month change and trend
- 12 month average
- Highest and lowest rates in the dataset

---

## Built By

[Erfan Ashourifar]

Business and Data Analyst transitioning to Data Engineering

[https://www.linkedin.com/in/erfan-ashourifar/]