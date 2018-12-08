from jinja2 import Template

import json
import datetime

import plotly
import plotly.graph_objs as go

def scale(value):
    return int(int(value.split('.')[0]) / 1000000)

def main():
    with open('speedtest.csv', 'rt') as file:
        it = iter(file)
        next(it)
        rows = list(line.split(',') for line in it)

        x_axis = [
            datetime.datetime.strptime(r[3].split('.')[0], '%Y-%m-%dT%H:%M:%S') for r in rows
        ]

        graph = dict(
            data=[
                go.Scatter(
                    x = x_axis,
                    y = [
                        scale(r[6]) for r in rows
                    ],
                    mode = 'lines',
                    name = 'Download'
                ),
                go.Scatter(
                    x = x_axis,
                    y = [
                        scale(r[7]) for r in rows
                    ],
                    mode = 'lines',
                    name = 'Upload'
                )
            ],
            layout=dict(
                title='Bandwidth',
                yaxis=dict(
                    title="Bandwidth (Mb/s)"
                ),
                xaxis=dict(
                    title="Time",
                    range=[
                        datetime.datetime.now() - datetime.timedelta(days=14),
                        datetime.datetime.now()
                    ]
                )
            )
        )

        with open('index.html.jinja2') as template_file:
            template = Template(template_file.read())

            html = template.render(graph=json.dumps(
                graph,
                cls=plotly.utils.PlotlyJSONEncoder
            ))

            with open('index.html', 'w') as html_file:
                html_file.write(html)

if __name__ == "__main__":
    main()
