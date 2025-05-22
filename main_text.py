import pandas as pd
from datetime import datetime, timedelta



df = pd.DataFrame({
    'project': ['Project A', 'Project B'],
    't1':  ['5/1/2025', '5/2/2025'],
    't2':  ['5/6/2025', '5/6/2025'],
    't3':  ['5/11/2025', '5/12/2025'],
    'end': ['5/15/2025', '5/23/2025']
})

subtasks = []
for i, col in enumerate(df.columns):
    if i > 0:
        if i < (len(df.columns) - 1):
          subtasks.append(col)
        df[col] = pd.to_datetime(df[col], format='%m/%d/%Y')


colors = [
    '\033[40m \033[0m',  # Black
    '\033[41m \033[0m',  # Red
    '\033[42m \033[0m',  # Green
    '\033[43m \033[0m',  # Yellow
    '\033[44m \033[0m',  # Blue
    '\033[45m \033[0m',  # Magenta
    '\033[46m \033[0m',  # Cyan
    '\033[47m \033[0m',  # White
    '\033[100m \033[0m', # Bright Black (Gray)
    '\033[101m \033[0m', # Bright Red
    '\033[102m \033[0m', # Bright Green
    '\033[103m \033[0m', # Bright Yellow
    '\033[104m \033[0m', # Bright Blue
    '\033[105m \033[0m', # Bright Magenta
    '\033[106m \033[0m', # Bright Cyan
    '\033[107m \033[0m', # Bright White
]

subtask_color = {
  subtask: colors[i] for i, subtask in enumerate(subtasks)
}

# Define timeline resolution
start_date = df.iloc[:, 1].min()
end_date = df['end'].max()
total_days = (end_date - start_date).days + 1

# Function to build row string for a project
def build_row(row):
    bar = [' '] * total_days
    for i, task in enumerate(subtasks):
        start = (row[task] - start_date).days
        if i < len(subtasks) - 1:
            end = (row[subtasks[i+1]] - start_date).days
        else:
            end = (row['end'] - start_date).days
        for i in range(start, end):
            bar[i] = subtask_color[task]
    return ''.join(bar)

# Print Gantt chart
print()
for idx, row in df.iterrows():
    bar = build_row(row)
    print(f"{row['project']:<15} ->    {bar}")

# Print timeline markers
tick_step = 10  # characters
print(f"\n{'Timeline':<15} ->    ", end="")
for day in range(0, total_days, tick_step):
    tick_date = start_date + timedelta(days=day)
    label = tick_date.strftime('%m/%d/%y')
    print(f"{label:<{tick_step}}", end="")
print("\n")
