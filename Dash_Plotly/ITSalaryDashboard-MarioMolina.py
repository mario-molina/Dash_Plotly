import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

######################################## STYLES ###############################################3
corporate_colors = {
    'dark-blue-grey' : 'rgb(62, 64, 76)',
    'medium-blue-grey' : 'rgb(77, 79, 91)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}

filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['light-green'],
    'background-color' : corporate_colors['light-green'],
    'box-shadow' : '2px 5px 5px 1px rgba(255, 101, 131, .5)'
    }

filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['light-green'],
    'background-color' : corporate_colors['light-green'],
    'box-shadow' : '2px 5px 5px 1px rgba(255, 101, 131, .5)'
    }

# ---------- Import data (importing csv into pandas)
# File was merged into one and cleaned up before.
pathToCsv ="https://dl.dropboxusercontent.com/s/8fuor88azrhytyw/TI_data_merged.csv"
df = pd.read_csv(pathToCsv)

# ------------------------------------------------------------------------------
# App layout
#####################
# Header with logo
def get_header():

    header = html.Div([

        html.Div([], className = 'col-2'),

        html.Div([
            html.H1(children='Informe de la encuesta de sueldos de TI',
                    style = {'textAlign' : 'center'}
            )],
            className='col-8',
            style = {'padding-top' : '1%'}
        ),

        html.Div([
            html.Img(
                    src = 'https://dl.dropboxusercontent.com/s/kbhn3z4h6jov5u4/Programming%20Model.png',
                    height = '43 px',
                    width = 'auto')
            ],
            className = 'col-2',
            style = {
                    'align-items': 'center',
                    'padding-top' : '1%',
                    'height' : 'auto'})

        ],
        className = 'row',
        style = {'height' : '4%',
                 'color': corporate_colors['light-grey'],
                'background-color' : corporate_colors['superdark-green']}
        )

    return header

def get_first_chart():

    chart = html.Div([
        ###########   Filters  ##########
        html.Div([

            html.H5('Company type:'),
            dcc.Dropdown(id="ddl_company_type",
                         options=[
                             {'label': i, 'value': i} for i in df['company_type'].unique()
                         ],
                         multi=False,
                         value='Product',
                         style={'width': "100%"}
                         ),
            html.H5('Year:'),
            dcc.Dropdown(id="ddl_year",
                         options=[
                             {'label': i, 'value': i} for i in df['year'].unique()
                         ],
                         multi=False,
                         value='2018',
                         style={'width': "100%"}
                         ),

        ],
        className = 'col-md-12 p-3'),

        ##############  Charts  ##############
        html.Div([
            dcc.Graph(id='gender_chart', figure={})
        ],
        className='col-md-4 p-1'),
        html.Div([
            dcc.Graph(id='salary_chart', figure={})

        ],
        className = 'col-md-4 p-1'),
        html.Div([
            dcc.Graph(id='language_chart', figure={})
        ],
        className='col-md-4 p-1')
    ],
    className = 'row')

    return chart

def get_second_chart():

    chart = html.Div([
        ##############  Charts  ##############

        html.Div([
            dcc.Graph(id='language_timeline', figure={})
        ],
        className = 'col-md-12 p-6')
        ],
        className = 'row')

    return chart


app.layout = html.Div([
    #####################
    #Row 1 : Header
    get_header(),
    get_first_chart(),
    html.Br(),
    get_second_chart(),
],
className = 'container',
style = filterdiv_borderstyling)

@app.callback(
    [Output(component_id='salary_chart', component_property='figure'),
     Output(component_id='language_chart', component_property='figure'),
     Output(component_id='gender_chart', component_property='figure'),
     Output(component_id='language_timeline', component_property='figure')],
    [Input(component_id='ddl_company_type', component_property='value'),
     Input(component_id='ddl_year', component_property='value')]
)
def update_graph(company_type_slctd, ddl_year):
    dff = df.copy()
    dff = dff[dff['company_type'] == company_type_slctd]
    dff = dff[dff['year'] == int(ddl_year)]

    fig = px.violin(
        dff,
        x="seniority",
        y="salary",
        box=True,
        title='Salary vs Seniority'
    )

    fig.update_layout(
        title="Salary mean vs Seniority",
        xaxis_title="Seniority",
        yaxis_title="Salary",
        font=dict(
            family="Courier New, monospace",
            size=13,
            color=corporate_colors['medium-green']
        )
    )

    languages_df = pd.DataFrame(dff['programming_language'].value_counts(sort=True)).reset_index()
    languages_df.rename(columns={'index': 'programming_language', 'programming_language': 'frequency'}, inplace=True)

    fig2 = px.bar(
        languages_df,
        x='programming_language',
        y='frequency'
    )

    fig2.update_layout(
        title="Most used languages",
        xaxis_title="Programming language",
        yaxis_title="Popularity",
        font=dict(
            family="Courier New, monospace",
            size=13,
            color=corporate_colors['medium-green']
        )
    )

    gender_df = pd.DataFrame(dff['gender'].value_counts(sort=True)).reset_index()
    gender_df.rename(columns={'index': 'gender', 'gender': 'frequency'}, inplace=True)

    fig3 = px.pie(
        gender_df,
        values='frequency',
        names='gender',
        title='Gender distribution'
    )

    fig3.update_layout(
        title="Gender distribution",
        font=dict(
            family="Courier New, monospace",
            size=13,
            color=corporate_colors['medium-green']
        )
    )

    fig4_ds = df.copy()
    fig4_ds['year'] = fig4_ds['year'].astype(str)
    fig4_ds = fig4_ds.query("programming_language in ('PHP','.NET','Java','Python','Javascript','C++','C#','C','Go','Ruby')")
    fig4_ds = fig4_ds.groupby(['programming_language', 'year']).agg({'salary': ['mean']}).reset_index()
    fig4_ds.columns = fig4_ds.columns.get_level_values(0)
    fig4_ds = fig4_ds.pivot(index='year', columns='programming_language', values='salary')
    fig4_ds.reset_index().columns

    fig4 = px.line(fig4_ds.reset_index(), x='year', y=fig4_ds.reset_index().columns)
    fig4.update_xaxes(type='category')

    fig4.update_layout(
        title="Yearly income based on used Programming language per year",
        xaxis_title="Year",
        yaxis_title="Yearly income",
        font=dict(
            family="Courier New, monospace",
            size=13,
            color=corporate_colors['medium-green']
        )
    )

    return fig, fig2, fig3, fig4
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
