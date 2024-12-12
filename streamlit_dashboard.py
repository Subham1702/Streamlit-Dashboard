# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 19:30:49 2024

@author: mital
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
file_path = r"C:\Users\mital\Documents\Project-4 (Analysis of Bonus Allocation)\PySpark\new_data.csv"  
data = pd.read_csv(file_path)

# Streamlit App Title
st.title("Advanced Bonus Allocation Analysis Dashboard")
st.markdown("""
This dashboard provides insights into the bonus allocation process, focusing on fairness, ROI, and customer segmentation.
Explore interactive visualizations to uncover actionable strategies for optimizing resource allocation.
""")

# Sidebar Filters
st.sidebar.header("Filters")

# Dropdown for Country
selected_country = st.sidebar.selectbox("Select Country:", options=['All'] + list(data['country'].unique()))

# to ensure Age_Group column is of category dtype
data['Age_Group'] = data['Age_Group'].astype('category')

# Dropdown for Age Group
selected_age_group = st.sidebar.selectbox(
    "Select Age Group:",
    options=['All'] + list(data['Age_Group'].cat.categories.astype(str))
)

# Categorize 'Income_level' into predefined categories
bins = [0, 30000, 70000, 150000]  # Define the ranges
labels = ['Low Income', 'Middle Income', 'High Income']  # Define the categories
data['Income_Category'] = pd.cut(data['income_level'], bins=bins, labels=labels, include_lowest=True)

# Dropdown for Income Category
income_categories = ['All'] + list(data['Income_Category'].cat.categories.astype(str))
selected_category = st.sidebar.selectbox("Select Income Category:", income_categories)

# Applying dynamic filters 
filtered_data = data.copy()

if selected_country != 'All':
    filtered_data = filtered_data[filtered_data['country'] == selected_country]

if selected_age_group != 'All':
    filtered_data = filtered_data[filtered_data['Age_Group'] == selected_age_group]

if selected_category != 'All':
    filtered_data = filtered_data[filtered_data['Income_Category'] == selected_category]

# KPI Section
st.subheader("Key Performance Indicators (KPIs)")
avg_bonus_roi = filtered_data['Bonus_ROI'].mean()
avg_clv = filtered_data['Customer_Lifetime_Value'].mean()
variance_bonus_distribution = filtered_data['Amount_of_Bonuses_Received'].var()

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric("Average Bonus ROI", f"{avg_bonus_roi:.2f}")
kpi_col2.metric("Average Customer Lifetime Value (CLV)", f"{avg_clv:.2f}")
kpi_col3.metric("Variance in Bonus Distribution", f"{variance_bonus_distribution:.2f}")

# Visualization: Bonus ROI by Country
st.subheader("Bonus ROI by Country")
roi_by_country = filtered_data.groupby('country')['Bonus_ROI'].mean().reset_index()
fig_roi_country = px.bar(roi_by_country, x='country', y='Bonus_ROI', color='Bonus_ROI',
                         title="Average Bonus ROI by Country",
                         labels={'Bonus_ROI': 'Average Bonus ROI'})
st.plotly_chart(fig_roi_country)

# Visualization: Customer Segmentation
st.subheader("Customer Segmentation by Income Level")
income_analysis = filtered_data.groupby('income_level').agg(
    Avg_Bonus=('Amount_of_Bonuses_Received', 'mean'),
    Avg_Wagering_Increase=('Increase_in_wagering_after_Bonus', 'mean')
).reset_index()
fig_income = px.bar(income_analysis, x='income_level', y=['Avg_Bonus', 'Avg_Wagering_Increase'],
                    title="Customer Segmentation: Bonus and Wagering Trends",
                    labels={'value': 'Average Amount'},
                    barmode='group')
st.plotly_chart(fig_income)

# Visualization: Fairness Analysis
st.subheader("Fairness in Bonus Distribution")
fairness_data = filtered_data.groupby('Should_Receive_Bonus').agg(
    Avg_Bonus=('Amount_of_Bonuses_Received', 'mean'),
    Variance=('Amount_of_Bonuses_Received', 'var')
).reset_index()
fig_fairness = px.pie(fairness_data, values='Avg_Bonus', names='Should_Receive_Bonus',
                      title="Fairness in Bonus Distribution",
                      labels={'Should_Receive_Bonus': 'Bonus Eligibility'})
st.plotly_chart(fig_fairness)

# Visualization: Cost-to-Revenue Ratio
st.subheader("Cost-to-Revenue Ratio")
cost_to_revenue = filtered_data['Amount_of_Bonuses_Received'] / filtered_data['Revenue_from_Bonuses']
fig_cost_revenue = px.histogram(cost_to_revenue, nbins=20,
                                title="Distribution of Cost-to-Revenue Ratio",
                                labels={'value': 'Cost-to-Revenue Ratio'})
st.plotly_chart(fig_cost_revenue)

# Closing Notes
st.markdown("""
**Key Insights:**
- Leverage the high Bonus ROI regions to prioritize bonus spending.
- Customize bonus strategies for income-specific customer groups.
- Ensure fairness by reducing variance in bonus distribution.
""")

st.markdown("---")
st.markdown("""
### Let's Connect!  
Developed by [Subhankar Deb](https://www.linkedin.com/in/subhankar-deb-ab1248188/).  
Feel free to reach out for collaboration or discussions!
""")
