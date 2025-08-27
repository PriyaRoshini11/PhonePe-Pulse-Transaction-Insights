To check website in My Project Link: http://192.168.1.7:8501

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
Home - Transactions:

<img width="1918" height="1022" alt="image" src="https://github.com/user-attachments/assets/2516ad65-cb34-4b76-9970-e3bdc92e54bf" />

<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/7f9f5177-d4a0-47ac-9fcc-64cf4ad5be33" />

Home - Users:

<img width="1918" height="1012" alt="image" src="https://github.com/user-attachments/assets/0f165fb8-352f-4086-8ce2-fa8d038528b8" />

<img width="1918" height="1007" alt="image" src="https://github.com/user-attachments/assets/220a98ce-9dc7-4176-aaec-fa8261d07c00" />

Analysis:

<img width="1918" height="1012" alt="image" src="https://github.com/user-attachments/assets/f8c34bf1-4dd7-4804-8742-cc2d40be30c2" />

<img width="1918" height="1006" alt="image" src="https://github.com/user-attachments/assets/f014dca9-8cfc-4db1-8a16-a164c2b7a21b" />







