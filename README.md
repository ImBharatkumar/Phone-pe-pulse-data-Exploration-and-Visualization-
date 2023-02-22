# Phone-pe-pulse-data-Exploration-and-Visualization-
Through this project i have explored and visualized the Phone pe pulse github data.

#Steps involved.

#1) Clone  https://github.com/PhonePe/pulse.git
*import necessary libraries listed in requirements.txt
*from pulse folder import/load json files of all states and convert json files into usefull dataframes.
*convert DataFrame into csv file.
'''
#Agg_transaction_data

path=r"C:\Users\Barry\Desktop\projects\capstone2\pulse\data\aggregated\transaction\country\india\state/"
Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<---------------------------------------------------

#This is to extract the data's to create a dataframe
clm={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}
for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Transacion_type'].append(Name)
              clm['Transacion_count'].append(count)
              clm['Transacion_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
df=pd.DataFrame(clm)
#convert df to csv
df.to_csv(r'C:\Users\Barry\Desktop\projects\capstone2\agg_trans.csv',index=False)
'''



#2) Push Data into MySQL database.
*Establish connection between MySQL using python.
*Create a Database and Table with respective columns in dataframe. 
*Write query to push data into Table.
'''
engine = create_engine('mysql+mysqlconnector://root:Bharatkori#1998@127.0.0.1:3306/phone_pe')

config = {
   'user': 'root',
   'password': 'Bharatkori#1998',
   'host': 'localhost',
   'database': 'phone_pe',
   'raise_on_warnings': True
 }

## Connect to the database
cnx = mysql.connector.connect(**config)

## Check if the connection is successful
if cnx.is_connected():
  print("Connection to MySQL database established.")
else:
  print("Connection to MySQL database failed.")
  
  ## create a table name and store the dataframe
df.to_sql(name='agg_trans', con=engine, if_exists='replace', index=False)'''

#3)Retrive data for Visualization.
*From MySQL retreive data.
*COnvert it into dataframe.
'''## Execute the SQL query and store the result in a Pandas dataframe
cursor = cnx.cursor()
query = "SELECT * FROM agg_trans"
agg_tran = pd.read_sql(query, cnx)
'''

#4)Visualization.
*Download indian jeojson file and use it with plotly Choropleth visualize statewise transactions.
*Using retrieved DataFrame visualize the data.
*refer("phone_pe_pulse.py")



