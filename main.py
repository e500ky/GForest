import json, requests
from io import BytesIO
import shutil
import PIL
import gc
import PIL.Image
import PIL.ImageDraw
import PIL.ImageTk
from customtkinter import *
from tkinter import *
from tkinter.filedialog import *
from json import *
from tkinter.font import BOLD
from tkinter.messagebox import *
from tkinter import colorchooser

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("GForest")
        self.setGeo()
        self.iconbitmap("./src/libs/icon.ico")
        self.setThemeDefault()
        self.setGUI()
        self.bind("<F5>", lambda event:self.listApps())

        with open("./src/data/selection.json", "r", encoding="utf-8") as file:
            a = file.read()
            file.close()

        a = a.replace("%USERNAME%", os.environ["USERNAME"])
        
        with open("./src/data/selection.json", "w", encoding="utf-8") as file:
            file.write(a)
            file.close()
    
    def setGeo(self):
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()

        self.appWidth = int(self.winfo_screenwidth() / 5 * 3.5)
        self.appHeight = int(self.winfo_screenheight() / 5 * 3.5)

        self.appX = int((self.screenwidth - self.appWidth) / 2)
        self.appY = int((self.screenheight - self.appHeight) / 2)

        self.geometry(f"{self.appWidth}x{self.appHeight}+{self.appX}+{self.appY}")
        self.minsize(self.appWidth/4*3, self.appHeight/4*3)

        self.resizable(False, False)

    def setGUI(self):
        self.header()
        self.body()

    def checkSearch(self):
        if self.search_entry.get() != self.beforeSearch:
            if self.beforeSearch == None:
                self.beforeSearch = ""
            else: 
                self.listApps(self.search_entry.get())
                self.beforeSearch = self.search_entry.get()

    def start_timer(self, master=False):
        """3 saniyelik bir zamanlayıcı başlatır."""
        # Eğer bir önceki zamanlayıcı varsa iptal et
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)

        # Yeni zamanlayıcı başlat
        if master: self.timer_id = self.after(self.timeout_duration, lambda: self.remove_focus(master))
        else: self.timer_id = self.after(self.timeout_duration, self.remove_focus)

    def reset_timer(self, event=None, master=False):
        """Bir tuşa basıldığında zamanlayıcıyı sıfırlar."""
        if master: self.start_timer(master)
        else: self.start_timer()

    def remove_focus(self, master=False):
        """Entry'den odaklanmayı kaldırır."""
        self.focus()  # Entry dışına odaklanmayı ayarlar
        if master: master.configure(state="disabled")

    def header(self):
        self.beforeSearch = None

        self.header_frame = CTkFrame(self, corner_radius=0, height=75)
        self.header_frame.pack(fill=X, padx=0, pady=0, side=TOP)

        self.iconFrame = CTkFrame(self, corner_radius=10, height=50, width=50, border_width=0)
        self.iconFrame.place(x=12.5, y=12.5)

        self.create_frame_with_image(
            width=50,
            height=50,
            corner_radius=10,
            image_path="./src/libs/icon.png",
            master=self.iconFrame,
            bg_color="#292929"
        )

        self.logo_label = CTkLabel(self.header_frame, text="GForest", font=("Arial", 25, "bold"))
        self.logo_label.place(x=75, y=20)

        self.search_entry = CTkEntry(self.header_frame, font=("Sans-Serif", 20), width=500, height=45, corner_radius=10, border_width=1, text_color="#888", justify="center", placeholder_text="Search",
                                     placeholder_text_color="#666")
        self.search_entry.pack(pady=(15, 15))
        self.search_entry.bind("<KeyRelease>", lambda event: self.checkSearch())
        self.search_entry.bind("<Key>", self.reset_timer)
        self.search_entry.bind("<Button>", self.reset_timer)

        with open("./src/data/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            self.timeout_duration = config["timeout.duration"] * 1000  # Milisaniye cinsinden
            f.close()

        self.timer_id = None

        self.addAppBtn = CTkButton(self.header_frame, text="➕", font=("Segoe UI Emoji",20), border_width=1, width=45, height=45, corner_radius=7.5, fg_color=self.fg_color, text_color="white", border_color=self.hover_color, hover_color=self.hover_color, command=lambda: self.addApp())
        self.addAppBtn.place(x=self.appWidth-120, y=15)

        self.settingsBtn = CTkButton(self.header_frame, text="▢", font=("Segoe UI Emoji",20), border_width=1, width=45, height=45, corner_radius=7.5, fg_color=self.fg_color, text_color="white", border_color=self.hover_color, hover_color=self.hover_color, command=lambda: self.settings())
        self.settingsBtn.place(x=self.appWidth-60, y=15)

    def settings(self):
        try:
            self.addAppFrame.pack_forget()
            self.addAppFrame.destroy()
            self.addAppBtn.configure(text="➕", command=lambda: self.addApp())
        except: pass
        # Settings butonu tıklandığında buraya gelecek
        self.settingsFrame = CTkFrame(self, width=self.appWidth - 40, height=self.appHeight - 115, corner_radius=10, border_width=1, fg_color="#303030")
        self.settingsFrame.place(x=20, y=95)

        self.head = CTkLabel(self.settingsFrame, font=("Sans-Serif", 60, BOLD), text="Settings", text_color="#999", fg_color="#303030", bg_color="#303030")
        self.head.place(x=50, y=30)

        self.themeSetArea = CTkFrame(self.settingsFrame, bg_color="#303030", fg_color="#404040", border_width=1, corner_radius=10, width=self.appWidth - 140, height=250)
        self.themeSetArea.place(x=50, y=150)

        with open("./src/data/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            f.close()

        self.primercolor = config["theme"]["button"]["color.fg"]
        self.secondercolor = config["theme"]["button"]["color.hover"]

        self.colorlabel = CTkLabel(self.themeSetArea, text="Colors", fg_color="#404040", bg_color="#404040", corner_radius=0, font=("Sans-Serif", 45, BOLD))
        self.colorlabel.place(x=40, y=25)

        self.maincolorlabel = CTkLabel(self.themeSetArea, text="Main Color", fg_color="#404040", bg_color="#404040", corner_radius=0, font=("Sans-Serif", 25, BOLD), text_color="#888")
        self.maincolorlabel.place(x=25+15, y=100)

        self.maincolorview = CTkFrame(self.themeSetArea, fg_color=self.primercolor, bg_color="#404040", corner_radius=10, border_width=0, border_color=self.secondercolor, height=50, width=50)
        self.maincolorview.place(x=25+15, y=150)
        self.maincolorview.bind("<Button-1>", lambda event: (self.select_color1()))

        self.maincolorhex = CTkLabel(self.themeSetArea, fg_color="#404040", bg_color="#404040", text=f"{self.primercolor}", text_color=self.primercolor, font=("Sans-Serif", 25, BOLD))
        self.maincolorhex.place(x=90+15, y=157.5)

        self.secondcolorlabel = CTkLabel(self.themeSetArea, text="Second Color", fg_color="#404040", bg_color="#404040", corner_radius=0, font=("Sans-Serif", 25, BOLD), text_color="#888")
        self.secondcolorlabel.place(x=325+15, y=100)

        self.secondcolorview = CTkFrame(self.themeSetArea, fg_color=self.secondercolor, bg_color="#404040", corner_radius=10, border_width=0, border_color=self.secondercolor, height=50, width=50)
        self.secondcolorview.place(x=325+15, y=150)
        self.secondcolorview.bind("<Button-1>", lambda event: (self.select_color2()))

        self.secondcolorhex = CTkLabel(self.themeSetArea, fg_color="#404040", bg_color="#404040", text=f"{self.secondercolor}", text_color=self.secondercolor, font=("Sans-Serif", 25, BOLD))
        self.secondcolorhex.place(x=390+15, y=157.5)

        self.bind("<Escape>", lambda event:(
            self.settingsFrame.pack_forget(),
            self.settingsFrame.destroy(),
            self.settingsBtn.configure(text="▢", command=lambda: self.settings()),
            self.listApps(),
            self.focus()
        ))

        self.save__btn = CTkButton(self.settingsFrame, fg_color=self.fg_color, command=self.save_settings, bg_color="#404040", border_color=self.hover_color, hover_color=self.hover_color, text="Save", font=("Sans-Serif", 18), corner_radius=7.5, width=160, height=45)
        self.save__btn.place(x=self.appWidth - 175-40, y=self.appHeight - 115-60)

        self.setDefault__btn = CTkButton(self.settingsFrame, fg_color=self.fg_color, command=self.set_default_settings, bg_color="#404040", border_color=self.hover_color, hover_color=self.hover_color, text="Default", font=("Sans-Serif", 18), corner_radius=7.5, width=160, height=45)
        self.setDefault__btn.place(x=self.appWidth - 175-40-175, y=self.appHeight - 115-60)

        self.settingsBtn.configure(text="✖️", command=lambda: (self.settingsFrame.pack_forget(), self.settingsFrame.destroy(), self.listApps(), self.settingsBtn.configure(text="▢", command=lambda: self.settings()), self.focus()))

    def save_settings(self):
        # Kaydedilecek ayarları kaydet
        with open("./src/data/config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()

        data["theme"]["button"]["color.fg"] = self.primercolor
        data["theme"]["button"]["color.hover"] = self.secondercolor

        with open("./src/data/config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()

        showinfo("Settings","The changes will take effect when you restart the application.")

    def set_default_settings(self):
        #Varsayılan ayarları yükle
        with open("./src/data/default.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()

        with open("./src/data/config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()

        showinfo("Settings","The changes will take effect when you restart the application.")

    def select_color1(self):
        # Renk seçme penceresini aç
        color_code = colorchooser.askcolor(title="Select a color")[1]  # HEX kodu döner
        if color_code:
            self.maincolorhex.configure(text=f"{color_code}", text_color=color_code)
            self.maincolorview.configure(fg_color=color_code)
            self.primercolor = color_code

    def select_color2(self):
        # Renk seçme penceresini aç
        color_code = colorchooser.askcolor(title="Select a color")[1]  # HEX kodu döner
        if color_code:
            self.secondcolorhex.configure(text=f"{color_code}", text_color=color_code)
            self.secondcolorview.configure(fg_color=color_code)
            self.secondercolor = color_code

    def addApp(self):
        try:
            self.settingsFrame.pack_forget()
            self.settingsFrame.destroy()
            self.settingsBtn.configure(text="▢", command=lambda: self.settings())
        except: pass
        self.addAppFrame = CTkFrame(self, width=self.appWidth - 40, height=self.appHeight - 115, corner_radius=10, border_width=1, fg_color="#303030")
        self.addAppFrame.place(x=20, y=95)

        self.appLogo_ = CTkFrame(self.addAppFrame, corner_radius=15, width=300, height=300, border_width=1,
                                    fg_color="#404040", bg_color="#303030", border_color="#505050")
        self.appLogo_.place(x=50 ,y=50)

        self.appLogoLabel_ = CTkLabel(self.appLogo_, wraplength=250, text="Select\nImage", font=("Consolas", 45), text_color="#777", bg_color="#404040", fg_color="#404040", corner_radius=15)
        self.appLogoLabel_.place()
        self.appLogoLabel_.update_idletasks()
        self.appLogoLabel_.place(x=(300 - self.appLogoLabel_.winfo_reqwidth())/2, y=(300 - self.appLogoLabel_.winfo_reqheight())/2)

        self.appLogo_.bind("<Enter>", lambda event: (self.appLogo_.configure(fg_color="#454545"), self.appLogoLabel_.configure(bg_color="#454545", fg_color="#454545")))
        self.appLogo_.bind("<Leave>", lambda event: (self.appLogo_.configure(fg_color="#404040"), self.appLogoLabel_.configure(bg_color="#404040", fg_color="#404040")))

        self.appLogoLabel_.bind("<Enter>", lambda event: (self.appLogo_.configure(fg_color="#454545"), self.appLogoLabel_.configure(bg_color="#454545", fg_color="#454545")))
        self.appLogoLabel_.bind("<Leave>", lambda event: (self.appLogo_.configure(fg_color="#404040"), self.appLogoLabel_.configure(bg_color="#404040", fg_color="#404040")))

        self.appLogo_.bind("<Button-1>", lambda event: self.selectimage())
        self.appLogoLabel_.bind("<Button-1>", lambda event: self.selectimage())

        self.appName__ = CTkEntry(self.addAppFrame, text_color="white", placeholder_text="App Name...", placeholder_text_color="#888", font=("Sans-Serif", 100,"bold"),corner_radius=0, fg_color="#303030", bg_color="#303030", border_width=0, width=self.appWidth - 450)
        self.appName__.place(x=400, y=75)

        self.bind("<Key>", self.reset_timer)
        self.bind("<Button>", self.reset_timer)

        self.type_ = CTkLabel(self.addAppFrame, text="Save Type: ", font=("Sans-Serif", 25 , BOLD), text_color="#777", bg_color="#303030", fg_color="#303030", corner_radius=7.5)
        self.type_.place(x=400, y=400)

        self.appTypeComboBox = CTkComboBox(self.addAppFrame,
                                           values=["Application", "Folder", "Game", "Shortcut", "URL"],
                                           font=("Sans-Serif", 16),
                                           fg_color="#404040",
                                           button_color="#505050",
                                           dropdown_fg_color="#404040",
                                           dropdown_text_color="white",
                                           width=500,
                                           height=45)
        self.appTypeComboBox.place(x=400, y=440)
        self.appTypeComboBox.set("Application")

        self.selectedimg = None

        self.appName_ = CTkLabel(self.addAppFrame, text="Directory / URL: ", font=("Sans-Serif", 25 , BOLD), text_color="#777", bg_color="#303030", fg_color="#303030")
        self.appName_.place(x=407.5, y=275)

        self.checkLink = None

        self.appName__.bind("<Return>", lambda event: self.setLinkImg())

        self.dir_ = CTkEntry(self.addAppFrame, text_color="white", placeholder_text="App Directory or URL...", placeholder_text_color="#888", font=("Sans-Serif", 25,"bold"), corner_radius=7.5, height=45, fg_color="#454545", bg_color="#303030", border_width=1, width=500)
        self.dir_.place(x=400, y=315)


        self.dir_.bind("<Return>", lambda event: self.setLinkImg())

        self.select_on_filedialog = CTkButton(self.addAppFrame, text="📂", width=45, height=45, font=("Segoe UI Emoji", 20), fg_color=self.fg_color, text_color="white", border_color=self.hover_color, hover_color=self.hover_color, border_width=1, command=self.selectfolder)
        self.select_on_filedialog.place(x=915, y=315)

        self.select_on_filedialog = CTkButton(self.addAppFrame, text="🔎", width=45, height=45, font=("Segoe UI Emoji", 20), fg_color=self.fg_color, text_color="white", border_color=self.hover_color, hover_color=self.hover_color, border_width=1, command=self.selectfile)
        self.select_on_filedialog.place(x=975, y=315)

        self.save_btn = CTkButton(self.addAppFrame,  text="Save", width=150, height=45, command=lambda: (self.saveApp()), border_width=1, border_color=self.hover_color, fg_color=self.fg_color, text_color="white", hover_color=self.hover_color, bg_color="#303030", font=("Sans-Serif", 20, BOLD))
        self.save_btn.place(x=(self.appWidth - 40 - 165), y=(self.appHeight - 115 - 60))

        self.bind("<Escape>", lambda event:(
            self.addAppFrame.pack_forget(),
            self.addAppFrame.destroy(),
            self.addAppBtn.configure(text="➕", command=lambda: self.addApp()),
            self.listApps(),
            self.focus()
        ))

        self.addAppBtn.configure(text="✖️", command=lambda: (self.addAppFrame.pack_forget(), self.addAppFrame.destroy(), self.listApps(), self.addAppFrame.configure(text="➕", command=lambda: self.addApp()), self.focus()))

    def selectApp(self, key, value, icon):
        self.appTypeComboBox.set(value["type"])
        self.appName__.delete(0, END)
        self.appName__.insert(0, value["name"].title())
        if value["dir"] != "none":
            self.dir_.delete(0, END)
            self.dir_.insert(0, value["dir"])
        self.checkLink = value["name"].lower()
        self.selectedimg = icon
        self.setimg(icon)
        if self.namesearch == "": self.appName__.focus()
        else: self.focus()

    def setLinkImg(self):
        self.appDirectory = self.dir_.get()
        with open("./src/data/selection.json", "r", encoding="utf-8") as src:
            selection = json.load(src)
            src.close()

        self.namesearch = self.appName__.get().replace("İ", "I")

        if os.path.isfile(self.appDirectory) and self.appDirectory != "" and self.appDirectory != None:
            self.create_frame_with_image(300, 300, 15, "folder/folder.png", self.appLogo_)

        else:
            for key, value in selection.items():
                if self.namesearch.lower() == value["name"] and self.checkLink != value["name"]:
                    if os.path.isfile(value["dir"]) or os.path.isdir(value["dir"]) or value["dir"].startswith("http") or self.namesearch == value["name"]:
                        if os.path.isdir(value["dir"]): self.selectApp(key, value, "folder/folder.png")
                        else: self.selectApp(key, value, value["icon"])

                else:
                    for i in value["keywords"]:
                        if self.appDirectory == i and self.checkLink != value["name"]:
                            if os.path.isfile(value["dir"]) or os.path.isdir(value["dir"]) or value["dir"].startswith("http"):
                                self.selectApp(key, value)
                                

    def saveApp(self):
        self.appDirectory = self.dir_.get()
        self.applicationName = self.appName__.get()
        self.appType = self.appTypeComboBox.get()
        self.fileDirectory = self.appDirectory

        try:
            if self.applicationName != "" and self.fileDirectory != "":
                with open("./src/data/apps.json", "r", encoding="utf-8") as f:
                    apps = json.load(f)
                    f.close()

                self.appIcon = "none"
                if self.selectedimg != None: self.appIcon = f"{self.applicationName}.png"
                if os.path.isdir(self.appDirectory):
                    self.appIcon = "folder/folder.png"
                    self.appType = "Folder"
                # new_app'in doğru formatta olması gerektiği yer
                new_app = {
                    "name": f"{self.applicationName}",
                    "icon": self.appIcon,
                    "type": f"{self.appType}",
                    "appDirectory": f"{self.fileDirectory}",
                }
                # Yeni uygulamayı ekle
                apps["apps"][self.applicationName] = new_app

                # Güncellenmiş JSON'u dosyaya yaz
                with open("./src/data/apps.json", "w", encoding="utf-8") as f:
                    json.dump(apps, f, indent=4, ensure_ascii=False)  # ensure_ascii=False Türkçe karakterleri korur
                    if self.selectedimg != None:
                        try:
                            os.rename("./src/libs/apps/current.png", f"./src/libs/apps/{self.applicationName}.png")
                        except FileExistsError:
                            os.remove(f"./src/libs/apps/{self.applicationName}.png")
                            os.rename("./src/libs/apps/current.png", f"./src/libs/apps/{self.applicationName}.png")
                    self.addAppFrame.pack_forget()
                    self.addAppFrame.destroy()
                    self.listApps()
                    f.close()

            else:
                showwarning("Incomplete Information", "Choosing one image is not mandatory,\nbut everything else is.\n\nPlease make sure you do not leave any missing information.")
        except AttributeError:
            showwarning("Incomplete Information", "Choosing one image is not mandatory,\nbut everything else is.\n\nPlease make sure you do not leave any missing information.")
        except json.decoder.JSONDecodeError:
            self.addAppFrame.pack_forget()
            self.addAppFrame.destroy()
            self.listApps()
            

    def setimg(self, path):
        self.create_frame_with_image(300, 300, 20, path, self.appLogo_)

    def selectfile(self):
        self.filedir = filedialog.askopenfilename( title="Select an .exe file", filetypes=[("Executable Files", "*.exe"), ("Shortcut Files", "*.lnk")])
        if self.filedir:
            self.dir_.delete(0, END)
            self.dir_.insert(0, self.filedir)
            if os.path.basename(self.filedir) != "" and os.path.basename(self.filedir):
                self.appName__.delete(0, END)
                self.appName__.insert(END, os.path.basename(self.filedir.replace(".exe","")))
                print(f"name is: {os.path.basename(self.filedir.replace(".exe",""))}")
            self.setLinkImg()

    def selectfolder(self):
        self.filedir = filedialog.askdirectory()
        if self.filedir:
            self.dir_.delete(0, END)
            self.dir_.insert(0, self.filedir)
            if os.path.basename(self.filedir) != "" and os.path.basename(self.filedir):
                self.appName__.delete(0, END)
                self.appName__.insert(END, os.path.basename(self.filedir))
            self.setimg("./src/libs/apps/folder/folder.png")
            self.appTypeComboBox.set("Folder")

    def selectimage(self):
        self.imagefile = filedialog.askopenfilename(title="Select an image file", filetypes=[(".png files", "*.png")])
        if self.imagefile:
            print(self.imagefile)
            self.selectedimg = self.imagefile
            self.appLogoLabel_.configure(text=self.imagefile)
            self.appLogoLabel_.update_idletasks()
            self.appLogoLabel_.place(x=(300 - self.appLogoLabel_.winfo_reqwidth())/2, y=(300 - self.appLogoLabel_.winfo_reqheight())/2)

            if self.selectedimg == None:
                self.selectedimg = "none"
                self.appIcon = "none"
            else:
                shutil.copy2(self.selectedimg, f"./src/libs/apps/current.png")

            self.create_frame_with_image(
                300,
                300,
                15,
                f"./src/libs/apps/current.png",
                self.appLogo_,
            )

            gc.collect()


    def body(self):
        self.body_frame = CTkScrollableFrame(self, fg_color=self.cget("bg"), corner_radius=0, border_width=0)
        self.body_frame.pack(fill=BOTH, expand=True, pady=(0, 20), padx=(10, 0))
        self.body_frame._scrollbar.configure(width=10)

        self.listApps()
        self.setThemeDefault()

    def setThemeDefault(self):
        with open("./src/data/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            f.close()

        self.hover_color = config["theme"]["button"]["color.hover"]
        self.fg_color = config["theme"]["button"]["color.fg"]
        self.font_family = config["theme"]["font.family"]

    def listApps(self, search=False):
        try:
            if self.body_frame.winfo_ismapped():
                self.body_frame.pack_forget()
                self.body_frame.destroy()

                self.body_frame = CTkScrollableFrame(self, fg_color=self.cget("bg"), corner_radius=0, border_width=0)
                self.body_frame.pack(fill=BOTH, expand=True, pady=(0, 20))
                self.body_frame._scrollbar.configure(width=0)
        except: ...


        self.appList = self.getApps()

        self.appNum = 0
        self.row, self.column = 0, 0  # Satır ve sütun başlangıç noktası

        for a, i in self.appList.items():
            if search and (i["name"].lower().find(search.lower()) != -1): self.listApps_(a, i)
            elif not search: self.listApps_(a, i)

        if not search:
            self.addappArea = CTkButton(self.body_frame, corner_radius=10, border_width=1, width=(self.appWidth-140)/6, height=(self.appHeight-115-20)/2, text_color="#888", fg_color="#303030", border_color="#444", hover_color="#404040", text="➕", font=("Segoe UI Emoji", 100, BOLD), command=self.addApp)
            self.addappArea.place()
            
            try:
                if self.addappArea.winfo_ismapped():
                    self.addappArea.pack_forget()
                    self.addappArea.destroy()

                    self.addappArea.grid_forget()
                    self.addappArea = CTkButton(self.body_frame, corner_radius=10, border_width=1, width=(self.appWidth-140)/6, height=(self.appHeight-115-20)/2, fg_color="#303030", border_color="#444", hover_color="#404040", text="���", font=("Segoe UI Emoji", 100, BOLD), command=self.addApp)
                    self.addappArea.grid(row=self.row, column=self.column, padx=(20, 0), pady=(20, 0), sticky="n")
                    self.column += 1
                    if self.column >= 6:
                        self.column = 0
                        self.row += 1
                else:
                    self.addappArea.grid_forget()
                    self.addappArea.grid(row=self.row, column=self.column, padx=(20, 0), pady=(20, 0), sticky="n")
                    self.column += 1
                    if self.column >= 6:
                        self.column = 0
                        self.row += 1
            except:
                self.addappArea.grid_forget()
                self.addappArea.grid(row=self.row, column=self.column, padx=(20, 0), pady=(20, 0), sticky="n")
                self.column += 1
                if self.column >= 6:
                    self.column = 0
                    self.row += 1

    def changeIcon(self, appName):
        try:
            new_icon = filedialog.askopenfilename(title="Select an image file", filetypes=[(".png files", "*.png")])
            if new_icon:
                # JSON dosyasını oku
                with open("./src/data/apps.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    f.close()

                # Belirtilen uygulamayı bul ve ikonunu güncelle
                if appName in data["apps"]:
                    data["apps"][appName]["icon"] = os.path.basename(new_icon)
                    try:
                        shutil.copy2(new_icon, f"./src/libs/apps/{appName}.png")
                    except FileExistsError:
                        os.remove(f"./src/libs/apps/{appName}.png")
                else:
                    print(f"Uygulama bulunamadı: {appName}")
                    return

                # Güncellenmiş JSON'u dosyaya yaz
                with open("./src/data/apps.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    self.listApps()
                    f.close()
        except json.decoder.JSONDecodeError:
            self.listApps()

    def deleteIcon(self, appName):
        try:
            if True:
                # JSON dosyasını oku
                with open("./src/data/apps.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    f.close()

                # Belirtilen uygulamayı bul ve ikonunu güncelle
                if appName in data["apps"]:
                    if data["apps"][appName]["icon"] != "none":
                        data["apps"][appName]["icon"] = "none"
                        os.remove(f"./src/libs/apps/{appName}.png")
                else:
                    print(f"Uygulama bulunamadı: {appName}")
                    return

                # Güncellenmiş JSON'u dosyaya yaz
                with open("./src/data/apps.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    self.listApps()
                    f.close()
        except json.decoder.JSONDecodeError:
            self.listApps()

    def removeApp(self, appName):
        # JSON dosyasını oku
        with open("./src/data/apps.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()

        if data["apps"][appName]["icon"] != "none" and data["apps"][appName]["icon"] != "folder/folder.png": os.remove(f"./src/libs/apps/{data["apps"][appName]["icon"]}")

        # appName tek bir string ise, listeye dönüştür
        if isinstance(appName, str):
            appName = [appName]

        # Sözlükten belirtilen uygulamaları kaldır
        for app in appName:
            if app in data["apps"]:
                del data["apps"][app]

        # Güncellenmiş JSON'u dosyaya yaz
        with open("./src/data/apps.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()

            self.listApps()
    
    def rightMenu(self, master, namee, i):
        try:
            self.rightMenuFrame.pack_forget()
            self.rightMenuFrame.destroy()
        except:
            ...
        self.rightMenuFrame = CTkFrame(master, corner_radius=10, width=(self.appWidth-140)/6 - 20, height=((self.appHeight-115-20)/2-20), border_width=1, fg_color="#303030")
        self.rightMenuFrame.place(x=10, y=10)

        self.openAppButton = CTkButton(self.rightMenuFrame, border_width=1, corner_radius=7.5, hover_color="#505050", border_color="#505050", height=((self.appHeight-115-20)/2-20)/10, width=(self.appWidth-140)/6-50, text="Start", text_color="#888", fg_color="#404040", bg_color="#303030", font=("Sans-Serif", 18))
        self.openAppButton.place(x=15, y=0+15)
        self.openAppButton.configure(command=lambda: self.openApp(i=i, master=self.openAppButton))

        self.removeAppButton = CTkButton(self.rightMenuFrame, border_width=1, corner_radius=7.5, hover_color="#505050", border_color="#505050", height=((self.appHeight-115-20)/2-20)/10, width=(self.appWidth-140)/6-50, text="Remove App", text_color="#888", fg_color="#404040", bg_color="#303030", font=("Sans-Serif", 18), command=lambda appDir = i["name"]: self.removeApp(appDir))
        self.removeAppButton.place(x=15, y=55+15-((((self.appHeight-115-20)/2-20)/10)/5)*1)

        self.renameAppButton = CTkButton(self.rightMenuFrame, border_width=1, corner_radius=7.5, hover_color="#505050", border_color="#505050", height=((self.appHeight-115-20)/2-20)/10, width=(self.appWidth-140)/6-50, text="Rename App", text_color="#888", fg_color="#404040", bg_color="#303030", font=("Sans-Serif", 18), command=lambda: (
            self.rightMenuFrame.pack_forget(),
            self.rightMenuFrame.destroy(),
            namee.configure(state="normal"),
            namee.focus(),
            self.appName.bind("<Double-Button-1>", lambda e: ...)
        ))
        self.renameAppButton.place(x=15, y=110+15-((((self.appHeight-115-20)/2-20)/10)/5)*2)

        self.changeIconButton = CTkButton(self.rightMenuFrame, border_width=1, corner_radius=7.5, hover_color="#505050", border_color="#505050", height=((self.appHeight-115-20)/2-20)/10, width=(self.appWidth-140)/6-50, text="Mod Icon", text_color="#888", fg_color="#404040", bg_color="#303030", font=("Sans-Serif", 18), command=lambda appDir = i["name"]: self.changeIcon(appDir))
        
        
        self.deleteIconButton = CTkButton(self.rightMenuFrame, border_width=1, corner_radius=7.5, hover_color="#505050", border_color="#505050", height=((self.appHeight-115-20)/2-20)/10, width=(self.appWidth-140)/6-50, text="Del Icon", text_color="#888", fg_color="#404040", bg_color="#303030", font=("Sans-Serif", 18), command=lambda appDir = i["name"]: self.deleteIcon(appDir))

        if i["icon"] != "folder/folder.png":
            if i["icon"] != "none":
                self.changeIconButton.place(x=15, y=165+15-((((self.appHeight-115-20)/2-20)/10)/5)*3)
                self.deleteIconButton.place(x=15, y=220+15-((((self.appHeight-115-20)/2-20)/10)/5)*4)
            else:
                self.changeIconButton.configure(text="Add Icon")


        try:
            self.bind("<Escape>", lambda event: (self.rightMenuFrame.pack_forget(), self.rightMenuFrame.destroy()))
            self.rightMenuFrame.bind("<Button-3>", lambda event: (self.rightMenuFrame.pack_forget(), self.rightMenuFrame.destroy()))
        except: ...

    def renameApp(self, old_name, new_name):
        with open("./src/data/apps.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        if old_name in data["apps"]:
            data["apps"][new_name] = data["apps"].pop(old_name)
            data["apps"][new_name]["name"] = new_name
        else:
            print(f"Uygulama bulunamadı: {old_name}")

        with open("./src/data/apps.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def openApp(self, i, master=False):
        os.startfile(i["appDirectory"])
        if master and i["type"] != "Folder":
            master.configure(text="Running...", state="disabled")
            master.after(2500, lambda: master.configure(text="Start", state="normal"))

    def listApps_(self, a, i):
        self.appNum += 1
        self.appArea = CTkFrame(self.body_frame, corner_radius=10, border_width=1, width=(self.appWidth-140)/6, height=(self.appHeight-115-20)/2, fg_color="#303030", bg_color=self.cget("bg"))
        self.appArea.grid(row=self.row, column=self.column, padx=(17.5, 0), pady=(20, 0), sticky="n")

        self.appLogo = CTkFrame(self.appArea, corner_radius=7.5, width=(self.appWidth-140)/6/10*8, height=(self.appWidth-140)/6/10*8, border_width=1,
                                    fg_color="#404040", bg_color="#353535", border_color="#505050")
        self.appLogo.place(x=((self.appWidth-140)/6 - (self.appWidth-140)/6/10*8)/2 ,y=((self.appWidth-140)/6 - (self.appWidth-140)/6/10*8)/2)

        self.appName = CTkEntry(self.appArea, font=("Sans Serif", 24, "bold"), border_width=0, bg_color="#303030", fg_color="#303030", state="normal", width=(self.appWidth-140)/6 - 40, justify="center")
        self.appType = CTkLabel(self.appArea, text=i["type"], font=("Arial", 16), text_color="#777", bg_color="#303030", height=20)
        self.playBtn = CTkButton(self.appArea, text_color_disabled="white", text="Start", bg_color="#303030", hover_color=self.hover_color, font=("Arial", 20, "bold"), fg_color=self.fg_color, corner_radius=7.5, width=(self.appWidth-140)/6/10*8, height=40)

        if i["icon"] != "none":
            licon = self.create_frame_with_image(
                (self.appWidth-140)/6/10*8,
                (self.appWidth-140)/6/10*8,
                10,
                f"./src/libs/apps/{i["icon"]}",
                self.appLogo,
                self.appArea,
                i
            )

        else:
            self.appLogoLabelFont = 100
            self.appLogoLabelText = ""
            self.appLogoLabelHowManyChar = 0
            for b in i["name"].split(" "):
                self.appLogoLabelText = self.appLogoLabelText + b[:1]
                self.appLogoLabelHowManyChar += 1
            
            if self.appLogoLabelHowManyChar != 1: self.appLogoLabelFont = int(self.appLogoLabelFont / (self.appLogoLabelHowManyChar + 1) * self.appLogoLabelHowManyChar)
            else: self.appLogoLabelFont = 80
        
            self.appLogoLabel = CTkLabel(self.appLogo, text=self.appLogoLabelText.upper(), font=("Arial", self.appLogoLabelFont, "bold"), text_color="#777")
            self.appLogoLabel.place()
            self.appLogoLabel.update_idletasks()
            label_width = self.appLogoLabel.winfo_reqwidth()
            new_x_position = ((self.appWidth-140)/6/10*8 - label_width) / 2

            self.appLogoLabel.place(x=new_x_position, y=((self.appWidth-140)/6/10*8-self.appLogoLabelFont)/2)

            self.appLogoLabel.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appLogoLabel.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appLogoLabel.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
        
        self.appName.place()
        self.appName.insert(END, f"{i["name"]}")
        self.appName.configure(state="disabled")
        self.appName.update_idletasks()
        label_width = self.appName.winfo_reqwidth()
        new_x_position = ((self.appWidth - 140) / 6 - label_width) / 2

        self.appName.bind("<Return>", lambda event, appN = i["name"]: (
            self.renameApp(appN, self.appName.get()),
            self.appName.configure(state="disabled"),
            self.listApps(),
            self.appArea.bind("<Double-Button-1>", lambda e: self.openApp(i))
        ))

        self.appName.bind("<Key>", self.reset_timer)


        self.appName.place(x=new_x_position, y=(self.appHeight-115-20)/2 - ((self.appWidth-140)/6 - (self.appWidth-140)/6/10*8)/2 - 105)

        self.appType.place()
        self.appType.update_idletasks()
        label_width_ = self.appType.winfo_reqwidth()
        new_x_position_ = ((self.appWidth - 140) / 6 - label_width_) / 2

        self.appType.place(x=new_x_position_, y=(self.appHeight-115-20)/2 - ((self.appWidth-140)/6 - (self.appWidth-140)/6/10*8)/2 - 72.5)

        self.playBtn.place(x=((self.appWidth-140)/6 - (self.appWidth-140)/6/10*8)/2, y=(self.appHeight-115-20)/2 - ((self.appWidth-140)/6 - (self.appWidth-140)/6/10*8)/2 - 45)
        self.playBtn.configure(command=lambda master=self.playBtn: self.openApp(i=i, master=master))

        self.appType.bind("<Double-Button-1>", lambda e: self.openApp(i))
        self.appName.bind("<Double-Button-1>", lambda e: self.openApp(i))
        self.appArea.bind("<Double-Button-1>", lambda e: self.openApp(i))
        self.appLogo.bind("<Double-Button-1>", lambda e: self.openApp(i))
        try:
            self.appType.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#353535"), appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appType.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#303030"), appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appType.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
            
            self.appName.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#353535"), appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appName.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#303030"), appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appName.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
            
            self.playBtn.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#353535"), appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.playBtn.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#303030"), appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.playBtn.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
            
            self.appArea.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#353535"), appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appArea.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#303030"), appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appArea.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
            
            self.appLogo.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#353535"), appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appLogo.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = licon: (image_label.configure(fg_color="#303030"), appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appLogo.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
        except UnboundLocalError:
            self.appType.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appType.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appType.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
            
            self.appName.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appName.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appName.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
            
            self.playBtn.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.playBtn.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.playBtn.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
            
            self.appArea.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appArea.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appArea.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))
            
            self.appLogo.bind("<Enter>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
            self.appLogo.bind("<Leave>", lambda event, appArea =self.appArea, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType: (appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
            self.appLogo.bind("<Button-3>", lambda event,  master=self.appArea, namee=self.appName: self.rightMenu(master, namee, i))


        self.column += 1
        if self.column >= 6:
            self.column = 0
            self.row += 1

    def create_frame_with_image(self, width, height, corner_radius, image_path, master, o_master=False, i=False, bg_color=False):
        """Bir CTkFrame içerisine köşe yarıçapı belirlenmiş bir resim ekler."""
        
        try:
            if image_path.startswith("http://") or image_path.startswith("https://"):
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                }
                response = requests.get(image_path, headers=headers)
                response.raise_for_status()  # Eğer hata olursa exception fırlatır
                image = PIL.Image.open(BytesIO(response.content))
                with open("./src/libs/apps/current.png", "wb") as f:
                    f.write(response.content)
                    f.close()
            else:
                # Yerel dosyadan resmi yükle
                image = PIL.Image.open(image_path)

            image = image.resize((int(width), int(height)))
            rounded_image = PIL.Image.new("RGBA", image.size, (0, 0, 0, 0))

            # Köşeleri yuvarlama
            mask = PIL.Image.new("L", image.size, 0)
            draw = PIL.ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), corner_radius, fill=255)
            rounded_image.paste(image, (0, 0), mask)

            # Resmi `PhotoImage` formatına dönüştürme
            self.photo = PIL.ImageTk.PhotoImage(rounded_image)

            if not bg_color:
                bg_color_ = "#303030"
            else:
                bg_color_ = bg_color

            # Resmi bir Label'e ekleme ve çerçevenin içine yerleştirme
            self.image_label = CTkLabel(master, image=self.photo, text="", corner_radius=corner_radius, bg_color=bg_color_, fg_color="#303030")
            self.image_label.place(relx=0.5, rely=0.5, anchor="center")

            try:
                if master == self.appLogo:
                    try:
                        self.image_label.bind("<Enter>", lambda event, appArea =o_master, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = self.image_label: (image_label.configure(fg_color="#353535"), appArea.configure(fg_color="#353535"), appLogo.configure(bg_color="#353535"), playBtn.configure(bg_color="#353535"), appType.configure(bg_color="#353535"), appName.configure(bg_color="#353535", fg_color="#353535")))
                        self.image_label.bind("<Leave>", lambda event, appArea =o_master, playBtn = self.playBtn, appName = self.appName, appLogo = self.appLogo, appType = self.appType, image_label = self.image_label: (image_label.configure(fg_color="#303030"), appArea.configure(fg_color="#303030"), appLogo.configure(bg_color="#303030"), playBtn.configure(bg_color="#303030"), appType.configure(bg_color="#303030"), appName.configure(bg_color="#303030", fg_color="#303030")))
                        self.image_label.bind("<Button-3>", lambda event,  master_=o_master, namee=self.appName: self.rightMenu(master_, namee, i))
                        self.image_label.bind("<Double-Button-1>", lambda e: self.openApp(i))
                    except TclError: ...
                else: self.image_label.bind("<Button-1>", lambda event: self.selectimage())
            except AttributeError as e: pass
            except: pass

            return self.image_label
        except FileNotFoundError: ...
    def getApps(self):
        with open("./src/data/apps.json", "r", encoding="utf-8") as f:
            self.apps = json.load(f)
            f.close()

        return self.apps["apps"]


if __name__ == "__main__":
    app = App()
    app.mainloop()