import customtkinter
from customtkinter import filedialog

from PIL import Image

imgOptions = [".avif", ".avifs", ".bmp", ".dds", ".ico", ".jpe", ".jpeg", ".jpg", ".png", ".webp"]

exts = ".avif .avifs .blp .bmp .bufr .dds .dib .eps .ps .grib .h5 .hdf .icns .ico .im .jfif .jpe .jpeg " \
".jpg .j2c .j2k .jp2 .jpc .jpf .jpx .msp .pcx .apng .png .pbm .pfm .pgm .pnm .ppm .qoi .bw .rgb .rgba " \
".sgi .ras .icb .tga .vda .vst .tif .tiff .webp .emf .wmf .xbm"

selectedImage = None
OutputFolder =""

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.selectFileButton = customtkinter.CTkButton(self, text="Select File", command=self.selectFile)
        self.selectFileButton.grid(row=0, column=0, padx=5)
        
        self.selectedLabel = customtkinter.CTkLabel(self, text="")
        self.selectedLabel.grid(row=1, column=0, padx=20)
        
        self.nameEntry = customtkinter.CTkEntry(self, placeholder_text="New file name")
        self.nameEntry.grid(row=2, column=0, padx=20)
        
        self.convertOptions = customtkinter.CTkOptionMenu(self, values=["Please select a source file"])
        self.convertOptions.grid(row=3, column=0, padx=20)
        
        self.selectOutputButton = customtkinter.CTkButton(self, text="Select output folder", command=self.selectOutputFolder)
        self.selectOutputButton.grid(row=4, column=0, padx=20)
        
        self.selectedFolderLabel = customtkinter.CTkLabel(self, text="")
        self.selectedFolderLabel.grid(row=5, column=0, padx=20)
        
        self.convertButton = customtkinter.CTkButton(self, text="Please select a file format", command=self.convertFile)
        self.convertButton.grid(row=6, column=0, padx=20)

    def selectFile(self):
        global selectedImage, imgOptions, exts
        
        supportedFiles = (("Image files", exts),)
        filename = filedialog.askopenfilename(filetypes=supportedFiles)
        
        selectedImage = Image.open(filename)
        
        self.selectedLabel.configure(text=filename)
        
        self.convertOptions.configure(values=imgOptions)
        
        self.convertOptions.set(imgOptions[0])
        self.convertButton.configure(text="Convert")

    def selectOutputFolder(self):
        global OutputFolder
        OutputFolder = filedialog.askdirectory() + "/"
        self.selectedFolderLabel.configure(text=OutputFolder)
    
    def convertFile(self):
        global selectedImage, OutputFolder
        if self.convertOptions.get() == "Please select a source file":
            return
        selectedImage.save(OutputFolder + self.nameEntry.get() + self.convertOptions.get(), self.convertOptions.get().removeprefix("."))



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("640x360")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20) #sticky="nsew"
    


app = App()
app.mainloop()