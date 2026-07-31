import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import sys
if getattr(sys, 'frozen', False):
    FOLDER_DE_BAZA = os.path.dirname(sys.executable)
else:
    FOLDER_DE_BAZA = os.path.dirname(os.path.abspath(__file__))
FOLDER_MESSIER = os.path.join(FOLDER_DE_BAZA, "messier")
class JocMessier:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Messier")
        self.root.geometry("900x780")
        self.root.configure(bg="black")
        self.lista_imagini = []
        self.nume_obiecte = []
        self.index_curent = 0
        self.scor = 0

        self.label_scor = tk.Label(root, text="Scor: 0", font=("Arial", 16, "bold"), bg="black", fg="white")
        self.label_scor.pack(pady=(10, 0))

        self.label_imagine = tk.Label(root, bg="black")
        self.label_imagine.pack(expand=True, fill="both", pady=10)
        self.frame_butoane = tk.Frame(root, bg="black")
        self.frame_butoane.pack(pady=10)

        self.butoane = []
        for i in range(4):
            btn = tk.Button(
                self.frame_butoane, text="", font=("Arial", 14), width=20, height=2,
                command=lambda i=i: self.verifica_raspuns(i)
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.butoane.append(btn)
        btn_shuffle = tk.Button(
            root, text="🔀 SHUFFLE", font=("Arial", 16, "bold"),
            bg="#FF9800", fg="white", activebackground="#FB8C00", activeforeground="white",
            relief="raised", bd=4, padx=20, pady=10,
            command=self.amesteca
        )
        btn_shuffle.pack(pady=20)
        self.incarca_folder(FOLDER_MESSIER)
    def incarca_folder(self, folder):
        if not os.path.isdir(folder):
            return
        extensii_valide = (".jpg")
        fisiere = [f for f in os.listdir(folder) if f.lower().endswith(extensii_valide)]
        if not fisiere:
            return
        random.shuffle(fisiere)
        self.lista_imagini = [os.path.join(folder, f) for f in fisiere]
        self.nume_obiecte = [os.path.splitext(f)[0] for f in fisiere]
        self.index_curent = 0
        self.afiseaza_intrebare()
    def amesteca(self):
        combinate = list(zip(self.lista_imagini, self.nume_obiecte))
        random.shuffle(combinate)
        self.lista_imagini, self.nume_obiecte = zip(*combinate)
        self.lista_imagini = list(self.lista_imagini)
        self.nume_obiecte = list(self.nume_obiecte)
        self.index_curent = 0
        self.scor = 0
        self.label_scor.config(text="Scor: 0")
        for btn in self.butoane:
            btn.grid()
        self.afiseaza_intrebare()
    def afiseaza_intrebare(self):
        if self.index_curent >= len(self.lista_imagini):
            self.label_imagine.config(image="", text=f"You've finished all the images! 🎉\nScor final: {self.scor}/{len(self.lista_imagini)}",
                                       font=("Arial", 20), fg="white")
            for btn in self.butoane:
                btn.grid_remove()
            return
        cale = self.lista_imagini[self.index_curent]
        imagine = Image.open(cale)
        imagine.thumbnail((700, 480))
        imagine_tk = ImageTk.PhotoImage(imagine)
        self.label_imagine.config(image=imagine_tk)
        self.label_imagine.image = imagine_tk
        nume_corect = self.nume_obiecte[self.index_curent]
        alte_nume = [n for i, n in enumerate(self.nume_obiecte) if i != self.index_curent]
        gresite = random.sample(alte_nume, min(3, len(alte_nume)))
        optiuni = gresite + [nume_corect]
        random.shuffle(optiuni)
        self.nume_corect_curent = nume_corect
        for i, btn in enumerate(self.butoane):
            btn.config(text=optiuni[i], bg="SystemButtonFace", state="normal")
    def verifica_raspuns(self, index_buton):
        text_ales = self.butoane[index_buton]["text"]

        if text_ales == self.nume_corect_curent:
            self.butoane[index_buton].config(bg="#4CAF50")
            self.scor += 1
            self.label_scor.config(text=f"Scor: {self.scor}")
            for btn in self.butoane:
                btn.config(state="disabled")
            self.root.after(800, self.imagine_urmatoare)
        else:
            self.butoane[index_buton].config(bg="#F44336", state="disabled")  # roșu, dezactivat

    def imagine_urmatoare(self):
        self.index_curent += 1
        self.afiseaza_intrebare()
if __name__ == "__main__":
    root = tk.Tk()
    app = JocMessier(root)
    root.mainloop()
