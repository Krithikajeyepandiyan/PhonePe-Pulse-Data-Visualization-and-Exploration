# import
import os
import json
import streamlit as st
import pandas as pd
import psycopg2
import requests
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu


# insurance file
def agg_ins():
    
    ins_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/aggregated/insurance/country/india/state/'

    agg_ins_list=os.listdir(ins_path)

    col={'States':[],'Year':[],'Quarter':[],'Insurance_Method':[],'Insurance_Count':[],'Insurance_Amount':[]   }

    for states in agg_ins_list:
        curr_state=ins_path+states+'/'
        agg_state_list= os.listdir(curr_state)

        for year in agg_state_list:
            curr_year=curr_state+year+'/'
            agg_year_list=os.listdir(curr_year)

            for file in agg_year_list:
                curr_file=curr_year+ file
                data=open(curr_file,'r')

                Agg1=json.load(data)

                for i in Agg1['data']['transactionData']:
                    method=i['name']
                    count=i['paymentInstruments'][0]['count']
                    amount=i['paymentInstruments'][0]['amount']
                    col['Insurance_Method'].append(method)
                    col['Insurance_Count'].append(count)
                    col['Insurance_Amount'].append(amount)
                    col['States'].append(states)
                    col['Year'].append(year)
                    col['Quarter'].append(int(file.strip('.json')))
                Agg_ins=pd.DataFrame(col)

                Agg_ins['States']= Agg_ins['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Agg_ins['States']=Agg_ins['States'].str.replace('-', ' ')
                Agg_ins['States']=Agg_ins['States'].str.title()
                Agg_ins['States']=Agg_ins['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')

                return Agg_ins
            
    Agg_ins=agg_ins()
            
#trans file
def agg_trans():
    
    trans_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/aggregated/transaction/country/india/state/'

    agg_trans_list=os.listdir(trans_path)

    col1={'States':[],'Year':[],'Quarter':[],'Transaction_Method':[],'Transaction_Count':[],'Transaction_Amount':[]   }

    for states in agg_trans_list:
        curr_state=trans_path+states+'/'
        agg_state_list=os.listdir(curr_state)

        for year in agg_state_list:
            curr_year= curr_state+ year+'/'
            agg_year_list=os.listdir(curr_year)

            for file in agg_year_list:
                curr_file= curr_year+file
                data=open(curr_file,'r')

                Agg2=json.load(data)

                for i in Agg2['data']['transactionData']:
                    method=i['name']
                    count=i['paymentInstruments'][0]['count']
                    amount=i['paymentInstruments'][0]['amount']
                    col1['Transaction_Method'].append(method)
                    col1['Transaction_Count'].append(count)
                    col1['Transaction_Amount'].append(amount)
                    col1['States'].append(states)
                    col1['Year'].append(year)
                    col1['Quarter'].append(int(file.strip('.json')))
                    
                Agg_trans=pd.DataFrame(col1)

                Agg_trans['States']= Agg_trans['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Agg_trans['States']=Agg_trans['States'].str.replace('-', ' ')
                Agg_trans['States']=Agg_trans['States'].str.title()
                Agg_trans['States']=Agg_trans['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')
                Agg_trans['Transaction_Amount']=Agg_trans['Transaction_Amount'].round()
                Agg_trans['Year']=Agg_trans['Year'].astype(int)

                return Agg_trans
        Agg_trans=agg_trans()

# user file
def agg_user():
    
    user_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/aggregated/user/country/india/state/'

    agg_user_list=os.listdir(user_path)

    col2= {'States':[],'Year':[],'Quarter':[],'Brands':[],'User_Count':[],'Percentage':[]   }

    for states in agg_user_list:
        curr_state=user_path+states+'/'
        agg_state_list=os.listdir(curr_state)

        for year in agg_state_list:
            curr_year=curr_state+year+'/'
            agg_year_list=os.listdir(curr_year)

            for file in agg_year_list:
                curr_file=curr_year+file
                data=open(curr_file,'r')

                Agg3=json.load(data)

                try:

                    for i in Agg3['data']['usersByDevice']:
                        brands=i['brand']
                        count=i['count']
                        percentage=i['percentage']
                        col2['Brands'].append(brands)
                        col2['User_Count'].append(count)
                        col2['Percentage'].append(percentage)
                        col2['States'].append(states)
                        col2['Year'].append(year)
                        col2['Quarter'].append(int(file.strip('.json')))
                except:
                    pass
                Agg_user=pd.DataFrame(col2)

                Agg_user['States']= Agg_user['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Agg_user['States']=Agg_user['States'].str.replace('-', ' ')
                Agg_user['States']=Agg_user['States'].str.title()
                Agg_user['States']=Agg_user['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')

                return Agg_user
            Agg_user=agg_user()

# map ins file
def map_ins():

    map_ins_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/map/insurance/hover/country/india/state/'

    map_ins_list=os.listdir(map_ins_path)

    col_map_1={'States':[],'Year':[],'Quarter':[],'District':[],'Insurance_Count':[],'Insurance_Amount':[]   }

    for states in map_ins_list:
        curr_state=map_ins_path+states+'/'
        map_state_list=os.listdir(curr_state)

        for year in map_state_list:
            curr_year=curr_state+year+'/'
            map_year_list=os.listdir(curr_year)

            for file in map_year_list:
                curr_file=curr_year+file
                data=open(curr_file,'r')

                Map1=json.load(data)

                for i in Map1['data']['hoverDataList']:
                    name=i['name']
                    count = i["metric"][0]["count"]
                    amount = i["metric"][0]["amount"]
                    col_map_1["District"].append(name)
                    col_map_1["Insurance_Count"].append(count)
                    col_map_1["Insurance_Amount"].append(amount)
                    col_map_1["States"].append(states)
                    col_map_1["Year"].append(year)
                    col_map_1["Quarter"].append(int(file.strip(".json")))

                Map_ins=pd.DataFrame(col_map_1)

                Map_ins['States']= Map_ins['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Map_ins['States']=Map_ins['States'].str.replace('-', ' ')
                Map_ins['States']=Map_ins['States'].str.title()
                Map_ins['States']=Map_ins['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')

                return Map_ins
            Map_ins=map_ins()

# map trans file
def map_trans():

    map_trans_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/map/transaction/hover/country/india/state/'

    map_trans_list=os.listdir(map_trans_path)

    col_map_2={'States':[],'Year':[],'Quarter':[],'District':[],'Transaction_Count':[],'Transaction_Amount':[]   }

    for states in map_trans_list:
        curr_state=map_trans_path+states+'/'
        map_state_list=os.listdir(curr_state)

        for year in map_state_list:
            curr_year=curr_state+year+'/'
            map_year_list=os.listdir(curr_year)

            for file in map_year_list:
                curr_file=curr_year+file
                data=open(curr_file,'r')

                Map2=json.load(data)

                for i in Map2['data']['hoverDataList']:
                    name=i['name']
                    count = i["metric"][0]["count"]
                    amount = i["metric"][0]["amount"]
                    col_map_2["District"].append(name)
                    col_map_2["Transaction_Count"].append(count)
                    col_map_2["Transaction_Amount"].append(amount)
                    col_map_2["States"].append(states)
                    col_map_2["Year"].append(year)
                    col_map_2["Quarter"].append(int(file.strip(".json")))

                Map_trans=pd.DataFrame(col_map_2)

                Map_trans['States']= Map_trans['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Map_trans['States']=Map_trans['States'].str.replace('-', ' ')
                Map_trans['States']=Map_trans['States'].str.title()
                Map_trans['States']=Map_trans['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')

                return Map_trans
            
        Map_trans=map_trans()

            
# map user file
def map_user():

    map_user_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/map/user/hover/country/india/state/'

    map_user_list=os.listdir(map_user_path)

    col_map_3={'States':[],'Year':[],'Quarter':[],'District':[],'Registered_User':[],'App_Opens':[]   }

    for states in map_user_list:
        curr_state=map_user_path+states+'/'
        map_state_list=os.listdir(curr_state)

        for year in map_state_list:
            curr_year=curr_state+year+'/'
            map_year_list=os.listdir(curr_year)

            for file in map_year_list:
                curr_file=curr_year+file
                data=open(curr_file,'r')

                Map3=json.load(data)

                for i in Map3["data"]["hoverData"].items():
                    district = i[0]
                    registereduser = i[1]["registeredUsers"]
                    appopens = i[1]["appOpens"]
                    col_map_3["District"].append(district)
                    col_map_3["Registered_User"].append(registereduser)
                    col_map_3["App_Opens"].append(appopens)
                    col_map_3["States"].append(states)
                    col_map_3["Year"].append(year)
                    col_map_3["Quarter"].append(int(file.strip(".json")))

                Map_user=pd.DataFrame(col_map_3)

                Map_user['States']= Map_user['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Map_user['States']=Map_user['States'].str.replace('-', ' ')
                Map_user['States']=Map_user['States'].str.title()
                Map_user['States']=Map_user['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')

                return Map_user
            Map_user=map_user
# map ins file
def top_ins():

    top_ins_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/top/insurance/country/india/state/'
    top_ins_list=os.listdir(top_ins_path)

    col_top_1={'States':[],'Year':[],'Quarter':[],'Pincode':[],'Insurance_Count':[],'Insurance_Amount':[]   }

    for states in top_ins_list:
        curr_state=top_ins_path+states+'/'
        top_state_list=os.listdir(curr_state)

        for year in top_state_list:
            curr_year=curr_state+year+'/'
            top_year_list=os.listdir(curr_year)

            for file in top_year_list:
                curr_file=curr_year+file
                data=open(curr_file,'r')

                Top1=json.load(data)

                for i in Top1["data"]["pincodes"]:
                    entityName = i["entityName"]
                    count = i["metric"]["count"]
                    amount = i["metric"]["amount"]
                    col_top_1["Pincode"].append(entityName)
                    col_top_1["Insurance_Count"].append(count)
                    col_top_1["Insurance_Amount"].append(amount)
                    col_top_1["States"].append(states)
                    col_top_1["Year"].append(year)
                    col_top_1["Quarter"].append(int(file.strip(".json")))

                Top_ins=pd.DataFrame(col_top_1)

                Top_ins['States']= Top_ins['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Top_ins['States']=Top_ins['States'].str.replace('-', ' ')
                Top_ins['States']=Top_ins['States'].str.title()
                Top_ins['States']=Top_ins['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')

                return Top_ins
            Top_ins=top_ins

# top trans file
def top_trans():

    top_trans_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/top/transaction/country/india/state/'

    top_trans_list=os.listdir(top_trans_path)

    col_top_2={'States':[],'Year':[],'Quarter':[],'Pincode':[],'Transaction_Count':[],'Transaction_Amount':[]   }

    for states in top_trans_list:
        curr_state=top_trans_path+states+'/'
        top_state_list=os.listdir(curr_state)

        for year in top_state_list:
            curr_year=curr_state+year+'/'
            top_year_list=os.listdir(curr_year)

            for file in top_year_list:
                curr_file=curr_year+file
                data=open(curr_file,'r')

                Top2=json.load(data)

                for i in Top2["data"]["pincodes"]:
                    entityName = i["entityName"]
                    count = i["metric"]["count"]
                    amount = i["metric"]["amount"]
                    col_top_2["Pincode"].append(entityName)
                    col_top_2["Transaction_Count"].append(count)
                    col_top_2["Transaction_Amount"].append(amount)
                    col_top_2["States"].append(states)
                    col_top_2["Year"].append(year)
                    col_top_2["Quarter"].append(int(file.strip(".json")))

                Top_trans=pd.DataFrame(col_top_2)

                Top_trans['States']= Top_trans['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Top_trans['States']=Top_trans['States'].str.replace('-', ' ')
                Top_trans['States']=Top_trans['States'].str.title()
                Top_trans['States']=Top_trans['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')  

                return Top_trans
            Top_trans=top_trans()         

# top user file
def top_user():

    top_user_path='C:/Users/Krithika J/OneDrive/Tài liệu/ds proj/youtube_proj/Phonepe_Proj/pulse/data/top/user/country/india/state/'

    top_user_list=os.listdir(top_user_path)

    col_top_3={'States':[],'Year':[],'Quarter':[],'Pincode':[],'Registered_User':[]   }

    for states in top_user_list:
        curr_state=top_user_path+states+'/'
        top_state_list=os.listdir(curr_state)

        for year in top_state_list:
            curr_year=curr_state+year+'/'
            top_year_list=os.listdir(curr_year)

            for file in top_year_list:
                curr_file=curr_year+file
                data=open(curr_file,'r')

                Top3=json.load(data)

                for i in Top3["data"]["pincodes"]:
                    name = i["name"]
                    registeredusers = i["registeredUsers"]
                    col_top_3["Pincode"].append(name)
                    col_top_3["Registered_User"].append(registeredusers)
                    col_top_3["States"].append(states)
                    col_top_3["Year"].append(year)
                    col_top_3["Quarter"].append(int(file.strip(".json")))

                Top_user=pd.DataFrame(col_top_3)

                Top_user['States']= Top_user['States'].str.replace('andaman-&-nicobar-islands','Andaman & Nicobar')
                Top_user['States']=Top_user['States'].str.replace('-', ' ')
                Top_user['States']=Top_user['States'].str.title()
                Top_user['States']=Top_user['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman & Diu')
                return Top_user
            Top_user=top_user

# Table creation-SQL Connection

mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Guvi2024",
    database="Phonepe_Data",
    port=5432
)
cursor = mydb.cursor()

# Agg ins
cursor.execute(' SELECT * FROM aggregated_insurance ')
mydb.commit()
table1=cursor.fetchall()

Agg_insurance=pd.DataFrame(table1, columns= ("States", "Year", "Quarter", "Insurance_Method", "Insurance_Count","Insurance_Amount"))    

# Agg trans
cursor.execute(' SELECT * FROM aggregated_transaction ')
mydb.commit()
table2=cursor.fetchall()

Agg_transaction=pd.DataFrame(table2, columns= ("States", "Year", "Quarter", "Transaction_Method", "Transaction_Count","Transaction_Amount")) 

# Agg user
cursor.execute(' SELECT * FROM aggregated_user ')
mydb.commit()
table3=cursor.fetchall()

Agg_user=pd.DataFrame(table3, columns= ("States", "Year", "Quarter", "Brands", "User_Count","Percentage")) 

# Trans ins
cursor.execute(' SELECT * FROM map_insurance ')
mydb.commit()
table4=cursor.fetchall()

Map_insurance=pd.DataFrame(table4, columns= ("States", "Year", "Quarter", "District", "Insurance_Count","Insurance_Amount"))    

# Agg trans
cursor.execute(' SELECT * FROM map_transaction ')
mydb.commit()
table5=cursor.fetchall()

Map_transaction=pd.DataFrame(table5, columns= ("States", "Year", "Quarter", "District", "Transaction_Count","Transaction_Amount")) 

# Agg user
cursor.execute(' SELECT * FROM aggregated_user ')
mydb.commit()
table6=cursor.fetchall()

Map_user=pd.DataFrame(table6, columns= ("States", "Year", "Quarter", "District","Registered_User","App_Opens" )) 


# Top ins
cursor.execute(' SELECT * FROM top_insurance ')
mydb.commit()
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7, columns= ("States", "Year", "Quarter", "Pincode", "Insurance_Count","Insurance_Amount"))    

# Top trans
cursor.execute(' SELECT * FROM top_transaction ')
mydb.commit()
table8=cursor.fetchall()

Top_transaction=pd.DataFrame(table8, columns= ("States", "Year", "Quarter", "Pincode", "Transaction_Count","Transaction_Amount")) 

# Top user
cursor.execute(' SELECT * FROM top_user ')
mydb.commit()
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9, columns= ("States", "Year", "Quarter", "Pincode","Registered_User" )) 

# plot

def Agg_ins_Y(df,year):
    iacy=df[df['Year']==year]
    iacy.reset_index(drop=True,inplace=True)

    iacyg=iacy.groupby('States')[["Insurance_Count","Insurance_Amount"]].sum()
    iacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
# Ins amt
        fig_amount=px.bar(iacyg,x ='States',y='Insurance_Amount',title=f'Insurance Amount - {year}',height=750,width=1000,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_amount)
    
    with col2:
# ins count
        fig_count=px.bar(iacyg,x ='States',y='Insurance_Count',title=f'Insurance Count- {year}',height=750,width=1000,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_name=[]
        for i in data['features']:
            states_name.append(i['properties']['ST_NM'])

        states_name.sort()

        fig1 = px.choropleth(   
            iacyg,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Insurance_Amount',
            color_continuous_scale='turbo',
            range_color = (iacyg['Insurance_Amount'].min(), iacyg['Insurance_Amount'].max()),
            title = f'Insurance Amount- {year}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            hover_data={"Insurance_Amount": True},
            height=750,width=1000
        )
        fig1.update_geos(visible=False)
        # Display the figure in notebook
        st.plotly_chart(fig1)

        # Create a choropleth map for India
        fig2 = px.choropleth(   
            iacyg,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Insurance_Count',
            color_continuous_scale='turbo',
            range_color = (iacyg['Insurance_Count'].min(), iacyg['Insurance_Count'].max()),
            title = f'Insurance Count- {year}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            hover_data={"Insurance_Count": True},
            height=750,width=1000
        )
        fig2.update_geos(visible=False)
        # Display the figure in notebook
        st.plotly_chart(fig2)

        return iacy



def Insurance_count_amount_Q(df,quarter):
    iacq=df[df['Quarter']==quarter]
    iacq.reset_index(drop=True,inplace=True)

    iacqg=iacq.groupby('States')[["Insurance_Count","Insurance_Amount"]].sum()
    iacqg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:

# Ins amt
        fig_q_amount=px.bar(iacqg,x ='States',y='Insurance_Amount',title=f'Insurance Amount for Quarter - {quarter}',height=750,width=1000,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_q_amount)
    with col2:
# ins count
        fig_q_count=px.bar(iacqg,x ='States',y='Insurance_Count',title=f'Insurance Count for Quarter- {quarter}',height=750,width=1000,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_name=[]
        for i in data['features']:
            states_name.append(i['properties']['ST_NM'])

        states_name.sort()

        fig5 = px.choropleth(   
            iacqg,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Insurance_Amount',
            color_continuous_scale='turbo',
            range_color = (iacqg['Insurance_Amount'].min(), iacqg['Insurance_Amount'].max()),
            title = f'Insurance Amount- {quarter}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            hover_data={"Insurance_Amount": True},
            height=750,width=1000
        )
        fig5.update_geos(visible=False)
        st.plotly_chart(fig5)

    with col2:
        # Create a choropleth map for India
        fig6 = px.choropleth(   
            iacqg,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Insurance_Count',
            color_continuous_scale='turbo',
            range_color = (iacqg['Insurance_Count'].min(), iacqg['Insurance_Count'].max()),
            title = f'Insurance count- {quarter}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            hover_data={"Insurance_Count": True},
            height=750,width=1000
        )
        fig6.update_geos(visible=False)
        st.plotly_chart(fig6)

        return iacq



def Transaction_count_amount_Y(df,year):
    tacy=df[df['Year']==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby('States')[["Transaction_Count","Transaction_Amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
# Ins amt
        fig_amount=px.bar(tacyg,x ='States',y='Transaction_Amount',title=f'Transaction Amount - {year}',height=750,width=1000,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_amount)
    with col2:
# ins count
        fig_count=px.bar(tacyg,x ='States',y='Transaction_Count',title=f'Transaction Count- {year}',height=750,width=1000,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_count)
    
    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_name=[]
        for i in data['features']:
            states_name.append(i['properties']['ST_NM'])

        states_name.sort()

        fig3 = px.choropleth(   
        tacyg,
        geojson=data,
        featureidkey='properties.ST_NM',
        locations='States',
        color='Transaction_Amount',
        color_continuous_scale='turbo',
        range_color = (tacyg['Transaction_Amount'].min(), tacyg['Transaction_Amount'].max()),
        title = f'Transaction Amount- {year}',
        fitbounds='locations',
        hover_name='States',  # Column to display on hover
        height=750,width=1000
        )
        fig3.update_geos(visible=False)
        # Display the figure in notebook
        st.plotly_chart(fig3)

        # Create a choropleth map for India
        fig4 = px.choropleth(   
            tacyg,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_Count',
            color_continuous_scale='turbo',
            range_color = (tacyg['Transaction_Count'].min(), tacyg['Transaction_Count'].max()),
            title = f'Transaction Count- {year}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            height=750,width=1000
        )
        fig4.update_geos(visible=False)
        # Display the figure in notebook
        st.plotly_chart(fig4)  # Use 'colab' renderer for Jupyter Notebooks
        return tacy

def Transaction_count_amount_Q(df,quarter):
    tacq=df[df['Quarter']==quarter]
    tacq.reset_index(drop=True,inplace=True)

    tacqg=tacq.groupby('States')[["Transaction_Count","Transaction_Amount"]].sum()
    tacqg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
# Ins amt
        fig_amount=px.bar(tacqg,x ='States',y='Transaction_Amount',title=f'Transaction Amount for Quarter- {quarter}',height=750,width=1000,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart (fig_amount)
# ins count
    with col2:
        fig_count=px.bar(tacqg,x ='States',y='Transaction_Count',title=f'Transaction Count for Quarter- {quarter}',height=750,width=1000,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_name=[]
        for i in data['features']:
            states_name.append(i['properties']['ST_NM'])

        states_name.sort()

        fig7 = px.choropleth(   
            tacqg,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_Amount',
            color_continuous_scale='turbo',
            range_color = (tacqg['Transaction_Amount'].min(), tacqg['Transaction_Amount'].max()),
            title = f'Transaction Amount- {quarter}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            height=750,width=1000
        )
        fig7.update_geos(visible=False)
        # Display the figure in notebook
        st.plotly_chart(fig7)
    with col2:
    # Create a choropleth map for India
        fig8 = px.choropleth(   
            tacqg,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_Count',
            color_continuous_scale='turbo',
            range_color = (tacqg['Transaction_Count'].min(), tacqg['Transaction_Count'].max()),
            title = f'Transaction count- {quarter}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            height=750,width=1000
        )
        fig8.update_geos(visible=False)
        st.plotly_chart(fig8) 

        return tacq


def Agg_trans_method(df,states):

    tacy=df[df['States']==states]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby('Transaction_Method')[['Transaction_Count','Transaction_Amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_bar1=px.bar(data_frame=tacyg,
                        names='Transaction_Method',
                        values='Transaction_Amount', 
                        width=600,
                        title=f'Transaction Amount-{states}',
                        hole=0.5,
                        color_discrete_sequence=px.colors.sequential.Bluered_r
                        )
        st.plotly_chart(fig_bar1) 
    
    with col2:
        fig_bar2=px.bar(data_frame=tacyg,
                        names='Transaction_Method',
                        values='Transaction_Count', 
                        width=600,
                        title=f'Transaction Count-{states}',
                        hole=0.5,
                        color_discrete_sequence=px.colors.sequential.Bluered_r
                        )
        st.plotly_chart(fig_bar2) 

def Agg_user_Y(df,states):
    uacy=df[df['States']==states]
    uacy.reset_index(drop=True, inplace=True)

    uacyg=uacy.groupby('Brands')[['User_Count','Percentage']].sum()
    uacyg.reset_index(inplace=True)
# User Count
    fig_bar3=px.bar(data_frame=uacyg,
                    names='Brands',
                    values='User_Count', 
                    width=600,
                    title=f'User Count-{states}',
                    hole=0.5,
                    color_discrete_sequence=px.colors.sequential.Emrld
                    )
    st.plotly_chart(fig_bar3)
# User Percentage
    fig_bar4=px.bar(data_frame=uacyg,
                    names='Brands',
                    values='Percentage', 
                    width=600,
                    title=f'User Percentage-{states}',
                    hole=0.5,
                    color_discrete_sequence=px.colors.sequential.Emrld
                    )
    st.plotly_chart(fig_bar4)

    return uacy

def Agg_user_Q(df,quarter):
    uacq=df[df['Quarter']==quarter]
    uacq.reset_index(drop=True, inplace=True)

    uacqg=uacq.groupby('Brands')[['User_Count','Percentage']].sum()
    uacqg.reset_index(inplace=True)
# User Count
    fig_pie1=px.pie(data_frame=uacqg,
                    names='Brands',
                    values='User_Count', 
                    hover_data= "Percentage",
                    width=600,
                    title=f'User Count Percentage-{quarter}',
                    hole=0.5,
                    color_discrete_sequence=px.colors.sequential.Emrld
                    )
    st.plotly_chart(fig_pie1)

    return uacq

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["User_Count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_bar5= px.bar(aguqyg, x= "Brands", y= "User_Count",width=1000)
    st.plotly_chart(fig_bar5)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Insurance_Count","Insurance_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Insurance_Amount",
                              width=600, height=500, title= f"{state} District Insurance Count",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)
        

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Insurance_Count",
                              width=600, height= 500, title= f"{state} District Insurance Count",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)


def map_insure_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "District", values= "Transaction_Amount",
                              width=600, height=500, title= f"{state} District Transaction Amount",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)
        
    with col2:
        fig_map_pie_1= px.pie(miysg, names= "District", values= "Transaction_Count",
                              width=600, height= 500, title= f"{state} District Transaction Count",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)
       

def map_user_plot_1(df, year):
    muy= df[df["Year"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["Registered_User", "App_Opens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1 = px.line(muyg, x="States", y=["Registered_User", "App_Opens"],
                              markers=True, width=1000, height=800,
                              title=f" Registered User And App_Opens in {year}",
                              color_discrete_sequence=px.colors.sequential.Viridis_r)

    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["Registered_User", "App_Opens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["Registered_User","App_Opens"], markers= True,
                                title= f" Quarter Wise Registered_User AND App_Opens {df['Years'].min()}, {quarter}",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("District")[["Registered_User", "App_Opens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "Registered_User",y= "District",orientation="h",
                                    title= f" Registered User in {state}",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "App_Opens", y= "District",orientation="h",
                                    title= f" App_Opens in {state}",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tuy= df[df["Year"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["Registered_User"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "Registered_User", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["Registered_User"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "Registered_User",barmode= "group",
                           width=1000, height= 800,color= "Registered_User",hover_data="Pincode",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

# questions

