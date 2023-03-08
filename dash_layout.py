from dash import Dash, dcc, html, Output, Input, State, callback, dash_table
import mysql.connector
import pandas as pd
import dash_bootstrap_components as dbc

# Connect to the database
conn = mysql.connector.connect(host="localhost", user="root", password="", database="FYP")

# Create a cursor object
cursor = conn.cursor()

# Retrieve all values from a table
# company_values_query = "SELECT c.name, b.outlook_2017, a.profit_growth_2017, " \
#                        "b.outlook_2018, a.profit_growth_2018, " \
#                        "b.outlook_2019, a.profit_growth_2019, " \
#                        "b.outlook_2020, a.profit_growth_2020, " \
#                        "b.outlook_2021, a.profit_growth_2021, " \
#                        "(10 + a.profit_growth_2017) AS credibility_score " \
#                        "FROM CompanyYearlyProfitGrowth a  " \
#                        "JOIN CompanyOutlookSentiment b " \
#                        "ON a.company_ID = b.company_ID " \
#                        "JOIN Company c ON c.ID = a.company_ID;"

company_values_query = "SELECT b.name, a.outlook_2017," \
                       "(10 + a.outlook_2017) AS credibility_score " \
                       "FROM CompanyOutlookSentiment a " \
                       "JOIN Company b ON b.ID = a.company_ID;"

cursor.execute(company_values_query)

# Fetch the results
results = cursor.fetchall()

df = pd.DataFrame([[ij for ij in i] for i in results])
df.rename(columns={0: 'Company Name', 1: 'Lastest Outlook', 2: 'Credibility Score'},
          inplace=True)

# df = df.sort_values(['LifeExpectancy'], ascending=[1]);

layout = dbc.Container([
    dbc.Row([
        dbc.Col(width=2),
        dbc.Col(dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                page_size=10,
                style_cell_conditional=[
                                {'if': {'column_id': 'Company Name'},
                                 'textAlign': 'left', 'paddingLeft': '10px'},
                                {'if': {'column_id': 'Lastest Outlook'},
                                 'textAlign': 'center'},
                                {'if': {'column_id': 'Credibility Score'},
                                 'textAlign': 'center'}
                            ],
                style_header={'textAlign': 'center'}
            ), width=8, style={'margin-top': '130px'}),
        dbc.Col(width=2)
    ])
], className='mt-4')
