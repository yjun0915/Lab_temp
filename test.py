import tkinter as tk

def check():
    print("s_count:", s_count.get())
    print("s_efficient:", s_efficient.get())
    print("s_position:", s_position.get())

root = tk.Tk()

s_count = tk.IntVar()
s_efficient = tk.IntVar()
s_position = tk.IntVar()

tk.Checkbutton(root, text='counts data', variable=s_count).pack(anchor='w')
tk.Checkbutton(root, text='efficiency data', variable=s_efficient).pack(anchor='w')
tk.Checkbutton(root, text='position data', variable=s_position).pack(anchor='w')

tk.Button(root, text="Apply", command=check).pack()

root.mainloop()