from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


class ChartGenerator:
    def __init__(self, df_path):
        self.df = pd.read_excel(df_path, header=6, index_col=1)
        self.df = self.df.drop(columns='Unnamed: 0')
        self.df = self.df.replace({
            "Improved": 'improve',
            "Increased" : 'improve',
            "Remained The Same" : 'same',
            "Decreased" : "worse",
            "Worsened": 'worse',
            "Will Improve": 'improve',
            "Will Increase": 'improve',
            "Remain The Same": 'same',
            "Will Decrease" : "worse",
            "Will Worsen": 'worse',
        })

    def pie(self,df, col):
        colcount = df[col].value_counts().reset_index()
        colcount.columns = ["key", "value"]
        fig = px.pie(colcount, values=colcount["value"], names=colcount["key"])
        return fig
    
    def bar(self, df, col):
        per = df["Perception on " + col + " - compared to one year ago"].value_counts().reset_index()
        per.columns = ["key", "value"]
        out = df["Outlook on "+ col +" - one year ahead"].value_counts().reset_index()
        out.columns = ["key", "value"]
        x_axis = per["key"]
        fig = go.Figure(data=[
            go.Bar(name="Perception on " + col + " - compared to one year ago", x=x_axis, y=per["value"]),
            go.Bar(name="Outlook on "+ col +" - one year ahead", x=x_axis, y=out["value"])
        ])
        return fig
    
    def filter_data(self, df, cities, acons, ages, genders):
        filtered_df = df.copy()
        if cities:
            filtered_df = filtered_df[filtered_df['City Name'].isin(cities)]
        if acons:
            filtered_df = filtered_df[filtered_df['Assembly Constituency Name'].isin(acons)]
        if ages:
            filtered_df = filtered_df[filtered_df['Age'].isin(ages)]
        if genders:
            filtered_df = filtered_df[filtered_df['Gender'].isin(genders)]
        return filtered_df
    
    def get_assembly_constituencies(self, selected_cities):
        if selected_cities: 
            return [{'label': acon, 'value': acon} for city in selected_cities for acon in self.df[self.df['City Name'] == city]['Assembly Constituency Name'].unique()]
        else:
            return [{'label': acon, 'value': acon} for acon in self.df['Assembly Constituency Name'].unique()]


chart_generator = ChartGenerator("CCS2.xlsx")

fig1 = chart_generator.pie(chart_generator.df,'City Name')
fig2 = chart_generator.bar(chart_generator.df,"Household income")

dropdown_city = [{'label': city, 'value': city} for city in chart_generator.df["City Name"].unique()]
dropdown_con = [{'label': city, 'value': city} for city in chart_generator.df["Assembly Constituency Name"].unique()]
dropdown_age = [{'label': city, 'value': city} for city in chart_generator.df["Age"].unique()]
dropdown_gender = [{'label': city, 'value': city} for city in chart_generator.df["Gender"].unique()]
pie = ["City Name","Gender","Age","Assembly Constituency Name"]
bar = ["General Economic condition","Household income","Household spending","essential spending","non-essential spending","Employment scenario","General prices","Inflation"]
dropdown_pie = [{'label': city, 'value': city} for city in pie]
dropdown_bar = [{'label': city, 'value': city} for city in bar]



app = Dash(__name__)


app.layout = html.Div(
    style={
        'display': 'flex',
        'flex-direction': 'column', 
        'align-items': 'center',  
        'background-color': '#1a1a1a',  
        'color': '#ffffff',  
    },
    children=[

        html.H1(
            "Consumer Constituency Survey",  
            style={
                'width': '100%',
                'color': '#ffffff',
                'font-size': '36px',
                'margin-bottom': '20px',
                'text-align': 'center', 
            },
        ),

        html.Div(
            style={'display': 'flex', 'width': '100%'},
            children=[

                html.Div(
                    children=[
                        html.Div(
                            [
                                html.Label("Choose Filter :",
                                    style={
                                        'width': '100%',
                                        'color': '#ffffff',
                                        'font-size': '24px',
                                    },
                                ),
                            ],
                        ),
                        html.Br(),  
                        html.Div(
                            [
                                html.Label('City Name',
                                    style={'color': '#ffffff'}), 
                                dcc.Dropdown(
                                    id='city',
                                    options=dropdown_city,
                                    multi=True,
                                    style={
                                        'width': '100%',
                                        'background-color': '#4d4d4d',
                                        'color': '#000000',
                                        'font-size': '14px',
                                    },
                                ),
                            ],
                        ),

                        html.Div(
                            [
                                html.Label('Assembly Constituency Name',
                                    style={'color': '#ffffff'}), 
                                dcc.Dropdown(
                                    id='acon',
                                    options=[{'label': acon, 'value': acon} for acon in chart_generator.df['Assembly Constituency Name'].unique()],  # Initially all options
                                    multi=True,
                                    style={
                                        'width': '100%',
                                        'background-color': '#4d4d4d',
                                        'color': '#000000',
                                        'font-size': '14px',
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.Label('Age',
                                    style={'color': '#ffffff'}),  
                                dcc.Dropdown(
                                    id='age',
                                    options=dropdown_age,
                                    multi=True,
                                    style={
                                        'width': '100%',
                                        'background-color': '#4d4d4d',
                                        'color': '#000000',
                                        'font-size': '14px',
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.Label('Gender',
                                    style={'color': '#ffffff'}),  
                                dcc.Dropdown(
                                    id='gen',
                                    options=dropdown_gender,
                                    multi=True,
                                    style={
                                        'width': '100%',
                                        'background-color': '#4d4d4d',
                                        'color': '#000000',
                                        'font-size': '14px',
                                    },
                                ),
                            ],
                        ),
                    ],
                    style={'width': '20%', 'padding': 10, 'border-right': '1px solid #333333', 'title': "Choose the Filter"}
                ),
                html.Div(
                    [
                        html.Label('Pie Chart',
                            style={'color': '#ffffff'}), 
                        dcc.Dropdown(
                            id='pie',
                            options=dropdown_pie,
                            clearable=False,
                            value="City Name",
                            style={
                                'width': '100%',
                                'background-color': '#ffffff',
                                'color': '#000000',
                                'font-size': '14px',
                            },
                        ),
                        dcc.Graph(
                            id='graph1',
                            figure=fig1,
                            style={
                                'width': '100%',
                                'margin': '5px',
                                'background-color': '#333333',  
                                'border': '1px solid #4d4d4d',  
                            }
                        ),
                    ],
                    style={'width': '40%', 'padding': 10}
                ),

                html.Div(
                    [
                        html.Label('Bar Graph',
                            style={'color': '#ffffff'}), 
                        dcc.Dropdown(
                            id='bar',
                            options=dropdown_bar,
                            clearable=False,
                            value='General Economic condition',
                            style={
                                'width': '100%',
                                'background-color': '#ffffff',
                                'color': '#000000',
                                'font-size': '14px',
                            },
                        ),
                        dcc.Graph(
                            id='graph2',
                            figure=fig2,
                            style={
                                'width': '100%',
                                'margin': '5px',
                                'background-color': '#333333',
                                'border': '1px solid #4d4d4d',
                            }
                        ),
                    ],
                    style={'width': '40%', 'padding': 10}
                ),
            ],
        ),
    ]
)






fig2.update_layout(legend=dict(x=0.95, y=1.2, yanchor="top", xanchor="right")),\
fig2.update_layout(legend_orientation='h'),\
fig1.update_layout(legend_orientation='h'),\
fig1.update_layout(legend=dict(x=1.2, y=0.5))\

@app.callback(
    [Output(component_id='graph1', component_property='figure'),
    Output(component_id='graph2', component_property='figure'),
    Output(component_id='acon', component_property='options')],
    [Input(component_id='city', component_property='value'),
    Input(component_id='acon', component_property='value'),
    Input(component_id='age', component_property='value'),
    Input(component_id='gen', component_property='value'),
    Input(component_id='pie', component_property='value'),
    Input(component_id='bar', component_property='value'),],
    prevent_initial_call=True
)

def update_graphs(selected_cities, selected_acons, selected_age, selected_gen, selected_pie, selected_bar):

    if not selected_pie:  
        selected_pie = "City Name"
    if not selected_bar: 
        selected_bar = "General Economic condition"
    
    if selected_cities and selected_acons:
        selected_acons = [acon for acon in selected_acons if {'label': acon, 'value': acon} in selected_cities]
          
    filtered_df = chart_generator.filter_data(chart_generator.df, selected_cities, selected_acons, selected_age, selected_gen)
    
    fig1 = chart_generator.pie(filtered_df, selected_pie)
    fig2 = chart_generator.bar(filtered_df, selected_bar)

    fig2.update_layout(legend=dict(x=0.95, y=1.2, yanchor="top", xanchor="right"))
    fig1.update_layout(legend=dict(x=1.2, y=0.5))
    fig2.update_layout(legend_orientation='h')
    fig1.update_layout(legend_orientation='h')

    acon_options = chart_generator.get_assembly_constituencies(selected_cities)
    
    return fig1, fig2, acon_options



if __name__ == '__main__':
    app.run_server(debug=True)