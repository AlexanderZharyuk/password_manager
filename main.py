from tkinter import *
import pandas
import random
import pyperclip
import os.path
from tkinter import messagebox, ttk

COUNT = 0
FIRSTCLICK = True
check_base = os.path.isfile('data.csv')

if not check_base:
    first_row = ['Login', 'Site', 'Pass']
    user_base = pandas.DataFrame(columns=first_row)
    user_base.to_csv('data.csv', index=False)


def save_profile():
    login = login_entry.get()
    site = site_entry.get()
    password = generated_pass.cget('text')
    if site_entry.get() == '' or site_entry.get() == 'Write the site' or login_entry.get() == '' \
            or login_entry.get() == 'Write the login' or generated_pass.cget('text') == '' \
            or generated_pass.cget('text') == 'GEN PASSWORD':
        messagebox.showerror(title='Profile not saved', message='Please don"t leave fields empty')
    else:
        user_profiles = pandas.read_csv('data.csv')
        user_sites = user_profiles['Site'].to_list()
        if site in user_sites:
            messagebox.showerror(title='Profile not saved', message='This site already in database!')
        else:
            is_ok = messagebox.askokcancel(title='Approve the changes', message=f'Site: {site}\nLogin: {login}'
                                                                                f'\nPassword: {password}'
                                                                                f'\nDo you want add new profile?')
            if is_ok:
                row = [login, site, password]
                user_profiles = user_profiles.append(pandas.DataFrame([row], index=[COUNT],
                                                                      columns=['Login', 'Site', 'Pass']))
                user_profiles.to_csv('data.csv', index=False)
                confirm_label.config(text='Profile saved', fg='green', font=('Arial', 10, 'bold'))

    generated_pass.config(text='')
    site_entry.delete(0, END)
    login_entry.delete(0, END)
    site_entry.focus()


def copy_password():
    password = generated_pass.cget('text')
    pyperclip.copy(password)


def copy_login_rightside():
    login = login_label.cget('text')
    pyperclip.copy(login)


def copy_pass_rightside():
    password = pass_label.cget('text')
    pyperclip.copy(password)


def generate_password():
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '1234567890'
    symbols = '!#$%&'
    password = []
    letters = [password.append(random.choice(alphabet)) for letter in range(5)]
    nums = [password.append(random.choice(numbers)) for num in range(3)]
    syml = [password.append(random.choice(symbols)) for sym in range(4)]
    random.shuffle(password)
    password_string = ''.join(password)
    generated_pass.config(text=password_string, fg='black')


def on_site_click(event):
    global FIRSTCLICK
    if FIRSTCLICK:
        site_entry.delete(0, "end")
        site_entry.config(fg='black')


def on_login_click(event):
    global FIRSTCLICK
    if FIRSTCLICK:
        login_entry.delete(0, "end")
        login_entry.config(fg='black')


def find_profile():
    base = pandas.read_csv('data.csv')
    dict_with_data = {row.Site:(row.Login, row.Pass) for (index, row) in base.iterrows()}
    try:
        login_label.config(text=dict_with_data[list_with_sites.get()][0], fg='black', font=('Arial', 8, 'bold'))
        pass_label.config(text=dict_with_data[list_with_sites.get()][1], fg='black', font=('Arial', 8, 'bold'))
    except KeyError:
        pass

# GI SETUP
# ------------------------------------LEFT SIDE------------------------------------
window = Tk()
window.geometry('+480+200')
window.config(width=1000, height=550, bg='#8fcdff', pady=70, padx=60)
window.maxsize(width=1000, height=550)
window.minsize(width=1000, height=550)
window.title('PASSWORD GENERATOR')

canvas = Canvas(width=150, height=150, bg='#8fcdff', highlightthickness=0)
pass_img = PhotoImage(file='pass_image.png')
canvas.create_image(80, 77, image=pass_img)
canvas.grid(row=0, column=1, padx=100)

# SITE LABEL
site_label = Label()
site_label.config(text='SITE:', font=('Arial', 10, 'italic'), bg='#8fcdff')
site_label.grid(row=1, column=1, padx=70, sticky='w')

# SITE ENTRY
site_entry = Entry()
site_entry.insert(0, 'Write the site')
site_entry.bind('<FocusIn>', on_site_click)
site_entry.config(fg='grey', width=35, justify='center')
site_entry.grid(row=2, column=1)

# SITE LABEL
site_label = Label()
site_label.config(text='LOGIN:', font=('Arial', 10, 'italic'), bg='#8fcdff')
site_label.grid(row=3, column=1, padx=70, sticky='w')

# LOGIN ENTRY
login_entry = Entry()
login_entry.insert(0, 'Write the login')
login_entry.bind('<FocusIn>', on_login_click)
login_entry.config(fg='grey', width=35, justify='center')
login_entry.grid(row=4, column=1)

# GEN PASS LABEL
generated_pass = Label()
generated_pass.config(fg='grey', width=30, height=1, justify='center', text='GEN PASSWORD')
generated_pass.grid(row=5, column=1, pady=15)

# BUTTONS LEFT SIDE
generate_button = Button()
generate_button.config(text='Generate', command=generate_password)
generate_button.grid(row=6, column=1, sticky='w', padx=65)

copy_button = Button()
copy_button.config(text='Copy', command=copy_password, height=1)
copy_button.grid(row=5, column=1, sticky='e', padx=65)

# SAVE BUTTON
save_button = Button()
save_button.config(text='SAVE PROFILE', command=save_profile)
save_button.grid(row=6, column=1, sticky='e', padx=65)


# ACCESS OR DENY LABEL
confirm_label = Label()
confirm_label.config(text='', font=('Arial', 10, 'italic'), bg='#8fcdff')
confirm_label.grid(row=7, column=1)
# -----------------------------------RIGHT SIDE------------------------------------
sep = ttk.Separator(window, orient=VERTICAL)
sep.grid(row=0, column=2, padx=100, sticky='ns', rowspan=10)

# CHOOSE SITE
database = pandas.read_csv('data.csv')
sites = database['Site'].to_list()
list_with_sites = ttk.Combobox(window, values=sites, width=30, justify='center')
list_with_sites.grid(row=2, column=3, columnspan=3, padx=45)

# CHOOSE SITE LABEL
choose_site_label = Label(text='CHOOSE SITE', bg="#8fcdff", font=('Arial', 10, 'italic'))
choose_site_label.grid(row=1, column=3, columnspan=3, padx=45, sticky='s')

# FIND BUTTON
find_button = Button(text='FIND!', command=find_profile)
find_button.grid(row=3, column=3, columnspan=3, pady=4)

# LOGIN LABEL RIGHT LABEL
login_label = Label(text='LOGIN', font=('Arial', 8, 'italic'), width=15, fg='grey')
login_label.grid(row=5, column=3, padx=1, sticky='e')

# PASS LABEL RIGHT LABEL
pass_label = Label(text='PASS', font=('Arial', 8, 'italic'), width=15, fg='grey')
pass_label.grid(row=6, column=3, padx=1, sticky='e')

# RIGTHSIDE BUTTON
login_right_side_copy = Button()
login_right_side_copy.config(text='Copy', command=copy_login_rightside)
login_right_side_copy.grid(row=5, column=4, padx=15, sticky='w')

# RIGHTSIDE COPY PASS BUTTON
login_right_side_copy_pass = Button()
login_right_side_copy_pass.config(text='Copy', command=copy_pass_rightside)
login_right_side_copy_pass.grid(row=6, column=4, padx=15, sticky='w')

window.mainloop()

