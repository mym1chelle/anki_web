import tkinter as tk
from login_logout_user import LoginLogOutUser
from utils import root, take_window_of_center


win_width = 600
win_height = 500
center_width, center_height = take_window_of_center(win_width, win_height)
root.title('Anki v.1.0')
root.geometry(f"{win_width}x{win_height}+{center_width}+{center_height}")
menu = tk.Menu(root)
root.config(menu=menu)
auth_user = tk.Menu(menu)
login = LoginLogOutUser(root, auth_user)
menu.add_cascade(label='Authorization', menu=auth_user)
auth_user.add_command(label='Log In', command=lambda: login.login_user())
auth_user.add_command(label='Registration', command=lambda: login.registration_form())
auth_user.add_command(label='Log Out', command=lambda: login.logout())
auth_user.entryconfig('Log Out', state='disabled')

root.mainloop()
