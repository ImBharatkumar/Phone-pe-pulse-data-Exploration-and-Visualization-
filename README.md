# PhonePe Pulse Data Extraction and Visualization

This repository contains code to extract and visualize PhonePe Pulse data. PhonePe Pulse is a dashboard provided by PhonePe that allows merchants to track their business performance over time.

# Getting Started
To get started with using the code in this repository, you will need to have access to PhonePe Pulse. 

# copy code
git clonehttps://github.com/PhonePe/pulse.git (you can download all data related to transactions).


# Usage
The code in this repository contains a Python ipynb file phonepe pe pulse.ipynb that demonstrates how to extract and visualize data from the PhonePe Pulse CSV file.
then extracted data is saved into databases using sql.

A phone_pe_pulse.py file is used to extract data from database and used that data to visualize the insights from data.
1) Indian map is drawn using plotly library which shows state wise transactions and transaction counts by hovering over it.
2) A bar plot for showing top 10 Districts with high amount of transactions.
3) A pie chart for transaction categories.
4) Finally a Data table with applied filter through which we can filter Year ,State, and  Quarter wise data and it diplays accordingly.


# Copy code
python phonepe_pulse.py
The script will read the data from the CSV file in the data directory and generate two plots:


# Contributing
If you would like to contribute to this repository, please feel free to submit a pull request. We welcome contributions from the community.

