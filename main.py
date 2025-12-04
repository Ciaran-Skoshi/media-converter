import customtkinter
from customtkinter import filedialog

from PIL import Image
import ffmpeg

imgSaveOptions = (".avif", ".bmp", ".dds", ".gif", ".ico", ".jpeg", ".png", ".webp")

imgOpenOptions = ".avif .avifs .blp .bmp .bufr .dds .dib .eps .ps .grib .h5 .hdf .icns .ico .im .jfif .jpe .jpeg " \
".jpg .j2c .j2k .jp2 .jpc .jpf .jpx .msp .pcx .apng .png .pbm .pfm .pgm .pnm .ppm .qoi .bw .rgb .rgba " \
".sgi .ras .icb .tga .vda .vst .tif .tiff .webp .emf .wmf .xbm"


vidSaveOptions = (".gif", ".mp4", ".mkv", ".mov", ".avi", ".wmv", ".ogg", "--Audio Files--", ".mp2")

selectedVideo = ""

selectedImage = None
OutputFolder = ""

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

        self.statusLabel = customtkinter.CTkLabel(self, text="")
        self.statusLabel.grid(row=7, column=0, padx=20)

    def selectFile(self):
        global selectedImage, selectedVideo, imgSaveOptions, imgOpenOptions, vidSaveOptions
        
        selectedVideo = None
        selectedImage = None

        supportedFiles = (("Image files", imgOpenOptions), ("Video files", vidSaveOptions))
        filename = filedialog.askopenfilename(filetypes=supportedFiles)

        if filename.endswith(vidSaveOptions):
            selectedVideo = filename
            self.convertOptions.configure(values=vidSaveOptions)
        
        else:
            selectedImage = Image.open(filename)
            self.convertOptions.configure(values=imgSaveOptions)
        
        self.selectedLabel.configure(text=filename)
        self.convertButton.configure(text="Convert")

    def selectOutputFolder(self):
        global OutputFolder
        OutputFolder = filedialog.askdirectory() + "/"
        self.selectedFolderLabel.configure(text=OutputFolder)
    
    def convertFile(self):
        global selectedImage, selectedVideo, OutputFolder
        if self.convertOptions.get() == "Please select a source file" or self.convertOptions.get() == "--Audio Files--":
            return

        #Why the fuck does this not work??
        #It seems the configure functions get called AFTER the save and ffmpeg functions, for some fucking reason
        #self.statusLabel.configure(text="Working")
        if not selectedImage == None:
            selectedImage.save(OutputFolder + self.nameEntry.get() + self.convertOptions.get(), self.convertOptions.get().removeprefix("."))
            self.statusLabel.configure(text="Done!")
        
        elif not selectedVideo == None:
            ffmpeg.input(selectedVideo).output(OutputFolder + self.nameEntry.get() + self.convertOptions.get()).run()
            self.statusLabel.configure(text="Done!")



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("640x360")
        self.title("Media Converter")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20) #sticky="nsew"
    


app = App()
app.mainloop()