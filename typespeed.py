import time
import tkinter as tk
from tkinter import messagebox
from essential_generators import DocumentGenerator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.gen = DocumentGenerator()
        self.String = ""
        self.wordcount = 0
        self.results = 0
        self.start_button = tk.Button(self.root, text="Start Typing", command=self.start_typing)

        self.create_widgets()

    def initialise_graph(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.ax.set_title('Performance')
        self.ax.set_ylabel('WPM')
        self.ax.set_xlabel('Y-axis')

        self.x_values = []
        self.y_values = []
        self.ax.plot(self.x_values, self.y_values)
        self.ax.set_xlim(0, 7)
        self.ax.set_ylim(0, 120) 
    
    def plot_wpm(self,wpm):
        self.results = self.results + 1
        self.y_values.append(wpm)
        self.x_values.append(self.results)
        self.ax.plot(self.x_values,self.y_values,"o-b")
        self.canvas.draw()

    def create_widgets(self):
        self.instructions_label = tk.Label(self.root, text="Type the sentence below:", font=("Arial", 12))
        self.instructions_label.grid(row=0,column=0,columnspan=3)

        self.sentence_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400)
        self.sentence_label.grid(row=1,column=0,columnspan=3)

        self.input_text = tk.Text(self.root, width=50, height=5, font=("Arial", 12))
        self.input_text.grid(row=2,column=0,columnspan=3,rowspan=3)
        
        self.initialise_graph()

        self.canvas.draw()
        self.canvas.get_tk_widget().config(width=300, height=200)
        self.canvas.get_tk_widget().grid(row=2,column=3,rowspan=3,padx=20,pady=20)

        self.start_button.grid(row=5,columnspan=3,column=0)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.grid(row=6,column=0,columnspan=3)

    def start_typing(self):
        self.String = self.gen.sentence()
        self.wordcount = len(self.String.split())

        self.sentence_label.config(text=self.String)
        self.input_text.delete("1.0", tk.END)
        self.input_text.focus_set()

        self.start_time = time.time()

        self.start_button.config(text="Submit", command=self.show_result)

    def show_result(self):
        endTime = time.time()
        textInput = self.input_text.get("1.0", tk.END).strip()

        accuracy = len(set(textInput.split()) & set(self.String.split())) / self.wordcount * 100
        timeTaken = round(endTime - self.start_time, 2)
        wpm = round((self.wordcount / timeTaken) * 60)

        self.result_label.config(text=f"Accuracy: {accuracy:.2f}%\nTime taken: {timeTaken} seconds\nTyping speed: {wpm} words per minute")

        if accuracy < 50 or wpm < 30:
            messagebox.showinfo("Result", "You need to practice typing more!")
        elif accuracy < 80 or wpm < 60:
            messagebox.showinfo("Result", "You are doing great!")
        elif accuracy <= 100 or wpm <= 100:
            messagebox.showinfo("Result", "You are a pro in typing!")
        else:
            messagebox.showinfo("Result", "You are a typing machine!")

        self.plot_wpm(wpm)

        self.start_button.config(text="Start Again", command=self.start_typing)

    def on_enter_key(self,event):
        self.start_button.invoke()

root = tk.Tk()
t = TypingSpeedTest(root)
root.bind('<Return>', t.on_enter_key)
root.mainloop()
