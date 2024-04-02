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

def Insurance_count_amount_Y(df,year):
    iacy=df[df['Year']==year]
    iacy.reset_index(drop=True,inplace=True)

    iacyg=iacy.groupby('States')[["Insurance_Count","Insurance_Amount"]].sum()
    iacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
# Ins amt
        fig_amount=px.bar(iacyg,x ='States',y='Insurance_Amount',title=f'Insurance Amount - {year}',height=600,width=600,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_amount)
    
    with col2:
# ins count
        fig_count=px.bar(iacyg,x ='States',y='Insurance_Count',title=f'Insurance Count- {year}',height=600,width=600,
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
            height=600,width=600
        )
        fig1.update_geos(visible=False)
        # Display the figure in notebook
        st.plotly_chart(fig1)
        with col2:
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
                height=600,width=600
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
        fig_q_amount=px.bar(iacqg,x ='States',y='Insurance_Amount',title=f'Insurance Amount for Quarter - {quarter}',height=600,width=600,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_q_amount)
    with col2:
# ins count
        fig_q_count=px.bar(iacqg,x ='States',y='Insurance_Count',title=f'Insurance Count for Quarter- {quarter}',height=600,width=600,
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
            title = f'Insurance Amount for Quarter- {quarter}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            hover_data={"Insurance_Amount": True},
            height=600,width=600
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
            title = f'Insurance Amount for Quarter- {quarter}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            hover_data={"Insurance_Count": True},
            height=600,width=600
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
        fig_amount=px.bar(tacyg,x ='States',y='Transaction_Amount',title=f'Transaction Amount - {year}',height=600,width=600,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart(fig_amount)
    with col2:
# ins count
        fig_count=px.bar(tacyg,x ='States',y='Transaction_Count',title=f'Transaction Count- {year}',height=600,width=600,
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
        height=600,width=600
        )
        fig3.update_geos(visible=False)
        # Display the figure in notebook
        st.plotly_chart(fig3)
    with col2:
        # Create a choropleth map for India
        fig4 = px.choropleth(   
            tacyg,
            geojson=data,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_Count',
            color_continuous_scale='turbo',
            range_color = (tacyg['Transaction_Count'].min(), tacyg['Transaction_Count'].max()),
            title = f'Transaction Count - {year}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            height=600,width=600
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
        fig_amount=px.bar(tacqg,x ='States',y='Transaction_Amount',title=f'Transaction Amount for Quarter- {quarter}',height=600,width=600,
                        color_discrete_sequence=px.colors.sequential.Brwnyl)
        st.plotly_chart (fig_amount)
# ins count
    with col2:
        fig_count=px.bar(tacqg,x ='States',y='Transaction_Count',title=f'Transaction Count for Quarter- {quarter}',height=600,width=600,
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
            title = f'Transaction Amount For Quarter- {quarter}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            height=600,width=600
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
            title = f'Transaction count For Quarter- {quarter}',
            fitbounds='locations',
            hover_name='States',  # Column to display on hover
            height=600,width=600
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

        fig_pie1=px.pie(data_frame=tacyg,
                        names='Transaction_Method',
                        values='Transaction_Amount', 
                        width=600,
                        title=f'Transaction Amount-{states}',
                        hole=0.5,
                        color_discrete_sequence=px.colors.sequential.Bluered_r
                        )
        st.plotly_chart(fig_pie1) 
    
    with col2:
        fig_pie2=px.pie(data_frame=tacyg,
                        names='Transaction_Method',
                        values='Transaction_Count', 
                        width=600,
                        title=f'Transaction Count-{states}',
                        hole=0.5,
                        color_discrete_sequence=px.colors.sequential.Bluered_r
                        )
        st.plotly_chart(fig_pie2) 

def Agg_user_Y(df,year):
    uacy=df[df['Year']==year]
    uacy.reset_index(drop=True, inplace=True)

    uacyg=uacy.groupby('Brands')[['User_Count']].sum()
    uacyg.reset_index(inplace=True)
# User Count
    fig_line_1= px.bar(uacyg, x="Brands",y= "User_Count", title=f" BRANDS AND USER COUNT-{year}",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)
    return uacy

def Agg_user_Q(df,quarter):
    uacq=df[df['Quarter']==quarter]
    uacq.reset_index(drop=True, inplace=True)

    uacqg=uacq.groupby('Brands')[['User_Count','Percentage']].sum()
    uacqg.reset_index(inplace=True)
# User Count
    fig_pie_1= px.pie(data_frame=uacq, names= "Brands", values="User_Count", hover_data= "Percentage",
                      width=1000,title=f"USER COUNT PERCENTAGE FOR QUARTER {quarter}",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)
    
    return uacq

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["User_Count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_bar5= px.bar(aguqyg, x= "Brands", y= "User_Count", width=1000)
    st.plotly_chart(fig_bar5)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Insurance_Count","Insurance_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Insurance_Amount",
                              width=600, height=500, title= f"{state} District Insurance Amount",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)
        

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Insurance_Count",
                              width=600, height= 500, title= f"{state} District Insurance Count",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)


def map_insure_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Insurance_Count","Insurance_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Insurance_Amount",
                              width=600, height=500, title= f"{state} District Insurance Amount",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)
        
    with col2:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Insurance_Count",
                              width=600, height= 500, title= f"{state} District Insurance Count",
                              color_discrete_sequence= px.colors.sequential.Mint)
        st.plotly_chart(fig_map_bar_1)


def map_trans_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Transaction_Amount",
                              width=600, height=500, title= f"{state} District Transaction Amount",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)
        

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Transaction_Count",
                              width=600, height= 500, title= f"{state} District Transaction Count",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_trans_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Transaction_Amount",
                              width=600, height=500, title= f"{state} District Transaction Amount",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)
        

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Transaction_Count",
                              width=600, height= 500, title= f"{state} District Transaction Count",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_user_plot_1(df, year):
    muy= df[df["Year"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["Registered_User", "App_Opens"]].sum()
    muyg.reset_index(inplace= True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_plot_1 = px.line(muyg, x="States", y=["Registered_User"],
                                markers=True, width=1000, height=800,
                                title=f" Registered User And App_Opens in {year}",
                                color_discrete_sequence=px.colors.sequential.Viridis_r)

        st.plotly_chart(fig_map_user_plot_1)
    with col2:
        fig_map_user_plot_1 = px.line(muyg, x="States", y=["App_Opens"],
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

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["Registered_User"], markers= True,
                                    title= f" Quarter Wise Registered_User  {df['Year'].min()}, {quarter}",
                                    width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)
    with col2:
        fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["App_Opens"], markers= True,
                                    title= f" Quarter Wise  App_Opens {df['Year'].min()}, {quarter}",
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
# 1.Which state has the highest number of transaction counts in a specific year and quarter?
def ques1():
    q1=Agg_transaction[['Transaction_Method', 'Transaction_Amount']]
    t1=q1.groupby('Transaction_Method')['Transaction_Amount'].sum().sort_values(ascending=False)
    df1=pd.DataFrame(t1).reset_index()

    fig_q1 = px.bar(df1, x= "Transaction_Method", y= "Transaction_Amount", title=" MAXIMUM TRANSACTION AMOUNT BY TRANSACTION METHOD",
                color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        template='plotly_dark')
    fig_q1.show(renderer='colab')
    return st.plotly_chart(fig_q1)

    
# 2.Which transaction method is most commonly used in a specific state during a certain year and quarter?
def qeus2():
    q2=Agg_transaction[['Transaction_Method', 'Transaction_Count']]
    t2=q2.groupby('Transaction_Method')['Transaction_Count'].sum().sort_values(ascending=False)
    df2=pd.DataFrame(t2).reset_index()

    fig_q2 = px.bar(df2, x= "Transaction_Method", y= "Transaction_Count", title=" MAXIMUM TRANSACTION COUNT BY TRANSACTION METHOD",
                color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        template='plotly_dark')
    return st.plotly_chart(fig_q2)

# 3.Which brand has the highest user count  
def ques3():
    q3=Agg_user[['Brands', 'User_Count']]
    t3=q3.groupby('Brands')['User_Count'].sum().sort_values(ascending=False)
    df3=pd.DataFrame(t3).reset_index()

    fig_q3 = px.bar(df3, x= "Brands", y= "User_Count", title="USER COUNT BY BRANDS ",
                color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        template='plotly_dark')
    return st.plotly_chart(fig_q3)

# 4	transaction
def ques4():
    q4= Map_user[["States", "App_Opens"]]
    t4= q4.groupby("States")["App_Opens"].sum().sort_values(ascending=False)
    df4= pd.DataFrame(t4).reset_index().tail(10)

    fig_q4= px.bar(df4, x= "States", y= "App_Opens", title="LOWEST 10 STATES WITH APP_OPENS",
            color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_q4)

# 5.lowest transaction amount and state
def ques5():
    q5= Agg_transaction[["States", "Transaction_Amount"]]
    t5= q5.groupby("States")["Transaction_Amount"].sum().sort_values(ascending= False)
    df5= pd.DataFrame(t5).reset_index().tail(10)

    fig_q5= px.bar(df5, x= "States", y= "Transaction_Amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_q5)
# 6.districts with highest transaction amount
def ques6():
    q6= Agg_transaction[["District", "Transaction_Amount"]]
    t6= q6.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=False)
    df6= pd.DataFrame(t6).head(10).reset_index()

    fig_q6= px.pie(df6, values= "Transaction_Amount", names= "District", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_q6)
# 7.States With Lowest Trasaction Count
def ques7():
    q7= Agg_transaction[["States", "Transaction_Count"]]
    t7= q7.groupby("States")["Transaction_Count"].sum().sort_values(ascending=True)
    df7= pd.DataFrame(t7).reset_index()

    fig_q7= px.bar(df7, x= "States", y= "Transaction_Count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_q7)
# 8.States With Highest Trasaction Count
def ques8():
    q8= Agg_transaction[["States", "Transaction_Count"]]
    t8= q8.groupby("States")["Transaction_Count"].sum().sort_values(ascending=False)
    df8= pd.DataFrame(t8).reset_index()

    fig_q8= px.bar(df8, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_q8)
# 
def ques9():
    q9=Map_transaction[['District','Transaction_Count']]
    t9=q9.groupby('District')['Transaction_Count'].sum().sort_values(ascending= True)
    df9=pd.DataFrame(t9).reset_index().head(10)
 
    fig_q9 = px.line(df9, x='District', y=['Transaction_Count'],
                        title='TOP 10 TRANSACTION COUNT BY DISTRICT ',
                        labels={'District': 'District', 'value': 'Count/Amount'},
                        template='plotly_dark', markers=True)
  
    return st.plotly_chart(fig_q9)

def ques10():
    q10=Map_transaction[['District','Transaction_Amount']]
    t10=q10.groupby('District')['Transaction_Amount'].sum().sort_values(ascending= True)
    df10=pd.DataFrame(t10).reset_index().head(10)

    fig_q10 = px.line(df10, x='District', y=['Transaction_Amount'],
                        title='TOP 10 TRANSACTION AMOUNT BY DISTRICT',
                        labels={'District': 'District', 'value': 'Count/Amount'},
                        template='plotly_dark', markers=True)
  
    return st.plotly_chart(fig_q10)
    
#Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",[ "Data Exploration", "Top Charts"])


if select == "Data Exploration":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years=st.selectbox("Select the Year",Agg_insurance["Year"].unique())
            df_agg_insur_Y= Insurance_count_amount_Y(Agg_insurance,years)
            
            col1,col2= st.columns(2)
            with col1:
                 quarters=st.selectbox("Select the Quarter",df_agg_insur_Y["Quarter"].unique())
            Insurance_count_amount_Q(df_agg_insur_Y, quarters)
        
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at=st.selectbox("Select the Year",Agg_transaction["Year"].unique())
            df_agg_tran_Y= Transaction_count_amount_Y(Agg_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at=st.selectbox("Select the Year",df_agg_tran_Y["Quarter"].unique())

            df_agg_tran_Q= Transaction_count_amount_Q(df_agg_tran_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Q["States"].unique())

            Agg_trans_method(df_agg_tran_Q,state_Y_Q)   
        
        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year",Agg_user["Year"].unique())
            agg_user_Y= Agg_user_Y(Agg_user,year_au)

            quarter_au= st.selectbox("Select the Quarter",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Agg_user_Q(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])


        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.slider("**Select the Year**", Map_insurance["Year"].min(), Map_insurance["Year"].max(),Map_insurance["Year"].min())

            df_map_insur_Y= Insurance_count_amount_Y(Map_insurance,years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y,state_m1)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m1= st.slider("**Select the Quarter**", df_map_insur_Y["Quarter"].min(), df_map_insur_Y["Quarter"].max(),df_map_insur_Y["Quarter"].min())

            df_map_insur_Y_Q= Insurance_count_amount_Q(df_map_insur_Y, quarters_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m2= st.selectbox("Select the State", df_map_insur_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_insur_Y_Q, state_m2)
        
        
        elif method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.slider("**Select the Year**", Map_transaction["Year"].min(), Map_transaction["Year"].max(),Map_transaction["Year"].min())

            df_map_tran_Y= Transaction_count_amount_Y(Map_transaction, years_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State", df_map_tran_Y["States"].unique())

            map_trans_plot_1(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.slider("**Select the Quarter**", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(),df_map_tran_Y["Quarter"].min())

            df_map_tran_Y_Q= Transaction_count_amount_Q(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State", df_map_tran_Y_Q["States"].unique(),key='State_Selection')            
            
            map_trans_plot_2(df_map_tran_Y_Q, state_m4)

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu3= st.selectbox("**Select the Year**",Map_user["Year"].unique(),key='Year_Selection')
            map_user_Y= map_user_plot_1(Map_user, year_mu3)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu3= st.selectbox("**Select the Quarter",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu3)

            col1,col2= st.columns(2)
            with col1:
                state_mu3= st.selectbox("**Select the State**",map_user_Y_Q["States"].unique(),key='State_selection')
            map_user_plot_3(map_user_Y_Q, state_mu3)

    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year**", Top_insurance["Year"].min(), Top_insurance["Year"].max(),Top_insurance["Year"].min())
 
            df_top_insur_Y= Insurance_count_amount_Y(Top_insurance,years_t1)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.slider("**Select the Quarter**", df_top_insur_Y["Quarter"].min(), df_top_insur_Y["Quarter"].max(),df_top_insur_Y["Quarter"].min())

            df_top_insur_Y_Q= Insurance_count_amount_Q(df_top_insur_Y, quarters_t1)
        
        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.slider("**Select the Year**", Top_transaction["Year"].min(), Top_transaction["Year"].max(),Top_transaction["Year"].min())
 
            df_top_tran_Y= Transaction_count_amount_Y(Top_transaction,years_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.slider("**Select the Quarter**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(),df_top_tran_Y["Quarter"].min())

            df_top_tran_Y_Q= Transaction_count_amount_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year**", Top_user["Year"].unique())

            df_top_user_Y= top_user_plot_1(Top_user,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State**", df_top_user_Y["States"].unique(),key='State_Selection')

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)
    
