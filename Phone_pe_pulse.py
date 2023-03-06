import pandas as pd
import streamlit as st
import mysql.connector
import plotly.express as px
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)



#Establishing the connection to Database
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
agg_tran = pd.read_sql(query, cnx)
query = "SELECT * FROM agg_user"
agg_user = pd.read_sql(query, cnx)
query = "SELECT * FROM map_trans"
map_tran = pd.read_sql(query, cnx)
query = "SELECT * FROM map_user"
map_user = pd.read_sql(query, cnx)
query = "SELECT * FROM top_trans"
top_tran = pd.read_sql(query, cnx)
query = "SELECT * FROM top_user"
top_user = pd.read_sql(query, cnx)

agg_tran.to_csv(r'C:\Users\Barry\Desktop\projects\2.csv')

#Change Dataframe column state by jeojson states
agg_tran['State'] = agg_tran['State'].replace({'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunanchal Pradesh',
       'assam':'Assam', 'bihar':'Bihar', 'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa':'Goa', 'gujarat': 'Gujarat',
       'haryana':'Haryana','himachal-pradesh':'Himachal Pradesh', 'jammu-&-kashmir':'Jammu & Kashmir', 'jharkhand':'Jharkhand',
       'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh',
       'maharashtra':'Maharashtra', 'manipur':'Manipur', 'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland',
       'odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim',
       'tamil-nadu': 'Tamil Nadu', 'telangana':'Telangana', 'tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh',
       'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'})


########################################################################################################################
#Dash board
#st.set_page_config(layout="wide")
st.title(':blue[PhonePe Pulse Data Analysis(2018-2022):]')
c1, c2 = st.columns((1, 1))
c1.subheader('           State wise transactions        ')
fig= px.choropleth(
agg_tran,
geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
featureidkey='properties.ST_NM',
locations='State',
hover_data=['Transacion_amount'],
color='Transacion_count',
color_continuous_scale='orRd'
)

fig.update_geos(fitbounds="locations")
c1.plotly_chart(fig)


#Top 10 districts with highest transactions
c2.subheader("              Transactions By Districts")
t =top_tran.groupby(['Transacion_by_district']).agg({'Transacion_amount': 'sum','Transacion_count':'sum'}).sort_values('Transacion_amount', ascending=False)
t=t.reset_index()
t=t.head(10)
fig = px.bar(t, x="Transacion_by_district", y="Transacion_amount",color='Transacion_count',title="Top Ten Districts,")
fig.update_traces(width=0.5)
c2.write(fig)



c3, c4 = st.columns((1, 1))
#Type of ftransactions taken place
c3.subheader("Transaction types")
k=agg_tran.groupby(['Transacion_type']).agg({'Transacion_amount':'sum','Transacion_count':'sum'})
k=k.reset_index(level=([0]))
fig = px.pie(k, values='Transacion_amount', names='Transacion_type',color_discrete_sequence=px.colors.sequential.RdBu)
c3.write(fig)


st.title("Transaction data Filter ")

st.write(
    """This application helps us to filter the respective input data
    """
)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        df (pd.DataFrame): Original dataframe
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df


df = pd.read_csv(
    r"C:\Users\Barry\Desktop\projects\2.csv"
)
Data = st.dataframe(filter_dataframe(df))
print(Data)


st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

# And the root-level secrets are also accessible as environment variables:

import os

st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["db_username"],
)
