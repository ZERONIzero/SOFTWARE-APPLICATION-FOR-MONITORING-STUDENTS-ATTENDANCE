import customtkinter as ct
import os
from PIL import Image
from PIL import ImageTk
from bd import db

ct.set_appearance_mode("system")
ct.set_default_color_theme("blue")

app = ct.CTk()
app.minsize(800,500)
app.title("Инструмент для работы с БД")
app.wm_iconbitmap()
icopath = ImageTk.PhotoImage(file = ("./src/student.png"))
app.iconphoto(False, icopath)

ct.FontManager.load_font("./src/cooljazz.ttf")
my_font = ct.CTkFont("Cool jazz", size=24)

teacher_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "invite_l.png")), dark_image=Image.open(os.path.join('./src', "invite_d.png")), size=(20, 20))
schedule_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "schedule_l.png")), dark_image=Image.open(os.path.join('./src', "schedule_d.png")), size=(20, 20))
group_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "group_l.png")), dark_image=Image.open(os.path.join('./src', "group_d.png")), size=(20, 20))
subject_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "subject_l.png")), dark_image=Image.open(os.path.join('./src', "subject_d.png")), size=(20, 20))
coming_soon_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "coming_soon_l.png")), dark_image=Image.open(os.path.join('./src', "coming_soon_d.png")), size=(20, 20))

app.grid_rowconfigure(0,weight=1)
app.grid_columnconfigure(1,weight=1)

navigation_frame = ct.CTkFrame(app, corner_radius=0)
navigation_frame.grid(row=0, column=0, sticky="nsew")
navigation_frame.grid_rowconfigure(5, weight=1)

def one_btn_event():
    select_frame("one")

def two_btn_event():
    select_frame("two")

def three_btn_event():
    select_frame("three")

def four_btn_event():
    select_frame("four")


navigation_frame_label = ct.CTkLabel(navigation_frame, text="Mеню", image = ct.CTkImage(Image.open(os.path.join('./src', "icon.png")), size=(26, 26)), compound="left", font=my_font)
navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

add_human_btn = ct.CTkButton(navigation_frame, corner_radius=0, height=50, border_spacing=10, text="Добавить нового человека", fg_color="transparent", text_color=("gray10","gray90"), hover_color=("gray70","gray30"), anchor="w", image=teacher_icon, command=one_btn_event)
add_human_btn.grid(row=1, column=0 , sticky="ew")

add_new_schedule_btn = ct.CTkButton(navigation_frame, corner_radius=0, height=50, border_spacing=10, text="Добавить новое занятие", fg_color="transparent", text_color=("gray10","gray90"), hover_color=("gray70","gray30"), anchor="w", image=schedule_icon, command=two_btn_event)
add_new_schedule_btn.grid(row=2, column=0 , sticky="ew")

add_group_btn = ct.CTkButton(navigation_frame, corner_radius=0, height=50, border_spacing=10, text="Добавить новую группу", fg_color="transparent", text_color=("gray10","gray90"), hover_color=("gray70","gray30"), anchor="w", image=group_icon, command=three_btn_event)
add_group_btn.grid(row=3, column=0 , sticky="ew")

add_new_subject_btn = ct.CTkButton(navigation_frame, corner_radius=0, height=50, border_spacing=10, text="Добавить новый предмет", fg_color="transparent", text_color=("gray10","gray90"), hover_color=("gray70","gray30"), anchor="w", image=subject_icon, command=four_btn_event)
add_new_subject_btn.grid(row=4, column=0 , sticky="ew")

add_coming_soon_btn = ct.CTkButton(navigation_frame, corner_radius=0, height=50, border_spacing=10, text="Скоро будет", fg_color="transparent", text_color=("gray10","gray90"), hover_color=("gray70","gray30"), anchor="w", image=coming_soon_icon)
add_coming_soon_btn.grid(row=5, column=0 , sticky="ew")

human_frame = ct.CTkFrame(app, corner_radius=0, fg_color="transparent")
human_frame.grid_columnconfigure(0,weight=1)

human_name_label = ct.CTkLabel(human_frame, text="Добавить человека в систему", compound="center", font=my_font)
human_name_label.grid(row=0, column=0, padx=20, pady=20)


value_st = [('id', 'login', 'password', 'face', 'first_name', 'middle_name', 'last_name', 'email')]


tabview = ct.CTkTabview(human_frame)
tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
tabview.add("Студенты")
tabview.add("Учителя")

def display_students(tab):
    student_frame = ct.CTkScrollableFrame(tabview.tab("Студенты"))
    student_frame.pack(expand=False, fill="both")

    for col_index, header in enumerate(value_st[0]):
        label = ct.CTkLabel(student_frame, text=header, font=("Cool jazz", 12))
        label.grid(row=0, column=col_index, padx=5, pady=5, sticky="ew")

    for row_index, row in enumerate(value_st[1:], start=1):
        for col_index, item in enumerate(row):
            label = ct.CTkLabel(student_frame, text=str(item))
            label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")

    for col_index in range(len(value_st[0])):
        student_frame.grid_columnconfigure(col_index, weight=1)

database = db()
database = database.connect()
display_students(tabview)

def select_frame(name):
    add_human_btn.configure(fg_color=("gray75", "gray25") if name == "one" else "transparent")
    add_new_schedule_btn.configure(fg_color=("gray75", "gray25") if name == "two" else "transparent")
    add_group_btn.configure(fg_color=("gray75", "gray25") if name == "three" else "transparent")
    add_new_subject_btn.configure(fg_color=("gray75", "gray25") if name == "four" else "transparent")

    if name == "one":
        res=database.get_stud_list()
        human_frame.grid(row=0, column=1, sticky="nsew")
        value_st.extend(res)
    else:
        human_frame.grid_forget()
    # if name == "two":
        # second_frame.grid(row=0, column=1, sticky="nsew")
    # else:
        # second_frame.grid_forget()
    # if name == "three":
        # third_frame.grid(row=0, column=1, sticky="nsew")
    # else:
        # third_frame.grid_forget()


# frame_1 = customtkinter.CTkFrame(master=app)
# frame_1.pack(pady=20, padx=60, fill="both", expand=True)

# logo_label = customtkinter.CTkLabel(app, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
# label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT)
# label_1.pack(pady=10, padx=10)

# progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
# progressbar_1.pack(pady=10, padx=10)

# button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback)
# button_1.pack(pady=10, padx=10)

# slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=1)
# slider_1.pack(pady=10, padx=10)
# slider_1.set(0.5)

# entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry")
# entry_1.pack(pady=10, padx=10)

# optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."])
# optionmenu_1.pack(pady=10, padx=10)
# optionmenu_1.set("CTkOptionMenu")

# combobox_1 = customtkinter.CTkComboBox(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."])
# combobox_1.pack(pady=10, padx=10)
# combobox_1.set("CTkComboBox")

# checkbox_1 = customtkinter.CTkCheckBox(master=frame_1)
# checkbox_1.pack(pady=10, padx=10)

# radiobutton_var = customtkinter.IntVar(value=1)

# radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1)
# radiobutton_1.pack(pady=10, padx=10)

# radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2)
# radiobutton_2.pack(pady=10, padx=10)

# switch_1 = customtkinter.CTkSwitch(master=frame_1)
# switch_1.pack(pady=10, padx=10)

# text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=70)
# text_1.pack(pady=10, padx=10)
# text_1.insert("0.0", "CTkTextbox\n\n\n\n")

# segmented_button_1 = customtkinter.CTkSegmentedButton(master=frame_1, values=["CTkSegmentedButton", "Value 2"])
# segmented_button_1.pack(pady=10, padx=10)

# tabview_1 = customtkinter.CTkTabview(master=frame_1, width=300)
# tabview_1.pack(pady=10, padx=10)
# tabview_1.add("CTkTabview")
# tabview_1.add("Tab 2")

app.mainloop()