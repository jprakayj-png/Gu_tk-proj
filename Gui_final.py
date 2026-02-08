
# Final version

import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from PIL import Image, ImageGrab, ImageTk
from tkinter import colorchooser
from tkinter import messagebox
 
root = tk.Tk()
root.title("Mini Paint App")
root.geometry("1800x900+100+50")
 
last_x, last_y = None, None
end_x, end_y = None, None
current_color = "black"
current_fill = "black"
current_tool = "brush"
open_image = None
# chatGPT stuff dont change
def save_canvas():
    file_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        save_as_png(canvas, file_path[:-4])
 
def save_as_png(canvas, fileName):
    # locate the canvas
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    img = ImageGrab.grab(bbox=(x, y, x1, y1))
    img.save(fileName + ".png")
 
def open_file():
    global open_image
    file_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((canvas.winfo_width(), canvas.winfo_height()))
        open_image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=open_image, anchor="nw")
#end of chatGPT dont change stuff
 
def choose_color(color_number):
    global current_color
    global current_fill
    color = colorchooser.askcolor(color=current_color)[1]
    if color:
        if color_number == 1:
            current_color = color
        else:
            current_fill = color
            status.config(text=f"Color: {current_color} | Size: {brush_size.get()} | Tool: {current_tool}")
 
def update_tool(tool):
    global current_color
    global current_tool
    current_tool = tool
    if current_tool == "eraser":
        current_color = "white"
    elif current_tool == "brush":
        current_color = "black"
    elif current_tool == "pencil":
        current_color = "black"
 
    update_brush_size()
 
def update_brush_size():
    if current_tool == "pencil":
        size = 1
    else:
        size = brush_size.get()
    status.config(text=f"Color: {current_color} | Size: {size} | Tool: {current_tool}")
 
# Exit confirmation function
def on_exit():
    confirm = messagebox.askyesnocancel("Quit", "Do you want to save before closing?")
    if confirm:
        save_canvas()
        root.destroy()
    elif confirm is False:  
        root.destroy()
    else:  
        pass
 
# Open new sketch
def new_sketch():
    confirm = messagebox.askyesnocancel("Before open new sketch", "Save before open a new sketch?")
    if confirm:
        save_canvas()
        clear_canvas()
    elif confirm is False:
        clear_canvas()
    else:
        pass
 
# drawing stuff (don't edit)
def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
 
def draw(event):
    global last_x, last_y
    if current_tool in ["brush", "eraser", "pencil"]:  # include pencil
        if last_x and last_y:
            # different width for pencil
            if current_tool == "pencil":
                width = 1  # always thin
            else:
                width = brush_size.get()
 
            canvas.create_line(
                last_x, last_y, event.x, event.y,
                width=width,
                fill=current_color,
                capstyle=tk.ROUND,
                smooth=True
            )
        last_x, last_y = event.x, event.y
 
def reset_draw(event):
    global last_x, last_y, end_x, end_y
    if current_tool in ["square", "circle"]:
        end_x, end_y = event.x, event.y
        draw_shape()
    last_x, last_y = None, None
 
# shape drawing
def draw_shape():
    global last_x, last_y, end_x, end_y, current_color
    if last_x != None and last_y != None and end_x != None and end_y != None:
        if current_tool == "square":
            canvas.create_rectangle(last_x, last_y, end_x, end_y,
                                    outline=current_color, width=brush_size.get(), fill=current_fill)
        elif current_tool == "circle":
            canvas.create_oval(last_x, last_y, end_x, end_y,
                               outline=current_color, width=brush_size.get(), fill=current_fill)
def end_draw(event):
    global end_x, end_y
    end_x, end_y = event.x, event.y
    draw_shape()
# end of drawing stuff
 
def clear_canvas():
    canvas.delete("all")
 
# menubar
menubar = tk.Menu(root)
root.config(menu=menubar)
 
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New Sketch", command=new_sketch)
file_menu.add_command(label="Open", command=open_file)   # << NEW OPEN FUNCTION
file_menu.add_command(label="Save", command=save_canvas)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)  # attach new exit
menubar.add_cascade(label="File", menu=file_menu)
 
tools_menu = tk.Menu(menubar, tearoff=0)
tools_menu.add_command(label="Brush", command=lambda: update_tool("brush"))
tools_menu.add_command(label="Eraser", command=lambda: update_tool("eraser"))
tools_menu.add_command(label="Pencil", command=lambda: update_tool("pencil"))
tools_menu.add_command(label="Shapes")
menubar.add_cascade(label="Tools", menu=tools_menu)
 
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About")
menubar.add_cascade(label="Help", menu=help_menu)
 
toolbar = tk.Frame(root, pady=5)
toolbar.pack(side=tk.TOP, fill=tk.X)
 
# brush size
tk.Label(toolbar, text="Brush Size:").pack(side=tk.LEFT, padx=5)
brush_size = tk.Scale(toolbar, from_=1, to=40, orient=tk.HORIZONTAL, command=lambda x: update_brush_size())
brush_size.set(5)
brush_size.pack(side=tk.LEFT)
 
# color button
color_btn = tk.Button(toolbar, text="Choose Color", command=lambda: choose_color(1))
color_btn.pack(side=tk.LEFT, padx=5)
 
# color2 button
color_btn = tk.Button(toolbar, text="Choose Color 2", command=lambda: choose_color(2))
color_btn.pack(side=tk.LEFT, padx=5)
 
# brush button
brush_btn = tk.Button(toolbar, text="Brush", command=lambda: update_tool("brush"))
brush_btn.pack(side=tk.LEFT, padx=5)
 
# eraser button
eraser_btn = tk.Button(toolbar, text="Eraser", command=lambda: update_tool("eraser"))
eraser_btn.pack(side=tk.LEFT, padx=5)
 
# pencil button
pencil_btn = tk.Button(toolbar, text="Pencil", command=lambda: update_tool("pencil"))
pencil_btn.pack(side=tk.LEFT, padx=5)
 
# shape dropdown
shape_options = ["square", "circle"]
shape_var = tk.StringVar(value="square")
 
def shape_selected(value):
    update_tool(value)
 
shape_menu = tk.OptionMenu(toolbar, shape_var, *shape_options, command=shape_selected)
shape_menu.config(width=10)
shape_menu.pack(side=tk.LEFT, padx=5)
 
# clear button
clear_btn = tk.Button(toolbar, text="Clear Canvas", command=clear_canvas)
clear_btn.pack(side=tk.LEFT, padx=5)
 
# save button
save_btn = tk.Button(toolbar, text="Save", command=save_canvas)
save_btn.pack(side=tk.LEFT, padx=5)
 
# canvas
canvas = tk.Canvas(root, bg="white", cursor="cross")
canvas.pack(fill=tk.BOTH, expand=True)
 
# drawing picture (don't edit)
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", reset_draw)
 
# Status Bar
status = tk.Label(root, text=f"Color: Black | Size: {brush_size.get()} | Tool: {current_tool}",
                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side=tk.BOTTOM, fill=tk.X)
 
# Handle window close button
root.protocol("WM_DELETE_WINDOW", on_exit)
 
# Run code
tk.mainloop()
