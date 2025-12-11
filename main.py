from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
               'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(6, 8))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbol + password_numbers
    shuffle(password_list)

    generate_password = "".join(password_list)
    password_input.insert(0, generate_password)
    pyperclip.copy(generate_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = username_input.get()
    password = password_input.get()

    if not website or not password or not email:
        messagebox.showinfo(title="Ooops", message="Please don't leave any fields empty")
        return

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    is_ok = messagebox.askokcancel(title=website, message=f"These are the message details entered: \n"
                                                          f" Email: {email}"
                                                          f"\nPassword: {password}\n"
                                                          f"is it Ok to save?")
    if not is_ok:
        return

    #---Load Existing data ----
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except (FileNotFoundError, ValueError ):
        with open("data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)

    else:
        # --- Update data ---
        data.update(new_data)

        # --- Save data back to file ---
        with open("data.json", "w") as data_file:
            # saving update data
            json.dump(data, data_file, indent=4)

    finally:
        # --- Clear fields ---
        website_input.delete(0, END)
        password_input.delete(0, END)


# --------------------------- Find Password -------------------------#
def find_password():
    website = website_input.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="error", message="No Data File Found!")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Info", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Info", message=f"{website} is not available in the saved passwords")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=100)

# --- Canvas (Logo) ---
canvas = Canvas(width=200, height=200)
locker_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_img)
canvas.grid(column=0, row=0, columnspan=3)

# --- Labels ---
Label(text="Website:").grid(column=0, row=1)
Label(text="Email/Username:").grid(column=0, row=2)
Label(text="Password:").grid(column=0, row=3)

# --- Entries ---
website_input = Entry()
website_input.grid(column=1, row=1)
website_input.focus()

username_input = Entry(width=35)
username_input.grid(column=1, row=2, columnspan=2)
username_input.insert(0, "gmail@suda.com")

password_input = Entry()
password_input.grid(column=1, row=3)

# --- Buttons ---
search_button = Button(text="Search", width=10, command=find_password)
search_button.grid(column=2, row=1)

generate_button = Button(text="Generate Pass", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=30, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
