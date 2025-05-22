
import pandas as pd
import plotly.graph_objects as go

# Sample data: each project has tasks t1, t2, t3
# New structure: one column per subtask's start, plus a final end-date column
df = pd.DataFrame({
    'project': ['Project A', 'Project B'],
    't1':  ['5/1/2025', '5/2/2025'],
    't2':  ['5/6/2025', '5/6/2025'],
    't3':  ['5/11/2025', '5/12/2025'],
    'end': ['5/15/2025', '5/15/2025']
})

subtasks = []
for i, col in enumerate(df.columns):
    if i > 0:
        if i < (len(df.columns) - 1):
          subtasks.append(col)
        df[col] = pd.to_datetime(df[col], format='%m/%d/%Y')


colors = ['rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)']
subtask_color = {
  subtask: colors[i] for i, subtask in enumerate(subtasks)
}

# Create figure
fig = go.Figure()

# Layout parameters
row_height = 0.8
y_base = list(reversed(range(len(df))))  # top-down layout

# Collect all shapes
shapes = []
for i, (_, row) in enumerate(df.iterrows()):
    y_center = y_base[i]

    for j, task in enumerate(subtasks):
        start = row[task]
        if j < len(subtasks) - 1:
            end = row[subtasks[j+1]]
        else:
            end = row['end']

        color = subtask_color[task]

        shapes.append(dict(
            type="rect",
            xref="x",
            yref="y",
            x0=start, x1=end,
            y0=y_center - row_height / 2,
            y1=y_center + row_height / 2,
            fillcolor=color,
            line=dict(width=0),
            layer="below",
        ))

# Add all shapes to figure
fig.update_layout(shapes=shapes)

# Add dummy scatter traces for legend
for task in subtasks:
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=10, color=subtask_color[task]),
        name=task,
        showlegend=True,
    ))

# Configure y-axis ticks
fig.update_yaxes(
    tickvals=y_base,
    ticktext=[p + " ->  " for p in df['project']],
    title="Project",
    range=[-1, len(df)],
    showgrid=False,
    zeroline=False
)

# Configure x-axis with datetime type and custom tick format
fig.update_xaxes(
    title="Date",
    type="date",
    showgrid=False,
    tickformat="%m/%d/%Y", 
)

# Final layout tweaks
fig.update_layout(
    title="Manual Gantt Chart",
    height=400 + 40 * len(df),
    plot_bgcolor="white",
)

fig.show()
