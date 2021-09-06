import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
test_img = ImageTk.PhotoImage(Image.open('./bin/cog.png'))
label = tk.Label(image=test_img)
label.pack()

root.mainloop()
