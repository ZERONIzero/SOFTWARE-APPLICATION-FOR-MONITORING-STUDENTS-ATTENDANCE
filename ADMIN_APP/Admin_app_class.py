import customtkinter as ct
import os
from PIL import Image
from PIL import ImageTk
from bd import db
import re

class ToplevelWindow(ct.CTkToplevel):
    def __init__(self, text_value,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x100")
        self.title("Ошибка")
        app.app.withdraw()
        self.label = ct.CTkLabel(self, text=text_value)
        self.label.pack(padx=20, pady=20)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        app.app.update()
        app.app.deiconify()
        self.destroy()

class ToplevelWindowImage(ct.CTkToplevel):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        self.title("Просмотр изображения")
        app.app.withdraw()

        image_path = app.url_photo.cget("text")
        self.image = Image.open(image_path)

        self.ctk_image = ct.CTkImage(light_image=self.image, dark_image=self.image, size=(500, 400))
        self.label = ct.CTkLabel(self, image=self.ctk_image, text="")
        self.label.pack(padx=5, pady=5)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        app.app.update()
        app.app.deiconify()
        self.destroy()

class AdminApp:
    def __init__(self):
        ct.set_appearance_mode("system")
        ct.set_default_color_theme("blue")
        
        self.app = ct.CTk()
        self.app.minsize(1280,720)
        self.app.geometry("+20+20")
        self.app.title("Инструмент для работы с БД")
        
        self.database = db().connect()
        if self.database is None:
            print("Ошибка подключения к базе данных")
            return
        
        self.value_st = [('id', 'login', 'password', 'face', 'first_name', 'middle_name', 'last_name', 'email')]
        self.value_th = [('id', 'login', 'face', 'password', 'first_name', 'middle_name', 'last_name', 'email')]
        
        self.check_email = self.app.register(self.is_email)

        self.setup_ui()
        
    def setup_ui(self):
        icopath = ImageTk.PhotoImage(file = ("./src/student.png"))
        self.app.iconphoto(False, icopath)

        ct.FontManager.load_font("./src/cooljazz.ttf")
        self.my_font = ct.CTkFont("Cool jazz", size=24)

        self.load_icons()
        
        self.app.grid_rowconfigure(0,weight=1)
        self.app.grid_columnconfigure(1,weight=1)
        
        self.create_navigation_frame()
        
        self.create_human_frame()
        # self.create_new_group()

    def load_icons(self):
        self.teacher_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "invite_l.png")), dark_image=Image.open(os.path.join('./src', "invite_d.png")), size=(20, 20))
        self.schedule_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "schedule_l.png")), dark_image=Image.open(os.path.join('./src', "schedule_d.png")), size=(20, 20))
        self.group_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "group_l.png")), dark_image=Image.open(os.path.join('./src', "group_d.png")), size=(20, 20))
        self.subject_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "subject_l.png")), dark_image=Image.open(os.path.join('./src', "subject_d.png")), size=(20, 20))
        self.coming_soon_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "coming_soon_l.png")), dark_image=Image.open(os.path.join('./src', "coming_soon_d.png")), size=(20, 20))
        self.add_icon = ct.CTkImage(light_image=Image.open(os.path.join('./src', "plus_l.png")), dark_image=Image.open(os.path.join('./src', "plus_d.png")), size=(10, 10))
        self.add_face = ct.CTkImage(light_image=Image.open(os.path.join('./src', "face_l.png")), dark_image=Image.open(os.path.join('./src', "face_d.png")), size=(14, 14))

    def create_navigation_frame(self):
        self.navigation_frame = ct.CTkFrame(self.app, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)
        
        navigation_frame_label = ct.CTkLabel(self.navigation_frame, 
                                             text="Mеню", 
                                             image=ct.CTkImage(Image.open(os.path.join('./src', "icon.png")), size=(26, 26)),
                                             compound="left", 
                                             font=self.my_font)
        navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.add_human_btn = ct.CTkButton(self.navigation_frame, 
                                         corner_radius=0, 
                                         height=50, 
                                         border_spacing=10, 
                                         text="Добавить нового человека",
                                         fg_color="transparent", 
                                         text_color=("gray10","gray90"),
                                         hover_color=("gray70","gray30"),
                                         anchor="w",
                                         image=self.teacher_icon,
                                         command=lambda: self.select_frame("one"))
        self.add_human_btn.grid(row=1, column=0, sticky="ew")

        self.add_new_schedule_btn = ct.CTkButton(self.navigation_frame,
                                                 corner_radius=0,
                                                 height=50, 
                                                 border_spacing=10, 
                                                 text="Добавить новое занятие", 
                                                 fg_color="transparent", 
                                                 text_color=("gray10","gray90"), 
                                                 hover_color=("gray70","gray30"), 
                                                 anchor="w", 
                                                 image=self.schedule_icon, 
                                                 command=lambda: self.select_frame("two"))
        self.add_new_schedule_btn.grid(row=2, column=0 , sticky="ew")

        self.add_group_btn = ct.CTkButton(self.navigation_frame, 
                                          corner_radius=0, 
                                          height=50, 
                                          border_spacing=10, 
                                          text="Добавить новую группу", 
                                          fg_color="transparent", 
                                          text_color=("gray10","gray90"), 
                                          hover_color=("gray70","gray30"), 
                                          anchor="w", 
                                          image=self.group_icon, 
                                          command=lambda: self.select_frame("three"))
        self.add_group_btn.grid(row=3, column=0 , sticky="ew")

        self.add_new_subject_btn = ct.CTkButton(self.navigation_frame, 
                                                corner_radius=0, 
                                                height=50, 
                                                border_spacing=10, 
                                                text="Добавить новый предмет", 
                                                fg_color="transparent", 
                                                text_color=("gray10","gray90"), 
                                                hover_color=("gray70","gray30"), 
                                                anchor="w", 
                                                image=self.subject_icon, 
                                                command=lambda: self.select_frame("four"))
        self.add_new_subject_btn.grid(row=4, column=0 , sticky="ew")

        self.add_coming_soon_btn = ct.CTkButton(self.navigation_frame, 
                                                corner_radius=0, 
                                                height=50, 
                                                border_spacing=10, 
                                                text="Скоро будет", 
                                                fg_color="transparent", 
                                                text_color=("gray10","gray90"), 
                                                hover_color=("gray70","gray30"), 
                                                anchor="w", 
                                                image=self.coming_soon_icon)
        self.add_coming_soon_btn.grid(row=5, column=0 , sticky="ew")


    def create_human_frame(self):
        self.human_frame = ct.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.human_frame.grid_columnconfigure(0, weight=1)
        
        self.human_name_label = ct.CTkLabel(self.human_frame, 
                                          text="Набор инструментов CRUD для человека",
                                          compound="center",
                                          font=self.my_font)
        self.human_name_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.create_tabview()
        self.create_form()
        self.create_biometric_form()
        self.create_delete_human_form()
        self.create_edit_email_form()

    def create_new_group(self):
        self.group_frame = ct.CTkFrame(self.app, corner_radius=0, fg_color="transparent")
        self.group_frame.grid_columnconfigure(0, weight=1)

        self.group_name_label = ct.CTkLabel(self.group_frame, 
                                          text="Набор инструментов CRUD для группы",
                                          compound="center",
                                          font=self.my_font)
        self.group_name_label.grid(row=0, column=0, padx=20, pady=10)

    def is_id(self,newval):
        if not newval:
            ToplevelWindow("Поле пустое").focus()
            return False
        if newval.isdigit():
            return True
        else:
            ToplevelWindow("Некорректный индентификатор").focus()
            self.entry_id.delete(0,'end')
            return False

    def is_valid(self, newval, entry):
        if not newval:
            ToplevelWindow("Поле пустое").focus()
            return False
        if not re.match("^[А-Яа-яЁёA-Za-z]+$", newval):
            ToplevelWindow("В поле недопустимые символы").focus()
            getattr(self, entry).delete(0, 'end')
            return False
        return True

    def is_email(self, newval):
        if not newval:
            ToplevelWindow("Поле пустое").focus()
            return False
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, newval):
            return True
        else:
            ToplevelWindow("Некорректный email").focus()
            self.entry_email.delete(0,'end')
            return False

    def select_photo(self):
        filename = ct.filedialog.askopenfilename(title="Выберите фотографию человека", filetypes=[('Portable Network Graphics','.png'),('Joint Photographic Experts Group','.jpeg'),('Joint Photographic Experts Group','.jpg'),('JPEG File Interchange Format','.jfif')])
        print(str(filename))
        if filename:
            self.url_photo.configure(text=str(filename))
            self.open_image.configure(state="enabled")
        else:
            self.url_photo.configure(text="Изображение не выбрано")
            self.open_image.configure(state="disabled")

    def add_biometric(self):
        try:
            i_d = self.entry_id.get()
            if not i_d:
                ToplevelWindow("Поле индентификатор пустое").focus()
                return False
            st = self.option_select.get()
            url = self.url_photo.cget("text")
            if url == "Изображение не выбрано":
                ToplevelWindow("Изображение не выбрано").focus()
                return False
            else:
                send_face = self.database.send_biometric(i_d,st,url)
                if send_face:
                    self.url_photo.configure(text="Изображение не выбрано")
                    self.entry_id.delete(0, 'end')
                    if st == "Учитель":
                        self.display_teacher()
                    else:
                        self.display_students()
                    return True
                else:
                    ToplevelWindow("Такой пользователь не существует в бд")
                    return False
        except Exception as e:
            ToplevelWindow("Ошибка при добавлении биометрии")
            return False

    def get_human_data(self):
        try:
            f_n = self.entry_first_name.get()
            if not f_n:
                ToplevelWindow("Поле имя пустое").focus()
                return False
            
            m_n = self.entry_middle_name.get()

            l_n = self.entry_last_name.get()
            if not l_n:
                ToplevelWindow("Поле фамилия пустое").focus()
                return False
            
            l_p = self.entry_login.get()
            if not l_p:
                ToplevelWindow("Поле login пустое").focus()
                return False
            
            e_p = self.entry_email.get()
            if not e_p:
                ToplevelWindow("Поле email пустое").focus()
                return False

            status = self.option_select_type.get()
            res_send = self.database.new_person(f_n,m_n,l_n,l_p,e_p,status)
            if res_send:
                self.entry_first_name.delete(0, 'end')
                self.entry_middle_name.delete(0, 'end')
                self.entry_last_name.delete(0, 'end')
                self.entry_login.delete(0, 'end')
                self.entry_email.delete(0, 'end')
                if status == "Учитель":
                    self.display_teacher()
                else:
                    self.display_students()
            else:
                ToplevelWindow("Такой пользователь существует в бд")

        except Exception as e:
            ToplevelWindow("Ошибка при создании пользователя")

    def delete_person(self):
        try:
            id_for_delete = self.delete_entry_id.get()
            if not id_for_delete:
                ToplevelWindow("Id имя пустое").focus()
                return False

            id_select_status = self.delete_option_select.get()
            del_human = self.database.del_person(id_for_delete,id_select_status)
            # if del_human:
            #     # self.entry_first_name.delete(0, 'end')
            #     # self.entry_middle_name.delete(0, 'end')
            #     # self.entry_last_name.delete(0, 'end')
            #     # self.entry_login.delete(0, 'end')
            #     # self.entry_email.delete(0, 'end')
            #     if id_select_status == "Учитель":
            #         self.display_teacher()
            #     else:
            #         self.display_students()
            # else:
            #     ToplevelWindow("Такой пользователь не существует в бд")


        except Exception as e:
            ToplevelWindow("Ошибка при удалении пользователя")

    def create_biometric_form(self):
        self.add_face_data = ct.CTkFrame(self.human_frame)
        self.add_face_data.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.add_face_data.grid_columnconfigure(0, weight=1)
        self.add_face_data.grid_rowconfigure(0,weight=1)

        self.add_face_frame = ct.CTkFrame(self.add_face_data, fg_color="transparent", bg_color="transparent")
        self.add_face_frame.grid(row=0, column=0, padx=20, pady=2, sticky="nsew")

        self.add_face_label = ct.CTkLabel(self.add_face_frame,
                                          text="Добавить биометрические данные человека",
                                          compound="center",
                                          font=  ct.CTkFont("Cool jazz", size=20))
        self.add_face_label.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")

        self.add_face_frame_for_entry = ct.CTkFrame(self.add_face_data, fg_color="transparent", bg_color="transparent")
        self.add_face_frame_for_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.entry_id = ct.CTkEntry(self.add_face_frame_for_entry,placeholder_text="id", validate="focusout", validatecommand=(self.app.register(self.is_id), "%P"))
        self.entry_id.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
        
        self.option_select = ct.CTkOptionMenu(self.add_face_frame_for_entry, values=["Студент","Учитель"], dynamic_resizing=False)
        self.option_select.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        self.filedialog_button = ct.CTkButton(self.add_face_frame_for_entry,text="Выбрать фото", command= lambda: self.select_photo())
        self.filedialog_button.grid(row=0, column=2, padx=5, pady=2, sticky="ew")

        self.url_photo = ct.CTkLabel(self.add_face_frame_for_entry, text="Изображение не выбрано")
        self.url_photo.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        self.open_image = ct.CTkButton(self.add_face_frame_for_entry,text="Посмотреть изображение", command= lambda: ToplevelWindowImage())
        self.open_image.configure(state="disabled")
        self.open_image.grid(row=0, column=4, padx=5, pady=2, sticky="ew")

        self.add_face_btn = ct.CTkButton(self.add_face_frame_for_entry, 
                                         corner_radius=10, 
                                         height=25, 
                                         border_spacing=5, 
                                         text="Добавить биометрию",
                                         fg_color="transparent", 
                                         text_color=("gray10","gray90"),
                                         hover_color=("gray70","gray30"),
                                         anchor="w",
                                         image=self.add_face,
                                         command=lambda: self.add_biometric())
        self.add_face_btn.grid(row=0, column=5, padx=5, pady=2, sticky="ew")

        self.add_face_frame_for_entry.grid_columnconfigure(0, weight=1)
        self.add_face_frame_for_entry.grid_columnconfigure(1, weight=1)
        self.add_face_frame_for_entry.grid_columnconfigure(2, weight=1)
        self.add_face_frame_for_entry.grid_columnconfigure(3, weight=1)
        self.add_face_frame_for_entry.grid_columnconfigure(4, weight=1)
        self.add_face_frame_for_entry.grid_columnconfigure(5, weight=1)

    def create_form(self):
        self.add_label = ct.CTkFrame(self.human_frame)
        self.add_label.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.entry_first_name = ct.CTkEntry(self.add_label, placeholder_text="Имя", validate="focusout", validatecommand=(self.app.register(self.is_valid), "%P", "entry_first_name"))
        self.entry_first_name.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        self.entry_middle_name = ct.CTkEntry(self.add_label, placeholder_text="Отчество")
        self.entry_middle_name.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.entry_last_name = ct.CTkEntry(self.add_label, placeholder_text="Фамилия", validate="focusout", validatecommand=(self.app.register(self.is_valid), "%P", "entry_last_name"))
        self.entry_last_name.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

        self.entry_login = ct.CTkEntry(self.add_label, placeholder_text="Логин пользователя", validate="focusout", validatecommand=(self.app.register(self.is_valid), "%P", "entry_login"))
        self.entry_login.grid(row=1, column=3, padx=5, pady=10, sticky="ew")
    
        self.entry_email = ct.CTkEntry(self.add_label, placeholder_text="Email", validate="focusout", validatecommand=(self.check_email, "%P"))
        self.entry_email.grid(row=1, column=4, padx=5, pady=10, sticky="ew")

        self.option_select_type = ct.CTkOptionMenu(self.add_label, values=["Студент","Учитель"], dynamic_resizing=False)
        self.option_select_type.grid(row=1, column=5, padx=5, pady=10, sticky="ew")

        self.add_post_btn = ct.CTkButton(self.add_label, 
                                         corner_radius=10, 
                                         height=25, 
                                         border_spacing=5, 
                                         text="Добавить",
                                         fg_color="transparent", 
                                         text_color=("gray10","gray90"),
                                         hover_color=("gray70","gray30"),
                                         anchor="w",
                                         image=self.add_icon,
                                         command= lambda: self.get_human_data())
        self.add_post_btn.grid(row=1, column=6, padx=5, pady=10, sticky="ew")

        for col_index in range(7):
            self.add_label.grid_columnconfigure(col_index,weight=1)

    def create_tabview(self):
        self.tabview = ct.CTkTabview(self.human_frame)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Студенты")
        self.tabview.add("Учителя")
        
        self.student_frame = ct.CTkScrollableFrame(self.tabview.tab("Студенты"))
        self.student_frame.pack(expand=False, fill="both")

        self.teacher_frame = ct.CTkScrollableFrame(self.tabview.tab("Учителя"))
        self.teacher_frame.pack(expand=False, fill="both")
        
        for col_index, header in enumerate(self.value_st[0]):
            label = ct.CTkLabel(self.student_frame, text=header, font=("Cool jazz", 12))
            label.grid(row=0, column=col_index, padx=5, pady=5, sticky="ew")
            
        for col_index in range(len(self.value_st[0])):
            self.student_frame.grid_columnconfigure(col_index, weight=1)

        for col_index, header in enumerate(self.value_th[0]):
            label = ct.CTkLabel(self.teacher_frame, text=header, font=("Cool jazz", 12))
            label.grid(row=0, column=col_index, padx=5, pady=5, sticky="ew")
            
        for col_index in range(len(self.value_th[0])):
            self.teacher_frame.grid_columnconfigure(col_index, weight=1)
            
        self.on_tab_change()

    def create_delete_human_form(self):
        self.double_label_frame = ct.CTkFrame(self.human_frame, fg_color="transparent", bg_color="transparent")
        self.double_label_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.double_label_frame.grid_columnconfigure(0, weight=1)
        self.double_label_frame.grid_columnconfigure(1, weight=1)
        self.double_label_frame.grid_rowconfigure(0,weight=1)

        self.delete_human_frame = ct.CTkFrame(self.double_label_frame)
        self.delete_human_frame.grid(row=0, column=0, padx=10, pady=2, sticky="nsew")
        self.delete_human_frame.grid_columnconfigure(0, weight=1)
        self.delete_human_frame.grid_rowconfigure(0,weight=1)
        self.delete_human_frame.grid_rowconfigure(1,weight=1)

        self.add_delete_label = ct.CTkLabel(self.delete_human_frame,
                                          text="Удалить данные человека из БД",
                                          compound="center",
                                          font=  ct.CTkFont("Cool jazz", size=20))
        self.add_delete_label.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")

        self.delete_frame_for_entry = ct.CTkFrame(self.delete_human_frame, fg_color="transparent", bg_color="transparent")
        self.delete_frame_for_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.delete_entry_id = ct.CTkEntry(self.delete_frame_for_entry, placeholder_text="id", validate="focusout", validatecommand=(self.app.register(self.is_id), "%P"))
        self.delete_entry_id.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
        
        self.delete_option_select = ct.CTkOptionMenu(self.delete_frame_for_entry, values=["Студент","Учитель"], dynamic_resizing=False)
        self.delete_option_select.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        self.delete_human_button = ct.CTkButton(self.delete_frame_for_entry,text="Удалить запись", command = lambda: self.delete_person())
        self.delete_human_button.grid(row=0, column=2, padx=5, pady=2, sticky="ew")

        self.delete_frame_for_entry.grid_columnconfigure(0, weight=1)
        self.delete_frame_for_entry.grid_columnconfigure(1, weight=1)
        self.delete_frame_for_entry.grid_columnconfigure(2, weight=1)


    def create_edit_email_form(self):
        self.update_human_frame = ct.CTkFrame(self.double_label_frame)
        self.update_human_frame.grid(row=0, column=1, padx=10, pady=2, sticky="nsew")
        self.update_human_frame.grid_columnconfigure(0, weight=1)
        self.update_human_frame.grid_rowconfigure(0,weight=1)

        self.add_update_label = ct.CTkLabel(self.update_human_frame,
                                          text="Изменить email человека из БД",
                                          compound="center",
                                          font=  ct.CTkFont("Cool jazz", size=20))
        self.add_update_label.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")

        self.update_frame_for_entry = ct.CTkFrame(self.update_human_frame, fg_color="transparent", bg_color="transparent")
        self.update_frame_for_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.update_entry_id = ct.CTkEntry(self.update_frame_for_entry, placeholder_text="id", validate="focusout", validatecommand=(self.app.register(self.is_id), "%P"))
        self.update_entry_id.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
        
        self.update_option_select = ct.CTkOptionMenu(self.update_frame_for_entry, values=["Студент","Учитель"], dynamic_resizing=False)
        self.update_option_select.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        self.update_entry_value = ct.CTkEntry(self.update_frame_for_entry, placeholder_text="update_email", validate="focusout", validatecommand=(self.app.register(self.is_email), "%P"))
        self.update_entry_value.grid(row=0, column=2, padx=5, pady=2, sticky="ew")

        self.update_human_button = ct.CTkButton(self.update_frame_for_entry,text="Изменить запись")
        self.update_human_button.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        self.update_frame_for_entry.grid_columnconfigure(0, weight=1)
        self.update_frame_for_entry.grid_columnconfigure(1, weight=1)
        self.update_frame_for_entry.grid_columnconfigure(2, weight=1)
        self.update_frame_for_entry.grid_columnconfigure(3, weight=1)

    def on_tab_change(self):
        current_tab = self.tabview.get()
        if current_tab == "Студенты":
            self.display_students()
        if current_tab == "Учителя":    
            self.display_teacher()

    def display_teacher(self):
        for widget in self.teacher_frame.winfo_children():
            if int(widget.grid_info()['row']) > 0:
                widget.destroy()

        try:
            teacher_data = self.database.get_teacher_list()
            if teacher_data:
                for row_index, row in enumerate(teacher_data, start=1):
                    for col_index, item in enumerate(row):
                        label = ct.CTkLabel(self.teacher_frame, text=str(item), font=('Cool jazz',12))
                        label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")
        except Exception as e:
            print(f"Ошибка при получении данных студентов: {e}")
            error_label = ct.CTkLabel(self.teacher_frame, text="Ошибка загрузки данных")
            error_label.grid(row=1, column=0, columnspan=len(self.value_th[0]), padx=5, pady=5)

    def display_students(self):
        for widget in self.student_frame.winfo_children():
            if int(widget.grid_info()['row']) > 0:
                widget.destroy()

        try:
            students_data = self.database.get_stud_list()
            if students_data:
                for row_index, row in enumerate(students_data, start=1):
                    for col_index, item in enumerate(row):
                        label = ct.CTkLabel(self.student_frame, text=str(item), font=('Cool jazz',12))
                        label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")
        except Exception as e:
            print(f"Ошибка при получении данных студентов: {e}")
            error_label = ct.CTkLabel(self.student_frame, text="Ошибка загрузки данных")
            error_label.grid(row=1, column=0, columnspan=len(self.value_st[0]), padx=5, pady=5)

    def select_frame(self, name):
        self.add_human_btn.configure(fg_color=("gray75", "gray25") if name == "one" else "transparent")
        self.add_new_schedule_btn.configure(fg_color=("gray75", "gray25") if name == "two" else "transparent")
        self.add_group_btn.configure(fg_color=("gray75", "gray25") if name == "three" else "transparent")
        self.add_new_subject_btn.configure(fg_color=("gray75", "gray25") if name == "four" else "transparent")

        if name == "one":
            # self.group_frame.grid_forget()

            self.human_frame.grid(row=0, column=1, sticky="nsew")
            try:
                students_data = self.database.get_stud_list()
                if students_data:
                    self.value_st = [self.value_st[0]] + list(students_data)
                    self.display_students()

                teacher_data = self.database.get_teacher_list()
                if teacher_data:
                    self.value_th = [self.value_th[0]] + list(teacher_data)
                    self.display_teacher()

            except Exception as e:
                print(f"Ошибка при обновлении данных: {e}")

        # elif name == "three":
        #     self.human_frame.grid_forget()

        #     self.group_frame.grid(row=0, column=1, sticky="nsew")
        #     try:

        #     except Exception as e:
        #         print(f"Ошибка при обновлении данных: {e}")
        else:
            self.human_frame.grid_forget()
            # self.group_frame.grid_forget()

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = AdminApp()
    app.run()