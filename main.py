from tkinter import*
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image

#main window
win = Tk()
win.geometry("1450x720+40+40")
win.title("Login into Student Database")
win.configure(bg="white")

#-----------------------------Login Page

#fuction to press login
def login_bf():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error!", "Please enter username and password.")
    elif username=='sami' and password=='1234':
        messagebox.showinfo('Successful','Welcome Back Sami')
        win.destroy()
        import database
    else:
        messagebox.showerror("Error!", "Invalid username or passwor")

# Create a login frame
login_frame = Frame(win, bg="white")
login_frame.place(relx=0.5, rely=0.2, anchor="n")

# Logo
logo_img = Image.open("group.png")
logo_img = ImageTk.PhotoImage(logo_img)
logo_label = Label(login_frame, image=logo_img, bg="white")
logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

# Username Entry
username_img = Image.open("user.png") 
username_img = ImageTk.PhotoImage(username_img)
username_label = Label(login_frame, image=username_img, text="Username", compound=LEFT, bg="white", font=("Arial", 18, "bold"))
username_label.grid(row=1, column=0, padx=(20, 0))
username_entry = Entry(login_frame, font=("Arial", 18), bd=3)
username_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky=W + E)

# Password Entry
password_img = Image.open("padlock.png")
password_img = ImageTk.PhotoImage(password_img)
password_label = Label(login_frame, image=password_img, text="Password", compound=LEFT, bg="white", font=("Arial", 18, "bold"))
password_label.grid(row=2, column=0, padx=(20, 0))
password_entry = Entry(login_frame, font=("Arial", 18), bd=3, show="*")
password_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky=W + E)

# Login Button
login_btn = Button(login_frame, text="Login", font=("Arial", 14, "bold"),
                    bg="deepskyblue2", fg="white", bd=3, padx=20, width=10,
                    activebackground="deepskyblue2", activeforeground="white",
                    cursor = 'hand2', command = login_bf)
login_btn.grid(row=3, column=0, columnspan=2, pady=(20, 10))

# Forgot Password Button
forgot_btn = Button(login_frame, text="Forgot your password?", font=("Arial", 10, "bold"), bg="white", bd=0, fg="blue", cursor = 'hand2')
forgot_btn.grid(row=4, column=0, columnspan=2, pady=10)
#-----------------------------------ebdl login-

win.mainloop()