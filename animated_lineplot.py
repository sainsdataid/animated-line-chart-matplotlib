import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import date

# data preparation
stocks = pd.read_csv("stocks_wide.csv")
stocks["Date"] = pd.to_datetime(stocks["Date"])
stocks = stocks.sort_values("Date", ascending=True).reset_index(drop=True)

colors = {"bbri": "#640303", "bbni": "c", "bmri": "orange"}

fig, ax = plt.subplots(figsize=(12, 8))

line_bank = {}
label_bank = {}


for bank in stocks.columns[1:]:
    # create lineplot for each stock code
    line_bank[bank] = plt.plot(
        stocks["Date"],
        stocks[bank],
        color=colors[bank],
        linewidth=2,
    )
    # create text for each stock code (BBRI, BBNI, BMRI)
    label_bank[bank] = ax.text(
        stocks["Date"][0],
        stocks[bank][0],
        bank.upper(),
        color=colors[bank],
        fontsize=13,
    )


quarter_text = ("Q1", "Q2", "Q3", "Q4")
mid_q = (
    date(2021, 2, 15),
    date(2021, 5, 15),
    date(2021, 8, 15),
    date(2021, 11, 15),
)

# add text at the middle of each quarter
for idx, q in enumerate(mid_q):
    ax.text(q, 7750, quarter_text[idx], fontsize=13, color="#4F4F4F")


# set plot title
ax.set_title(
    label="Stock Prices of State-Owned Banks (Indonesia 2021)",
    fontsize=15,
    fontweight="bold",
    fontfamily="arial",
    color="#0E2433",
    pad=15,
)

# set axis label
ax.set_ylabel("Price (Rupiah)", fontsize=13)

# limit lines X-Axis
start_date = date(2021, 1, 1)
end_date = date(2022, 1, 20)
plt.xlim(start_date, end_date)

# limit lines Y-Axis
plt.ylim(3000, 8000)


# setup background color for each quarter
start_q1 = date(2021, 1, 1)
start_q2 = date(2021, 4, 1)
start_q3 = date(2021, 7, 1)
start_q4 = date(2021, 10, 1)
start_pad = date(2022, 1, 1)
stop_pad = date(2022, 1, 20)

ax.axvspan(xmin=start_q1, xmax=start_q2, facecolor="#3BAFDA", alpha=0.2)
ax.axvspan(xmin=start_q2, xmax=start_q3, facecolor="#F3B0C3", alpha=0.2)
ax.axvspan(xmin=start_q3, xmax=start_q4, facecolor="orange", alpha=0.2)
ax.axvspan(xmin=start_q4, xmax=start_pad, facecolor="#55CBCD", alpha=0.2)
ax.axvspan(xmin=start_pad, xmax=stop_pad, facecolor="#EEEEEE")


def update(frame):
    """
    Function to update the data and visualization for each animation frame.

    Parameters:
        - frame (int): The current frame number.

    Returns:
        - lines dan text (tuple): The tuple of updated line and text objects.

    """
    cur_date = stocks["Date"][frame]

    for bank in label_bank:
        line_bank[bank][0].set_data(stocks["Date"][:frame], stocks[bank][:frame])
        label_bank[bank].set_position((cur_date, stocks[bank][frame]))

    # the animation function must return a sequence of Artist objects.
    return (
        line_bank["bbri"][0],
        line_bank["bbni"][0],
        line_bank["bmri"][0],
        label_bank["bbri"],
        label_bank["bbni"],
        label_bank["bmri"],
    )


#  setup animation
ani = FuncAnimation(
    fig, update, frames=len(stocks), interval=80, blit=True
)

## directly display the animation in dialog
# plt.show()

# Set the embed limit to a larger value (in MB)
plt.rcParams["animation.embed_limit"] = 100

# save the plot to javascript+html
ani_html = ani.to_jshtml()
with open("animation.html", "w") as f:
    f.write(ani_html)
