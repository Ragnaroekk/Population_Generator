# Author: Ray Franklin
# Population Generator CS361
# Built with research from https://realpython.com/python-gui-tkinter/


import tkinter as tk


window = tk.Tk()
window.title("Test Title")

greeting = tk.Label(text="Hello, Tkinter")

greeting.pack()

label = tk.Label(
    text="Hello, Tkinter",
    fg="white",
    bg="black",
    width=10,
    height=10
)

button = tk.Button(
    text="Display Results!",
    width=10,
    height=5,
    bg="green",
    fg="white",
)

button.pack()

frame_a = tk.Frame()
frame_b = tk.Frame()

label_a = tk.Label(master=frame_a, text="I'm in Frame A")
label_a.pack()

label_b = tk.Label(master=frame_b, text="I'm in Frame B")
label_b.pack()

frame_a.pack()
frame_b.pack()

state = tk.Label(text="State:")
entry = tk.Entry(fg="yellow", bg="blue", width=50)

state.pack()
entry.pack()

test = entry.get()
print(test)
entry.delete(0, tk.END)

window.mainloop()