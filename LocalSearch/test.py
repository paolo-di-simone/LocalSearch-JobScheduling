import plotly.graph_objs as go
import plotly.io as pio

from Machine import Machine

if __name__ == '__main__':

    dict_color = {
        "A": "#c8a2c8",
        "B": "#6495ED"
    }

    m = Machine({"A": 10, "B": 10}, 5, 20, 2)
    #steps = m.local_search_first_improvement()
    steps = m.local_search_steepest_descent()

    steps_shape = []
    for step in steps:
        length = 0
        dict_of_shape = {}
        jobs_sequence = step[0].get_job_sequence()
        for job in jobs_sequence:
            dict_of_shape[job.get_id()] = {
                "x": [length, length + job.get_length(), length + job.get_length(), length, length],
                "y": [0, 0, 1, 1, 0],
                "color": dict_color[job.get_user()],
                "label": str(job.get_user())+str(job.get_length())
            }
            length += job.get_length()
        steps_shape.append(dict_of_shape)

    start = []
    for key, value in steps_shape[0].items():
        start.append(go.Scatter(x=value["x"], y=value["y"], mode='lines', fill='toself', fillcolor=value["color"], name=key, line=dict(color="black", width=2)))
        start.append(go.Scatter(x=[(max(value["x"])+min(value["x"]))/2], y=[1.1], mode='text', text=value["label"], textfont=dict(color='black', size=10)))

    end = []
    for key, value in steps_shape[-1].items():
        end.append(go.Scatter(x=value["x"], y=value["y"], mode='lines', fill='toself', fillcolor=value["color"], name=key, line=dict(color="black", width=2)))
        end.append(go.Scatter(x=[(max(value["x"]) + min(value["x"])) / 2], y=[1.1], mode='text', text=value["label"], textfont=dict(color='black', size=10)))

    fig = go.Figure(data=start, layout=go.Layout(xaxis=dict(range=[0, 100]), yaxis=dict(range=[0, 2])))

    steps = []
    for step in steps_shape[1:-1]:
        data = []
        for key, value in step.items():
            data.append(go.Scatter(x=value["x"], y=value["y"], mode='lines', fillcolor=value["color"], name=key, line=dict(color="black", width=2)))
            data.append(go.Scatter(x=[(max(value["x"]) + min(value["x"])) / 2], y=[1.1], mode='text', text=value["label"], textfont=dict(color='black', size=10)))
        steps.append(go.Frame(data=data))

    fig.frames = [go.Frame(data=start)] + steps + [go.Frame(data=end)]

    fig.layout.updatemenus = [
        dict(
            type='buttons',
            showactive=False,
            buttons=[
                dict(
                    label='Play',
                    method='animate',
                    args=[
                        None,
                        dict(
                            frame=dict(
                                duration=800,
                                redraw=True
                            ),
                            fromcurrent=True,
                            transition=dict(duration=300)
                        )
                    ]
                ),
                dict(
                    label='Pause',
                    method='animate',
                    args=[
                        [None],
                        dict(
                            frame=dict(
                                duration=0,
                                redraw=False
                            ),
                            mode='immediate',
                            transition=dict(duration=0)
                        )
                    ]
                )
            ]
        )
    ]

    pio.show(fig)
