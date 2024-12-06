#import moviepy as mp
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
import os
import shutil
import whisper
import glob
from transformers import pipeline
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
model = whisper.load_model("turbo")

folder_za_import = os.path.join(os.path.dirname(__file__), "video_datoteke")
folder_za_transkripciju = os.path.join(os.path.dirname(__file__), "text_datoteke")

def import_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Video files", "*.mp4"), ("All files", "*.*")])
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(folder_za_import, file_name)

    if file_path:
        shutil.copy(file_path, destination_path)
        print("Uspješno predana datoteka")
        if len([name for name in os.listdir(folder_za_import)]):
            messagebox.showinfo("showinfo", "Uspješno uploadana datoteka") 
        transcribe_file(folder_za_import)
        

def import_folder():
    file_path = filedialog.askdirectory(title="Select a folder")
    messagebox.showinfo("showinfo", "Uspješno uploadana mapa")
    transcribe_file(file_path)

#nepotrebno jer ipak whisper može podržati iz videa u tekst
'''def change_file():
    if not len([name for name in os.listdir(folder_za_import)]):
      messagebox.showerror("showerror", "Ne mogu se obraditi datoteke jer nije predana nijedna datoteka")
      #u folder za import stavi putanju na folder koji je uploadan

    for file in os.listdir(folder_za_import):
        if file.endswith(".mp4"):
            audio_ime = file[:-4] + '.mp3'
            audio_putanja = os.path.join(folder_za_audio, audio_ime)
            ime = os.path.join(folder_za_import, file)
            video = mp.VideoFileClip(ime)
            video.audio.write_audiofile(audio_putanja)
        #else if ako je već predan mp3, samo ga stavi u točan folder
    messagebox.showinfo("showinfo", "Uspješno obrađene datoteke") 
'''

def transcribe_file(putanja_za_folder):
    if not len([name for name in os.listdir(putanja_za_folder)]):
      print(putanja_za_folder)
      messagebox.showerror("showerror", "Ne mogu se obraditi datoteke jer nije predana nijedna datoteka")

    messagebox.showinfo("showinfo", "Započela je transkripcija")
    for file in (os.listdir(putanja_za_folder)):
        if file == 'desktop.ini':
            print("Preskoči ovu datoteku")
        else:
            putanja_za_model = os.path.join(putanja_za_folder, file)
            ime = file[:-4] + '.txt'
            putanja_za_text = os.path.join(folder_za_transkripciju, ime)
            results = model.transcribe(putanja_za_model)
            f = open(putanja_za_text, "w", encoding="utf-8")
            f.write(results["text"])
            f.close()
    if len([name for name in os.listdir(folder_za_transkripciju)]):
        messagebox.showinfo("showinfo", "Uspješna transkripcija") 

def summarize_file():
    if not len([name for name in os.listdir(folder_za_transkripciju)]):
      messagebox.showerror("showerror", "Ne mogu se obraditi datoteke jer nije predana nijedna datoteka")

    messagebox.showinfo("showinfo", "Započelo je sažimanje teksta") 
    for file in os.listdir(folder_za_transkripciju):
        file_path = os.path.join(folder_za_transkripciju, file)
        with open(file_path, "r", encoding="utf-8") as file: 
            text_to_summarize = file.read()
            text_length = len(text_to_summarize)
            text_int = text_length//1000
            text_rest = text_length - text_int*1000
            text_final = text_to_summarize[(text_int*1000):(text_int*1000 + text_rest)]
            for i in range (1, text_int + 1):
                j = i - 1
                text_summarize = text_to_summarize[j*1000:i*1000]
                sazetak = summarizer(text_summarize, max_length=int(len(text_summarize)*0.25), min_length=int(len(text_summarize)*0.1), do_sample=False)
                with open(file_path, "a", encoding="utf-8") as file:
                    string1 = str(sazetak)
                    string2 = string1[19:-3]
                    file.write("\n")
                    final_sazetak = "\n" + string2
                    file.write(final_sazetak)
                    file.close()
            sazetak = summarizer(text_final, max_length=int(len(text_final)*0.25), min_length=int(len(text_final)*0.1), do_sample=False)
            with open(file_path, "a", encoding="utf-8") as file:
                    string1 = str(sazetak)
                    string2 = string1[19:-3]
                    file.write("\n")
                    final_sazetak = "\n" + string2
                    file.write(final_sazetak)
                    file.close()
    
    messagebox.showinfo("showinfo", "Uspješno napisan sažetak") 

def izaberi_folder():
    file_path = filedialog.askdirectory(title="Select a folder")
    if file_path:
        messagebox.showinfo("showinfo", "Uspješno uploadana mapa")
    msg = messagebox.askyesno("askyesno", "Ako kliknete da, sačuvati će vam se .txt datoteke, ali ako kliknete ne će vam se pohraniti kao pdf datoteke")
    if msg == True:
        for file in os.listdir(folder_za_transkripciju):
            stari_file = os.path.join(folder_za_transkripciju, file)
            novi_file = os.path.join(file_path, file)
            shutil.copy(stari_file, novi_file)
    #if msg == False:
        #transform_pdf(file_path)
        

'''def transform_pdf(file_putanja): 
    if not len([name for name in os.listdir(folder_za_transkripciju)]):
      messagebox.showerror("showerror", "Ne mogu se obraditi datoteke jer nije predana nijedna datoteka")
    for file in os.listdir(folder_za_transkripciju):
        #input file
        file_path = os.path.join(folder_za_transkripciju, file)
        #output file
        file_name = file[:-4] + '.pdf'
        file_final = os.path.join(file_putanja, file_name)
        c = canvas.Canvas(file_final, pagesize=letter)
    width, height = letter 
    c.setFont("Helvetica", 10)
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    y = height - 40  
    line_height = 12  

    for line in lines:
        if y < 40:  
            c.showPage()  
            c.setFont("Helvetica", 10)
            y = height - 40
        
        c.drawString(40, y, line.strip())  
        y -= line_height
    
    c.save()
'''

def delete_file():
    msg = messagebox.askyesno("askyesno", "Jeste li sigurni da žeilte obrisati datoteke? Ako niste pohranili tekst u drugu mapu, on će se trajno izbrisati.")
    if msg == True:
        velicina_importa = len([name for name in os.listdir(folder_za_import)])
        velicina_transkripcija = len([name for name in os.listdir(folder_za_transkripciju)])
        file_delete_video = glob.glob(os.path.join(folder_za_import, '*'))
        file_delete_text = glob.glob(os.path.join(folder_za_transkripciju, '*'))
        if velicina_importa:
            for file in file_delete_video:
                os.remove(file)
        if velicina_transkripcija:
            for file in file_delete_text:
                os.remove(file)


'''

def txt_to_pdf(input_file, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter 
    c.setFont("Helvetica", 10)
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    y = height - 40  # Top margin
    line_height = 12  # Space between lines

    for line in lines:
        if y < 40:  
            c.showPage()  
            c.setFont("Helvetica", 10)
            y = height - 40
        
        c.drawString(40, y, line.strip())  
        y -= line_height
    
    c.save()

# Convert a .txt file to PDF
txt_to_pdf("example.txt", "output.pdf")
'''
        
root = tk.Tk()
root.title("Aplikacija")
root.geometry('560x400')


'''root.style = ttk.Style(root)
root.style.configure('basic_button', 
                    bg="SteelBlue4", 
                    activebackground="DodgerBlue4", 
                    fg="white smoke",
                    height = 10,
                    width = 30)'''

root.config(bg="skyblue")

style = ttk.Style()

style.configure('TButton', bg = "blue",
                font =
               ('calibri', 15, 'bold'), 
                    foreground = "black",
                    height = 15,
                    width = 30)

style.map('TButton', bg = [('active', 'navy')])

import_button = ttk.Button(root, text="IZABERITE DATOTEKU", command=import_file)
import_button.pack(pady=20)

folder_button = ttk.Button(root, text="IZABERITE MAPU DATOTEKA", command=import_folder)
folder_button.pack(pady=20)

summary_button = ttk.Button(root, text="DODAJ SAŽETAK", command=summarize_file)
summary_button.pack(pady=20)

putanja_button = ttk.Button(root, text="IZABERI FOLDER GDJE ĆE SE NALAZITI TEKST DATOTEKE", command=izaberi_folder)
putanja_button.pack(pady=20)

#pdf_button = tk.Button(root, text="Turn the .txt into .pdf", command=transform_pdf)
#pdf_button.pack(pady=10)

delete_button = ttk.Button(root, text="IZBRIŠI DATOTEKE IZ PROGRAMA", command=delete_file)
delete_button.pack(pady=20)

root.mainloop()
