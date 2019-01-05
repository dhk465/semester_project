import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
        html.H1(
            children='Python Semester Project'
        ),
        html.Div(children='''
            AIDS statistics in Australia up to 1992
        ''')
])

if __name__ == '__main__':
    app.run_server()