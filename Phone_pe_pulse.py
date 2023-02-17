import streamlit as st
st.title("Phone pe Pulse Data")
import mysql.connector as connect
import pandas as pd
import numpy as np
import json

from sqlalchemy import create_engine
import plotly.express as px

cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Bharatkori#1998",
  database='phone_pe'
)

print(cnx)
cursor = cnx.cursor()

# Define the SQL query to retrieve data from the "table
query = "SELECT * FROM agg_trans"

# Execute the SQL query and store the result in a Pandas dataframe
agg_tran = pd.read_sql(query, cnx)
#print(agg_tran)
agg_tran['State'] = agg_tran['State'].replace({'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunanchal Pradesh',
       'assam':'Assam', 'bihar':'Bihar', 'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa':'Goa', 'gujarat': 'Gujarat',
       'haryana':'Haryana','himachal-pradesh':'Himachal Pradesh', 'jammu-&-kashmir':'Jammu & Kashmir', 'jharkhand':'Jharkhand',
       'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh',
       'maharashtra':'Maharashtra', 'manipur':'Manipur', 'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland',
       'odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim',
       'tamil-nadu': 'Tamil Nadu', 'telangana':'Telangana', 'tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh',
       'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'})



fig = px.choropleth(
agg_tran,
geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
featureidkey='properties.ST_NM',
locations='State',
hover_data=['Transacion_amount'],
color='Transacion_count',
color_continuous_scale='orRd'
)

fig.update_geos(fitbounds="locations")
fig.show()
