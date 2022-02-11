from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px






def import_export_figure(df_imp,df_exp,Interest_list):
    # fig = make_subplots(rows=1, cols=1,shared_xaxes=True,shared_yaxes=False,subplot_titles=("2019       Imports {}  Exports {} ($MM)".format(-int(df_imp['Trade Value'].sum()),int(df_exp['Trade Value'].sum()))
    #                                                                                         ),vertical_spacing =0.05)


    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_imp[df_imp['HS4'].isin(Interest_list)]['HS4'], y=df_imp[df_imp['HS4'].isin(Interest_list)]['Trade Value'],marker_pattern_shape=".",name='Imports',marker_color='red'))
    fig.add_trace(go.Bar(x=df_exp[df_exp['HS4'].isin(Interest_list)]['HS4'], y=df_exp[df_exp['HS4'].isin(Interest_list)]['Trade Value'], marker_pattern_shape="+",name='Exports',marker_color='green'))

    fig.update_layout(#width=1500,
        height=800,
        barmode='relative')
    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)',    yanchor="bottom",orientation="v",
        y=0.5,
        xanchor="center",
        x=1.07),
                      font=dict(
                          family="Palatino Linotype",
                          size=18,
                          color="white"
                      )
                      )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })
    fig.update_yaxes(title_text="Value ($MM)")

    return fig