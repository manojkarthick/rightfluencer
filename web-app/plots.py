import plotly
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout, Bar


def bar_plot(x_list, y_list, barcolors, vertical=True, title='',
             showYAxis=False, showYticks=False, showYticklabels=False,
             showXAxis=False, showXticks=False, showXticklabels=False,
             gridY=False, gridx=False):

    xaxisdict = dict(
        showline=True,
        showgrid=gridx,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        autotick=False,
        ticks='outside',
        tickcolor='rgb(204, 204, 204)',
        tickwidth=2,
        ticklen=5,
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    )

    yaxisdict = dict(
        linecolor='rgb(204, 204, 204)',
        autorange=True,
        showgrid=gridY,
        zeroline=False,
        showline=showYAxis,
        autotick=True,
        ticks='outside',
        tick0=0,
        showticklabels=showYticklabels
    )

    layout = go.Layout(
        title=title,
        yaxis=yaxisdict if vertical else xaxisdict,
        xaxis=xaxisdict if vertical else yaxisdict,
        width=500,
        height=500,
        autosize=False,
        margin=dict(
            autoexpand=False,
            # l=-50,
            # r=20,
            # t=110,
        ),
        showlegend=False
    )

    trace0 = go.Bar(
        x=x_list,
        y=y_list,
        marker=dict(
            color=barcolors,
            line=dict(
                color='rgba(115,115,115, 0.5)',
                width=1.5,
            )
        ),
        opacity=0.6,
        orientation='v' if vertical else 'h'
    )

    plot = plotly.offline.plot({
        "data": [trace0],
        'layout': layout
    }, output_type="div", include_plotlyjs=False, link_text="", show_link=False)
    return plot


def bubble_plot(x_list, radius, bubblecolors='', title='', hover_labels=''):

    height_y = [max(radius) + 10] * len(radius)

    xaxisdict = dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        autotick=False,
        ticks='outside',
        tickcolor='rgb(204, 204, 204)',
        tickwidth=2,
        ticklen=5,
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    )

    yaxisdict = dict(
        linecolor='rgb(204, 204, 204)',
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        tick0=0,
        showticklabels=False
    )

    layout = go.Layout(
        title=title,
        yaxis=yaxisdict,
        xaxis=xaxisdict,
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False
    )

    trace0 = go.Scatter(
        x=x_list,
        y=height_y,  # [15, 15, 15],
        mode='markers',
        marker=dict(
            size=radius,
            color=bubblecolors,
            line=dict(
                color='rgba(115,115,115, 0.5)',
                width=1.5,
            )
        ),
        opacity=0.6,
        showlegend=False,
        hoverinfo='text',
        text=hover_labels
    )

    plot = plotly.offline.plot({
        "data": [trace0],
        'layout': layout,
    }, output_type="div", include_plotlyjs=False, link_text="", show_link=False)

    return plot


def multi_line(x_data, y_data, labels, colors, title, x_axis_label, fill=False):

    x_count = len(x_data[0])
    mode_size = [8] * len(labels)
    line_size = [2] * len(labels)

    draw_fill = 'tozeroy' if fill else ''
    traces = []
    for i in range(0, len(labels)):
        traces.append(go.Scatter(
            x=x_data[i],
            y=y_data[i],
            mode='lines+markers',
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
            fill=draw_fill,
            hoverinfo='all',
            name=labels[i]
        ))

#         traces.append(go.Scatter(
#             x=[x_data[i][0], x_data[i][x_count -1]],
#             y=[y_data[i][0], y_data[i][x_count-1]],
#             mode='markers',
#             marker=dict(color=colors[i], size=mode_size[i]),
#             hoverinfo='none'
#         ))

    layout = go.Layout(
        xaxis=dict(
            range=[0, x_count - 1],
            zeroline=False,
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            autotick=False,
            ticks='outside',
            tickcolor='rgb(204, 204, 204)',
            tickwidth=2,
            ticklen=5,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            title='Activity',
            titlefont=dict(family='Arial', size=12, color='rgb(150,150,150)'),
            linecolor='rgb(204, 204, 204)',
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=False,
            ticks='',
            showticklabels=False,
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=100,
            r=40,
            t=110,
        ),
        showlegend=True
    )

    annotations = []

    # Adding labels
#     for y_trace, label, color in zip(y_data, labels, colors):
#         # labeling the left_side of the plot
#         annotations.append(dict(xref='paper', x=0.05, y=y_trace[0] + 5,
#                                       xanchor='right', yanchor='middle',
#                                       text=label + ' {}'.format(y_trace[0]),
#                                       font=dict(family='Arial',
#                                                 size=16,
#                                                 color=colors,),
#                                       showarrow=False))
#         # labeling the right_side of the plot
#         annotations.append(dict(xref='paper', x=0.95, y=y_trace[x_count -1],
#                                       xanchor='left', yanchor='middle',
#                                       text=' {}'.format(y_trace[x_count -1]),
#                                       font=dict(family='Arial',
#                                                 size=16,
#                                                 color=colors,),
#                                       showarrow=False))
    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text=title,
                            font=dict(family='Arial',
                                      size=30,
                                      color='rgb(37,37,37)'),
                            showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                            xanchor='center', yanchor='top',
                            text=x_axis_label,
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    layout['annotations'] = annotations

    plot = plotly.offline.plot({
        "data": traces,
        'layout': layout
    }, output_type="div", include_plotlyjs=False, link_text="", show_link=False)
    return(plot)


def heat_map(x, y, z, title='', colorscale='YlGnBu'):
    trace0 = go.Heatmap(
        z=z,
        y=y,
        x=x,
        colorscale=colorscale,
    )

    layout = go.Layout(
        title=title,
        xaxis=dict(
            autotick=False,
            ticks='outside',
            dtick=3.0
        )
    )

    plot = plotly.offline.plot({
        "data": [trace0],
        "layout": layout,
    }, output_type="div", include_plotlyjs=False, link_text="", show_link=False)

    return plot


def plotWaterfall(x_data, positives, negatives, bases):

    # Base
    trace0 = go.Bar(
        x=x_data,
        y = bases,
        marker=dict(
            color='rgba(1,1,1, 0.0)',
        )
    )
    # Revenue
    trace1 = go.Bar(
        x=x_data,
        y = positives,
        marker=dict(
            color='#2db24a'
        )
    )
    # Costs
    trace2 = go.Bar(
        x=x_data,
        y= negatives,
        marker=dict(
            color='#C45B15'
        )
    )


    data = [trace0, trace1, trace2]
    layout = go.Layout(
        title='Audience Growth - Past week',
        barmode='stack',
        showlegend=False
    )


    fig = go.Figure(data=data, layout=layout)

    plot = plotly.offline.plot({
        "data": data,
        "layout": layout,
    }, output_type="div", include_plotlyjs=False, link_text="", show_link=False)

    return plot

