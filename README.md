To check website in My Project Link: https://phonepe-pulse-transaction-insights-tfjxjjyc7svncslvgoms5y.streamlit.app/

**Problem Statement:**

Retrieve and analyze PhonePe transaction data from the PhonePe Pulse dataset, perform data transformation and stored it in a MySQL database, and build an interactive Streamlit dashboard using Plotly.

The dashboard provides real-time insights into transactions, users, devices, and insurance adoption across Indian states and districts. It includes multiple dropdowns and filters for better exploration.

The project aims to be efficient, secure, and user-friendly, offering actionable insights for business strategy.


**Technology Stack Used:**

Python

MySQL

Streamlit

SQLAlchemy

Plotly (Geo Visualization, Charts)

Visual Studio Code

**Installation:**

pip install pandas

pip install numpy

pip install os

pip install mysql.connector

pip install streamlit


**Import Libraries:**

import pandas as pd

import numpy as np

import json

import mysql.connector

import sqlalchemy

import streamlit as st

import plotly.express as px


**Approach:**

1. Data Extraction - Collected PhonePe Pulse datasets (transactions, users, devices, insurance).
Downloaded JSON files for structured processing.

2. Data Transformation - Converted raw JSON into pandas DataFrames.

3. Database Integration - Inserted data into MySQL tables for efficient querying.

4. Live Dashboard Development - Built with Streamlit + Plotly.Features interactive filters and dropdowns (≥10 options).Visualizations include Geo maps, bar charts, line charts, and data tables.

5. Database Integration with the Dashboard - Queried MySQL data using SQLAlchemy. Real-time fetching ensures accurate and updated information.

6. Visualization - Finally, create a dashboard using Streamlit, incorporating selection and dropdown options. Showcase the output through Geo visualization, bar charts, and a DataFrame table.


**Snapshort:**

Project Introduction:

<img width="1918" height="1018" alt="image" src="https://github.com/user-attachments/assets/3d5a7750-b53b-4052-8e27-8349367a3da0" />


Home - Transactions:

<img width="1918" height="1015" alt="image" src="https://github.com/user-attachments/assets/c1de7f57-986b-44cc-826a-f79159be7d75" />

<img width="1912" height="1025" alt="image" src="https://github.com/user-attachments/assets/2b88ae0b-3cd8-4dff-b039-0524d6d8b3d6" />


Home - Users:

<img width="1918" height="1021" alt="image" src="https://github.com/user-attachments/assets/f025af24-b879-40eb-9d88-7257e28b757e" />

<img width="1918" height="1013" alt="image" src="https://github.com/user-attachments/assets/5bf0e9e2-5dd7-4403-bdae-f3cca9198128" />


Analysis:

<img width="1918" height="1015" alt="image" src="https://github.com/user-attachments/assets/829cc2b3-090b-4b04-8028-961055c8a6bd" />

<img width="1918" height="852" alt="image" src="https://github.com/user-attachments/assets/ac820858-2c8e-4311-827c-f3c38bda5e43" />








