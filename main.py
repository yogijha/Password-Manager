from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_name = website_entry.get()
    if len(website_name) == 0:
        messagebox.showinfo(title="Error", message=f"Please enter website name")
    else:
        try:
            with open("data.json", "r") as data_file:
                all_data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No details found.")
        else:
            if website_name in all_data:
                username = all_data[website_name]["email"]
                password = all_data[website_name]["password"]
                password_entry.insert(0, password)
                messagebox.showinfo(title=f"{website_name}", message=f"Email : {username}\nPassword : {password}")
            else:
                messagebox.showinfo(title="Website", message="No details for the website exist.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    password = "".join(str(v) for v in password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0:
        messagebox.showinfo(title="Website", message="Website field is empty.")
    elif len(password) == 0:
        messagebox.showinfo(title="Password", message="Password field is empty.")
    elif len(email) == 0:
        messagebox.showinfo(title="Email", message="Email field is empty.")
    else:
        is_ok = messagebox.askokcancel(title=f"{website}", message=f"Thsese are the entered information.\n"
                                                                   f"Email : {email}\nPassword : {password}\n"
                                                                   f"Is this ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    #reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    #add first data
                    json.dump(new_data, data_file, indent=4)
            else:
                #update old data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    #saving updated data
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

windows = Tk()
windows.title("Password Generator")
windows.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
photo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "example@email.com")
password_entry = Entry(width=35)
password_entry.grid(row=3, column=1, columnspan=2)

generate_password_button = Button(text="generate password", command=generate_password)
generate_password_button.grid(row=3, column=3, columnspan=1)

add_button = Button(text="Add", width=10, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=3, columnspan=1)

windows.mainloop()
