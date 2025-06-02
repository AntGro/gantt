import numpy as np
import pandas as pd
from datetime import timedelta
import shutil
from pandas import Timestamp

COLORS_BACKGROUND: list[str] = [
    '\033[40m \033[0m',  # Black
    '\033[41m \033[0m',  # Red
    '\033[42m \033[0m',  # Green
    '\033[43m \033[0m',  # Yellow
    '\033[44m \033[0m',  # Blue
    '\033[45m \033[0m',  # Magenta
    '\033[46m \033[0m',  # Cyan
    '\033[47m \033[0m',  # White
    '\033[100m \033[0m',  # Bright Black (Gray)
    '\033[101m \033[0m',  # Bright Red
    '\033[102m \033[0m',  # Bright Green
    '\033[103m \033[0m',  # Bright Yellow
    '\033[104m \033[0m',  # Bright Blue
    '\033[105m \033[0m',  # Bright Magenta
    '\033[106m \033[0m',  # Bright Cyan
    '\033[107m \033[0m',  # Bright White
]

c = "▮"
c = "■"
c = "◆"
c = "█"
COLORS: list[str] = [
    f'\033[30m{c}\033[0m',  # Black
    f'\033[31m{c}\033[0m',  # Red
    f'\033[32m{c}\033[0m',  # Green
    f'\033[33m{c}\033[0m',  # Yellow
    f'\033[34m{c}\033[0m',  # Blue
    f'\033[35m{c}\033[0m',  # Magenta
    f'\033[36m{c}\033[0m',  # Cyan
    f'\033[37m{c}\033[0m',  # White
    f'\033[90m{c}\033[0m',  # Bright Black (Gray)
    f'\033[91m{c}\033[0m',  # Bright Red
    f'\033[92m{c}\033[0m',  # Bright Green
    f'\033[93m{c}\033[0m',  # Bright Yellow
    f'\033[94m{c}\033[0m',  # Bright Blue
    f'\033[95m{c}\033[0m',  # Bright Magenta
    f'\033[96m{c}\033[0m',  # Bright Cyan
    f'\033[97m{c}\033[0m',  # Bright White
]


def get_terminal_width() -> int:
    return shutil.get_terminal_size().columns


def map_dates_to_timeline(start_date: Timestamp, end_date: Timestamp, width: int | None = None) -> dict[Timestamp, int]:
    total_days = (end_date - start_date).days
    if total_days == 0:
        return {start_date: 0}

    # Get terminal width (or set a default minimum)
    if width is None:
        width = get_terminal_width()
    timeline_width = max(20, width - 10)

    # Map each date to a timeline index
    date_to_index = {}
    current = start_date
    while current <= end_date:
        days_elapsed = (current - start_date).days
        index = round(days_elapsed * (timeline_width - 1) / total_days)
        date_to_index[current] = index
        current += timedelta(days=1)

    return date_to_index


def get_tick_dates(date_to_index: dict[Timestamp, int], show_15: bool) -> list[Timestamp]:
    keep = [1]
    if show_15:
        keep.append(15)
    return [date for date in sorted(date_to_index.keys()) if date.day in keep]


def get_timeline(
        date_to_index: dict[Timestamp, int], tick_dates: list[Timestamp], tick_symbol: str, line_symbol: str,
        end_line_symbol: str, show_labels: bool, offset: str | None = None,
) -> str:
    if offset is None:
        offset = ""

    width = max(date_to_index.values()) + 1
    timeline_line = [line_symbol] * width
    label_line = [' '] * width

    # Place ticks and labels
    for d in tick_dates:
        if d not in date_to_index:
            raise ValueError(d)
        i = date_to_index[d]
        timeline_line[i] = tick_symbol
        label = d.strftime('%Y-%m-%d')
        start = max(0, i - len(label) // 2)
        for j, ch in enumerate(label):
            if 0 <= start + j < width:
                label_line[start + j] = ch
    timeline_line[-1] = end_line_symbol
    s = offset + ''.join(timeline_line)
    if show_labels:
        s += "\n" + offset + ''.join(label_line)
    return s


def build_row(row: pd.Series, subtasks: list[str]) -> str:
    bar = [' '] * len(set(date_to_index.values()))
    for i, task in enumerate(subtasks):
        start_date = row[task]
        if i < len(subtasks) - 1:
            end_date = row[subtasks[i + 1]]
        else:
            end_date = row['end']

        for i in range(date_to_index[start_date], date_to_index[end_date]):
            bar[i] = subtask_color[task]
    return ''.join(bar)


df = pd.DataFrame(
    {
        'project': ['Project A', 'Project B', 'Project C', 'Project D'],
        'step1': ['4/10/2025', '3/5/2025', '5/1/2025', '7/20/2025'],
        'Very Long Step 2': ['8/17/2025', '3/12/2025', '5/8/2025', '7/28/2025'],
        'Very Very Long Step 3': ['10/25/2025', '3/20/2025', '5/17/2025', '8/4/2025'],
        'Very Very Very Long Step 4': ['12/30/2025', '3/28/2025', '5/24/2025', '8/10/2025'],
        'Very Very Very Long Step 5': ['2/4/2026', '4/5/2025', '6/1/2025', '8/18/2025'],
        'end': ['2/10/2026', '4/12/2025', '6/8/2025', '8/25/2025']
    }
)

subtasks = []
for i, col in enumerate(df.columns):
    if i > 0:
        if i < (len(df.columns) - 1):
            subtasks.append(col)
        df[col] = pd.to_datetime(df[col], format='%m/%d/%Y')

subtask_color = {
    subtask: COLORS[i] for i, subtask in enumerate(subtasks)
}

# Define timeline resolution
start_date = df.iloc[:, 1].min()
end_date = df['end'].max()

width = np.round(get_terminal_width() * 2).astype(int)
date_to_index = map_dates_to_timeline(start_date=start_date, end_date=end_date, width=width)

tick_dates = get_tick_dates(date_to_index=date_to_index, show_15=False)

# Print Gantt chart
print()
arrow = " ->    "
timeline_offset = " " * (15 + len(arrow))
tick_row = get_timeline(
    date_to_index=date_to_index, tick_dates=tick_dates, tick_symbol='\033[38;5;252m│\033[0m',
    line_symbol='\033[38;5;252m-\033[0m', show_labels=False, offset="\033[38;5;252m-\033[0m" * (15 + len(arrow)),
    end_line_symbol="\033[38;5;252m▶\033[0m"
    )

for idx, row in df.iterrows():
    bar = build_row(row, subtasks=subtasks)
    print(f"{row['project']:<15}{arrow}{bar}")
    if idx < (len(df) - 1):
        print(tick_row)

timeline = get_timeline(
    date_to_index=date_to_index, tick_dates=tick_dates, line_symbol="─", tick_symbol="┬", show_labels=True,
    offset=timeline_offset, end_line_symbol="▶"
    )
print(timeline)
print()

total_width = len(timeline.split("\n")[0])
legends = []
length = 0
s = ""
for subtask in subtasks:
    step_legth = len(subtask) + 7
    if (length + step_legth - 7) > total_width and len(s) > 0:
        legends.append((s[:-2], length - 3))
        length = 0
        s = ""
    s += subtask_color[subtask] * 3 + " " + subtask + "\033[0m" + "   "
    length += len(subtask) + 7

if len(s) > 0:
    legends.append((s[:-2], length - 3))

for legend in legends:
    print()
    center_gap = max(0, (total_width - legend[1]) // 2)
    print(" " * center_gap + legend[0] + " " * center_gap)
