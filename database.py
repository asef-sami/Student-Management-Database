from tkinter import*
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
from PIL import ImageTk
from PIL import Image
import ttkthemes
import time
import pymysql
import pandas as pd

#main window
window = ttkthemes.ThemedTk()
window.get_themes()
window.set_theme('breeze')

window.geometry("1350x720+100+40")
window.title("Student Database")
window.configure(bg="white")

#========Functions------
# text slider
cnt = 0
text=''
def slidename():
    global text, cnt
    text = text + st[cnt]
    slider_label.config(text=text)
    cnt+=1
    slider_label.after(400,slidename)


#date & time
def myclock():
    currdate = time.strftime('%d.%m.%Y')
    currtime = time.strftime('%H:%M:%S')
    #print(currdate,currtime)
    datetime_label.config(text=f'  Date: {currdate}\nTime: {currtime}')
    datetime_label.after(1000,myclock)

# Connect Databse

def connectDB():

    def connect():
        global mycursor,conn
        try:
            conn = pymysql.connect(host=host_entry.get(), user=username_entry.get(), password=pass_entry.get())
            #direct to work on project
            #conn = pymysql.connect(host='localhost', user='root', password='1234')
            #localhost, root, 1234 (expected from sami)
            mycursor = conn.cursor()
        except:
            messagebox.showerror('ERROR!','Wrong Password!',parent=connectWin)
            return
        try:
            query = 'CREATE DATABASE school'
            mycursor.execute(query)

            query = 'USE school'
            mycursor.execute(query)

            query= 'CREATE TABLE student (Id INT NOT NULL PRIMARY KEY, RegistrationNo VARCHAR(30), Name VARCHAR(255), Class VARCHAR(50), DOB DATE, Gender VARCHAR(10), Email VARCHAR(255), Contact VARCHAR(15), BloodGroup VARCHAR(5), Address VARCHAR(255))'
            mycursor.execute(query)
        except:
            query = 'USE school'
            mycursor.execute(query)

        messagebox.showinfo('Success','Database connection is complete',parent=connectWin)
        connectWin.destroy()
        addstubtn.config(state=NORMAL)
        srcstubtn.config(state=NORMAL)
        delstubtn.config(state=NORMAL)
        upstubtn.config(state=NORMAL)
        showstubtn.config(state=NORMAL)
        exstubtn.config(state=NORMAL)


    connectWin = Toplevel()
    connectWin.grab_set()
    connectWin.geometry('480x250+700+230')
    connectWin.configure(bg='white')
    connectWin.title('Connect with Database')

    #Host Name
    hostname_label = Label(connectWin, text='Host Name:', font=('arial',20,'bold'),bg='white')
    hostname_label.grid(row=0,column=0,padx=25,pady=10)
    host_entry = Entry(connectWin,font=('arial',15),bd=2)
    host_entry.grid(row=0, column=1, padx=20, pady=10)

    #Username
    username_label = Label(connectWin, text='Username:', font=('arial',20,'bold'),bg='white')
    username_label.grid(row=1,column=0,padx=25,pady=10)
    username_entry = Entry(connectWin,font=('airal',15),bd=2)
    username_entry.grid(row=1, column=1, padx=20, pady=10)

    #PassWord
    pass_label = Label(connectWin, text='Password:', font=('arial',20,'bold'),bg='white')
    pass_label.grid(row=2,column=0,padx=25,pady=10)
    pass_entry = Entry(connectWin,font=('arial',15),bd=2, show="*")
    pass_entry.grid(row=2, column=1, padx=20, pady=20)

    #Connect Button
    conn_btn = ttk.Button(connectWin, text ='CONNECT',width=12, command=connect)
    conn_btn.grid(row=3, column=0, columnspan=2, pady=11)

#Show Student Function
def show_student():
    query = 'SELECT * FROM student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    student_table.delete(*student_table.get_children())
    for data in fetched_data:
        student_table.insert('', END, values=data)


# Add Student func

def add_student():
    def add_data():
        if id_entry.get() == '' or reg_entry.get() == '' or name_entry.get() == '' or class_entry.get() == '' or dob_entry.get() == '' or gender_entry.get() == '' or email_entry.get() == '' or contact_entry.get() == '' or blood_group_entry.get() == '' or address_entry.get() == '':
            messagebox.showerror('ERROR!', 'Please fill all information', parent=addwin)
        else:
            try:
                query = "INSERT INTO student (Id, RegistrationNo, Name, Class, DOB, Gender, Email, Contact, BloodGroup, Address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (
                    id_entry.get(),
                    reg_entry.get(),
                    name_entry.get(),
                    class_entry.get(),
                    dob_entry.get(),
                    gender_entry.get(),
                    email_entry.get(),
                    contact_entry.get(),
                    blood_group_entry.get(),
                    address_entry.get()
                )
                mycursor.execute(query, data)
                conn.commit()
                res = messagebox.askyesno('Confirm!','Data added successfully. Do you want to clean from?')
                if res:
                    # List of entry widgets
                    entry_fields = [id_entry, reg_entry, name_entry, class_entry, dob_entry, gender_entry, email_entry, contact_entry, blood_group_entry, address_entry]

                    # Clear all entry fields
                    for entry in entry_fields:
                        entry.delete(0, END)
                else:
                    pass
            except:
                messagebox.showerror('Error!','Duplicate Id is not alowed',parent=addwin)
            
            show_student()

    addwin = Toplevel()
    addwin.grab_set()
    addwin.geometry('480x600+200+150')
    addwin.configure(bg='white')
    addwin.title('Add student in Database')

    #Id
    id_label = Label(addwin,text='Id',font=('arial',15,'bold'),bg='white')
    id_label.grid(row=0,column=0,padx=15,pady=10)
    id_entry = Entry(addwin,font=('arial',15),bg='white')
    id_entry.grid(row=0,column=1,padx=15,pady=10)
    # Registration No
    reg_label = Label(addwin, text='Registration No', font=('arial', 15, 'bold'), bg='white')
    reg_label.grid(row=1, column=0, padx=15, pady=10)
    reg_entry = Entry(addwin, font=('arial', 15), bg='white')
    reg_entry.grid(row=1, column=1, padx=15, pady=10)

    # Name
    name_label = Label(addwin, text='Name', font=('arial', 15, 'bold'), bg='white')
    name_label.grid(row=2, column=0, padx=15, pady=10)
    name_entry = Entry(addwin, font=('arial', 15), bg='white')
    name_entry.grid(row=2, column=1, padx=15, pady=10)

    # Class
    class_label = Label(addwin, text='Class', font=('arial', 15, 'bold'), bg='white')
    class_label.grid(row=3, column=0, padx=15, pady=10)
    class_entry = Entry(addwin, font=('arial', 15), bg='white')
    class_entry.grid(row=3, column=1, padx=15, pady=10)

    # D.O.B
    dob_label = Label(addwin, text='D.O.B', font=('arial', 15, 'bold'), bg='white')
    dob_label.grid(row=4, column=0, padx=15, pady=10)
    dob_entry = Entry(addwin, font=('arial', 15), bg='white')
    dob_entry.grid(row=4, column=1, padx=15, pady=10)

    # Gender
    gender_label = Label(addwin, text='Gender', font=('arial', 15, 'bold'), bg='white')
    gender_label.grid(row=5, column=0, padx=15, pady=10)
    gender_entry = Entry(addwin, font=('arial', 15), bg='white')
    gender_entry.grid(row=5, column=1, padx=15, pady=10)

    # Email
    email_label = Label(addwin, text='Email', font=('arial', 15, 'bold'), bg='white')
    email_label.grid(row=6, column=0, padx=15, pady=10)
    email_entry = Entry(addwin, font=('arial', 15), bg='white')
    email_entry.grid(row=6, column=1, padx=15, pady=10)

    # Contact
    contact_label = Label(addwin, text='Contact', font=('arial', 15, 'bold'), bg='white')
    contact_label.grid(row=7, column=0, padx=15, pady=10)
    contact_entry = Entry(addwin, font=('arial', 15), bg='white')
    contact_entry.grid(row=7, column=1, padx=15, pady=10)

    # Blood Group
    blood_group_label = Label(addwin, text='Blood Group', font=('arial', 15, 'bold'), bg='white')
    blood_group_label.grid(row=8, column=0, padx=15, pady=10)
    blood_group_entry = Entry(addwin, font=('arial', 15), bg='white')
    blood_group_entry.grid(row=8, column=1, padx=15, pady=10)

    # Address
    address_label = Label(addwin, text='Address', font=('arial', 15, 'bold'), bg='white')
    address_label.grid(row=9, column=0, padx=15, pady=10)
    address_entry = Entry(addwin, font=('arial', 15), bg='white')
    address_entry.grid(row=9, column=1, padx=15, pady=10)

    #Button to add
    add_btn = ttk.Button(addwin, text = 'ADD',width=15,command=add_data)
    add_btn.grid(row=10,columnspan=2,padx=15,pady=20)

# Search Student Func
def search_student():
    def src_data():
        # Get values from Entry widgets
        id_value = id1_entry.get()
        reg_value = reg1_entry.get()
        name_value = name1_entry.get()
        class_value = class1_entry.get()
        dob_value = dob1_entry.get()
        gender_value = gender1_entry.get()
        email_value = email1_entry.get()
        contact_value = contact1_entry.get()
        blood_group_value = blood1_group_entry.get()
        address_value = address1_entry.get()

        # Construct the SQL query
        query = 'SELECT * FROM student WHERE '
        conditions = []

        if id_value:
            conditions.append(f'Id = {id_value}')
        if reg_value:
            conditions.append(f'RegistrationNo = "{reg_value}"')
        if name_value:
            conditions.append(f'Name = "{name_value}"')
        if class_value:
            conditions.append(f'Class = "{class_value}"')
        if dob_value:
            conditions.append(f'DOB = "{dob_value}"')
        if gender_value:
            conditions.append(f'Gender = "{gender_value}"')
        if email_value:
            conditions.append(f'Email = "{email_value}"')
        if contact_value:
            conditions.append(f'Contact = "{contact_value}"')
        if blood_group_value:
            conditions.append(f'BloodGroup = "{blood_group_value}"')
        if address_value:
            conditions.append(f'Address = "{address_value}"')

        query += ' OR '.join(conditions)

        # Execute the query
        mycursor.execute(query)

        student_table.delete(*student_table.get_children())
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            student_table.insert('', END, values=data)

    srcwin = Toplevel()
    srcwin.grab_set()
    srcwin.geometry('480x600+200+150')
    srcwin.configure(bg='white')
    srcwin.title('Search Student')

    #Id
    id1_label = Label(srcwin,text='Id',font=('arial',15,'bold'),bg='white')
    id1_label.grid(row=0,column=0,padx=15,pady=10)
    id1_entry = Entry(srcwin,font=('arial',15),bg='white')
    id1_entry.grid(row=0,column=1,padx=15,pady=10)

    # Registration No
    reg1_label = Label(srcwin, text='Registration No', font=('arial', 15, 'bold'), bg='white')
    reg1_label.grid(row=1, column=0, padx=15, pady=10)
    reg1_entry = Entry(srcwin, font=('arial', 15), bg='white')
    reg1_entry.grid(row=1, column=1, padx=15, pady=10)

    # Name
    name1_label = Label(srcwin, text='Name', font=('arial', 15, 'bold'), bg='white')
    name1_label.grid(row=2, column=0, padx=15, pady=10)
    name1_entry = Entry(srcwin, font=('arial', 15), bg='white')
    name1_entry.grid(row=2, column=1, padx=15, pady=10)

    # Class
    class1_label = Label(srcwin, text='Class', font=('arial', 15, 'bold'), bg='white')
    class1_label.grid(row=3, column=0, padx=15, pady=10)
    class1_entry = Entry(srcwin, font=('arial', 15), bg='white')
    class1_entry.grid(row=3, column=1, padx=15, pady=10)

    # D.O.B
    dob1_label = Label(srcwin, text='D.O.B', font=('arial', 15, 'bold'), bg='white')
    dob1_label.grid(row=4, column=0, padx=15, pady=10)
    dob1_entry = Entry(srcwin, font=('arial', 15), bg='white')
    dob1_entry.grid(row=4, column=1, padx=15, pady=10)

    # Gender
    gender1_label = Label(srcwin, text='Gender', font=('arial', 15, 'bold'), bg='white')
    gender1_label.grid(row=5, column=0, padx=15, pady=10)
    gender1_entry = Entry(srcwin, font=('arial', 15), bg='white')
    gender1_entry.grid(row=5, column=1, padx=15, pady=10)

    # Email
    email1_label = Label(srcwin, text='Email', font=('arial', 15, 'bold'), bg='white')
    email1_label.grid(row=6, column=0, padx=15, pady=10)
    email1_entry = Entry(srcwin, font=('arial', 15), bg='white')
    email1_entry.grid(row=6, column=1, padx=15, pady=10)

    # Contact
    contact1_label = Label(srcwin, text='Contact', font=('arial', 15, 'bold'), bg='white')
    contact1_label.grid(row=7, column=0, padx=15, pady=10)
    contact1_entry = Entry(srcwin, font=('arial', 15), bg='white')
    contact1_entry.grid(row=7, column=1, padx=15, pady=10)

    # Blood Group
    blood1_group_label = Label(srcwin, text='Blood Group', font=('arial', 15, 'bold'), bg='white')
    blood1_group_label.grid(row=8, column=0, padx=15, pady=10)
    blood1_group_entry = Entry(srcwin, font=('arial', 15), bg='white')
    blood1_group_entry.grid(row=8, column=1, padx=15, pady=10)

    # Address
    address1_label = Label(srcwin, text='Address', font=('arial', 15, 'bold'), bg='white')
    address1_label.grid(row=9, column=0, padx=15, pady=10)
    address1_entry = Entry(srcwin, font=('arial', 15), bg='white')
    address1_entry.grid(row=9, column=1, padx=15, pady=10)

    #Button to add
    src_btn = ttk.Button(srcwin, text = 'SEARCH',width=15,command=src_data)
    src_btn.grid(row=10,columnspan=2,padx=15,pady=20)

# Delete Student func
def del_stu():
    indexing = student_table.focus()
    content = student_table.item(indexing)
    content_id = content['values'][0]
    query = 'DELETE FROM student WHERE Id = %s'
    mycursor.execute(query, (content_id,))
    conn.commit()
    messagebox.showinfo('Deleted', f'Data of {content_id} is deleted.')

    show_student()

#Update Student

def update_stu():

    def update_data():
        # Get the values from the entry fields
        id_value = idu_entry.get()
        reg_value = regu_entry.get()
        name_value = nameu_entry.get()
        class_value = classu_entry.get()
        dob_value = dobu_entry.get()
        gender_value = genderu_entry.get()
        email_value = emailu_entry.get()
        contact_value = contactu_entry.get()
        blood_group_value = bloodu_group_entry.get()
        address_value = addressu_entry.get()

        # Execute the SQL update query
        query = 'UPDATE student SET RegistrationNo=%s, Name=%s, Class=%s, DOB=%s, Gender=%s, Email=%s, Contact=%s, BloodGroup=%s, Address=%s WHERE Id=%s'
        data = (reg_value, name_value, class_value, dob_value, gender_value, email_value, contact_value, blood_group_value, address_value, id_value)
        
        try:
            mycursor.execute(query, data)
            conn.commit()
            messagebox.showinfo("Success", "Data updated successfully")
            show_student()
            updateWin.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error: {str(e)}")


    updateWin = Toplevel()
    updateWin.grab_set()
    updateWin.geometry('480x600+200+150')
    updateWin.configure(bg='white')
    updateWin.title('Update Data')

    # Id
    idu_label = Label(updateWin, text='Id', font=('arial', 15, 'bold'), bg='white')
    idu_label.grid(row=0, column=0, padx=15, pady=10)
    idu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    idu_entry.grid(row=0, column=1, padx=15, pady=10)

    # Registration No
    regu_label = Label(updateWin, text='Registration No', font=('arial', 15, 'bold'), bg='white')
    regu_label.grid(row=1, column=0, padx=15, pady=10)
    regu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    regu_entry.grid(row=1, column=1, padx=15, pady=10)

    # Name
    nameu_label = Label(updateWin, text='Name', font=('arial', 15, 'bold'), bg='white')
    nameu_label.grid(row=2, column=0, padx=15, pady=10)
    nameu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    nameu_entry.grid(row=2, column=1, padx=15, pady=10)

    # Class
    classu_label = Label(updateWin, text='Class', font=('arial', 15, 'bold'), bg='white')
    classu_label.grid(row=3, column=0, padx=15, pady=10)
    classu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    classu_entry.grid(row=3, column=1, padx=15, pady=10)

    # D.O.B
    dobu_label = Label(updateWin, text='D.O.B', font=('arial', 15, 'bold'), bg='white')
    dobu_label.grid(row=4, column=0, padx=15, pady=10)
    dobu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    dobu_entry.grid(row=4, column=1, padx=15, pady=10)

    # Gender
    genderu_label = Label(updateWin, text='Gender', font=('arial', 15, 'bold'), bg='white')
    genderu_label.grid(row=5, column=0, padx=15, pady=10)
    genderu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    genderu_entry.grid(row=5, column=1, padx=15, pady=10)

    # Email
    emailu_label = Label(updateWin, text='Email', font=('arial', 15, 'bold'), bg='white')
    emailu_label.grid(row=6, column=0, padx=15, pady=10)
    emailu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    emailu_entry.grid(row=6, column=1, padx=15, pady=10)

    # Contact
    contactu_label = Label(updateWin, text='Contact', font=('arial', 15, 'bold'), bg='white')
    contactu_label.grid(row=7, column=0, padx=15, pady=10)
    contactu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    contactu_entry.grid(row=7, column=1, padx=15, pady=10)

    # Blood Group
    bloodu_group_label = Label(updateWin, text='Blood Group', font=('arial', 15, 'bold'), bg='white')
    bloodu_group_label.grid(row=8, column=0, padx=15, pady=10)
    bloodu_group_entry = Entry(updateWin, font=('arial', 15), bg='white')
    bloodu_group_entry.grid(row=8, column=1, padx=15, pady=10)

    # Address
    addressu_label = Label(updateWin, text='Address', font=('arial', 15, 'bold'), bg='white')
    addressu_label.grid(row=9, column=0, padx=15, pady=10)
    addressu_entry = Entry(updateWin, font=('arial', 15), bg='white')
    addressu_entry.grid(row=9, column=1, padx=15, pady=10)

    # Button to add
    update_btn = ttk.Button(updateWin, text='UPDATE', width=15, command=update_data)
    update_btn.grid(row=10, columnspan=2, padx=15, pady=20)

    indexing = student_table.focus()
    content=student_table.item(indexing)

    listdata = content['values']
    idu_entry.insert(0, listdata[0])
    regu_entry.insert(0, listdata[1])
    nameu_entry.insert(0, listdata[2])
    classu_entry.insert(0, listdata[3])
    dobu_entry.insert(0, listdata[4])
    genderu_entry.insert(0, listdata[5])
    emailu_entry.insert(0, listdata[6])
    contactu_entry.insert(0, listdata[7])
    bloodu_group_entry.insert(0, listdata[8])
    addressu_entry.insert(0, listdata[9])

#Export Data func

# Export Data func
def export_data():
    # Ask the user for a file location
    url = filedialog.asksaveasfilename(defaultextension='.csv')

    indexing = student_table.get_children()

    newlist = []
    for index in indexing:
        content = student_table.item(index)
        datalist = content['values']
        newlist.append(datalist)


    df = pd.DataFrame(newlist, columns=['Id', 'RegistrationNo', 'Name', 'Class', 'DOB', 'Gender', 'Email', 'Contact', 'BloodGroup', 'Address'])

    df.to_csv(url, index=False)

    # Show a success message
    messagebox.showinfo('Success', 'Data is saved to a CSV file.')


#Exit Functions
def bye():
    res = messagebox.askyesno('Confirm','Do you want to Loguot Sami?')
    if res:
        window.destroy()
    else:
        pass
#========--------------

#---------GUi database-----

#date time
datetime_label = Label(window,font=('Arial',20,'bold'),bg='white')
datetime_label.place(x=5,y=5)
myclock()

#database name
st = 'Student Management Database'
slider_label = Label(window, text=st, font=('times new roman', 35, 'italic bold'), bg='white')
slider_label.place(x=400, y=0)
slidename()

#connect Database buttun
style = ttk.Style()
style.configure("Connect.TButton", font=("Arial", 12), width=60, bd=2)
connectdbbtn = ttk.Button(window, text='Connect with Database', style="Connect.TButton",command=connectDB)
connectdbbtn.place(x=1100, y=12)

# Button frame (left)--------------------------
button_frame = Frame(window, bg='white')
button_frame.place(x=30, y=80, width=350, height=620)

# Logo pic
logo_image = Image.open("wdb.png")
logo_image = ImageTk.PhotoImage(logo_image)
logo_label = Label(button_frame, image=logo_image, bg='white')
logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


# Button design
stl = ttk.Style()
stl.configure("Connect.TButton", font=("Arial", 10), width=25)

# Create a spacer column to center the buttons
button_frame.columnconfigure(1, weight=1)

# Add student Button
addstubtn = ttk.Button(button_frame, text='Add Student', style="Connect.TButton",state=DISABLED, command=add_student)
addstubtn.grid(row=1, column=1, padx=10, pady=15)

# Search student Button
srcstubtn = ttk.Button(button_frame, text='Search Student', style="Connect.TButton",state=DISABLED, command= search_student)
srcstubtn.grid(row=2, column=1, padx=10, pady=15)

# Delete student Button
delstubtn = ttk.Button(button_frame, text='Delete Student', style="Connect.TButton",state=DISABLED, command=del_stu)
delstubtn.grid(row=3, column=1, padx=10, pady=15)

# Update student Button
upstubtn = ttk.Button(button_frame, text='Update Student', style="Connect.TButton",state=DISABLED, command=update_stu)
upstubtn.grid(row=4, column=1, padx=10, pady=15)

# Show student Button
showstubtn = ttk.Button(button_frame, text='Show All Student', style="Connect.TButton",state=DISABLED, command=show_student)
showstubtn.grid(row=5, column=1, padx=10, pady=15)

# Export student Button
exstubtn = ttk.Button(button_frame, text='Export Data', style="Connect.TButton",state=DISABLED, command=export_data)
exstubtn.grid(row=6, column=1, padx=10, pady=15)

# Exit Button
exitbtn = ttk.Button(button_frame, text='Logout', style="Connect.TButton",command=bye)
exitbtn.grid(row=7, column=1, padx=10, pady=15)
#--------------------------------------------------

# Right frame (data)--------------------------
data_frame = Frame(window, bg='white')
data_frame.place(x=390, y=80, width=930, height=620)

# Scroll Bar
x_scrool = tk.Scrollbar(data_frame, orient=tk.HORIZONTAL)
y_scrool = tk.Scrollbar(data_frame, orient=tk.VERTICAL)

# Grid info
student_table = ttk.Treeview(data_frame, columns=('Id','Registration No','Name','Class','D.O.B','Gender','Email','Contact','Blood Group','Address'),
                             xscrollcommand=x_scrool.set, yscrollcommand=y_scrool.set)


# Make the Treeview headings clickable
student_table.heading("Id", text="Id")
student_table.heading("Registration No", text="Registration No")
student_table.heading("Name", text="Name")
student_table.heading("Class", text="Class")
student_table.heading("D.O.B", text="D.O.B")
student_table.heading("Gender", text="Gender")
student_table.heading("Email", text="Email")
student_table.heading("Contact", text="Contact")
student_table.heading("Blood Group", text="Blood Group")
student_table.heading("Address", text="Address")

student_table['show'] = 'headings'

# Set the column widths
student_table.column("Id", width=100, anchor=CENTER)
student_table.column("Registration No", width=150, anchor=CENTER)
student_table.column("Name", width=210,)
student_table.column("Class", width=100, anchor=CENTER)
student_table.column("D.O.B", width=120, anchor=CENTER)
student_table.column("Gender", width=100, anchor=CENTER)
student_table.column("Email", width=220,)
student_table.column("Contact", width=120, anchor=CENTER)
student_table.column("Blood Group", width=120, anchor=CENTER)
student_table.column("Address", width=250, anchor=CENTER)

#set Column style
sty=ttk.Style()
sty.configure('Treeview',rowhight=50,font=('Arial',11),background='white',fieldbackground='turquiise1')
sty.configure('Treeview.Heading',font=('Arial',12,'bold'))

# Configure the Scrollbars to scroll the Treeview
x_scrool.config(command=student_table.xview)
y_scrool.config(command=student_table.yview)

# Pack the Scrollbars and Treeview widget
x_scrool.pack(side=tk.BOTTOM, fill=tk.X)
y_scrool.pack(side=tk.RIGHT, fill=tk.Y)
student_table.pack(fill=tk.BOTH, expand=True)

#++++++++++++++++++++++++++++++++++++++++++++

window.mainloop()