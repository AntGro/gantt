import numpy as np
from datetime import datetime, timedelta

import pandas as pd
from datetime import datetime, timedelta
import shutil

terminal_size = shutil.get_terminal_size()


import pandas as pd

df = pd.DataFrame({
    'project': ['Project A', 'Project B', 'Project C', 'Project D', 'Project E'],
    'step1':   ['1/10/2025', '3/5/2025',  '5/1/2025',  '7/20/2025', '10/15/2025'],
    'step2':   ['1/17/2025', '3/12/2025', '5/8/2025',  '7/28/2025', '10/22/2025'],
    'step3':   ['1/25/2025', '3/20/2025', '5/17/2025', '8/4/2025',  '10/30/2025'],
    'step4':   ['1/30/2025', '3/28/2025', '5/24/2025', '8/10/2025', '11/7/2025'],
    'step5':   ['2/4/2025',  '4/5/2025',  '6/1/2025',  '8/18/2025', '11/15/2025'],
    'end':     ['2/10/2025', '4/12/2025', '6/8/2025',  '8/25/2025', '11/23/2025']
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

def map_dates_to_timeline(start_date: str, end_date: str, date_format='%Y-%m-%d', width=None) -> dict:
    # Parse dates
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    total_days = (end - start).days
    if total_days == 0:
        return {start.strftime(date_format): 0}

    # Get terminal width (or set a default minimum)
    if width is None:
        width = shutil.get_terminal_size().columns
    timeline_width = max(20, width - 10)

    # Map each date to a timeline index
    date_to_index = {}
    current = start
    while current <= end:
        days_elapsed = (current - start).days
        index = round(days_elapsed * (timeline_width - 1) / total_days)
        date_to_index[current.strftime(date_format)] = index
        current += timedelta(days=1)

    return date_to_index

def print_timeline(date_to_index: dict, label_interval_days=None, n_ticks=None, offset: str | None = None):
    if offset is None:
        offset = "" 
    
    # Prepare basics
    dates = sorted(date_to_index.keys())
    width = max(date_to_index.values()) + 1
    timeline_line = ['─'] * width
    label_line = [' '] * width
    date_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    start_date, end_date = date_objs[0], date_objs[-1]
    total_days = (end_date - start_date).days

    # Compute tick dates
    if n_ticks is not None and n_ticks > 1:
        tick_days = np.linspace(0, total_days, n_ticks + 2)[1:-1]
        tick_dates = [start_date + timedelta(days=np.round(tick_day)) for tick_day in tick_days]
    elif label_interval_days:
        tick_dates = []
        current = start_date
        while current <= end_date:
            tick_dates.append(current)
            current += timedelta(days=label_interval_days)
    else:
        raise ValueError("Either n_ticks or label_interval_days must be provided")

    # Place ticks and labels
    timeline_line[0] = '┬'
    for d in tick_dates:
        dstr = d.strftime("%Y-%m-%d")
        if dstr not in date_to_index:
            raise ValueError(dstr)
        i = date_to_index[dstr]
        timeline_line[i] = '┬'
        label = dstr
        start = max(0, i - len(label) // 2)
        for j, ch in enumerate(label):
            if 0 <= start + j < width:
                label_line[start + j] = ch

    timeline_line[-1] = '┬'

    print(offset + ''.join(timeline_line))
    print(offset + ''.join(label_line))


def build_row(row):
    bar = [' '] * len(mapping)
    for i, task in enumerate(subtasks):
        start_date = row[task]
        if i < len(subtasks) - 1:
            end_date = row[subtasks[i+1]]
        else:
            end_date = row['end']

        for i in range(mapping[start_date.strftime('%Y-%m-%d')], mapping[end_date.strftime('%Y-%m-%d')]):
            bar[i] = subtask_color[task]
    return ''.join(bar)

import shutil
from datetime import datetime, timedelta



# Example usage
width = terminal_size.columns * 2
mapping = map_dates_to_timeline(start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'), width=width)


# Print Gantt chart
print()
arrow = " ->    "
for idx, row in df.iterrows():
    bar = build_row(row)
    print(f"{row['project']:<15}{arrow}{bar}")

print_timeline(mapping, n_ticks=10, offset=" " * (15 + len(arrow)))
print()

legends = []
length = 0
s = ""
for subtask in subtasks:
    s += subtask_color[subtask] * 2 + " " + subtask + "\033[0m" + "   "
    length += len(subtask) + 6
    if length > width:
        length = 0
        legends.append((s[:-2], length - 3))
        s = ""

if len(s) > 0:
    legends.append((s[:-2], length - 3))

for legend in legends:
    center_gap = (width - legend[-1]) // 2
    print(" " * center_gap + legend[0] + " " * center_gap)
