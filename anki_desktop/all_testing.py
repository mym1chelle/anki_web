import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window(size=(500, 500))

gauge = ttk.Floodgauge(
    bootstyle=INFO,
    font=(None, 24, 'bold'),
    mask='Memory Used {}%',
)
gauge.pack(fill=BOTH, expand=YES, padx=10, pady=10)



gauge.start()
#
# gauge.stop()


app.mainloop()
