import tkinter as tk

root = tk.Tk()
root.title('Test window')
tk.Label(root, text='Seleccione su modo').grid(row=0, column=0, columnspan=2)

btn_server = tk.Button(root, text='Servidor')
btn_server.grid(row=1, column=0)
btn_client = tk.Button(root, text='Cliente')
btn_client.grid(row=1, column=1)




root.geometry('600x600')
root.mainloop()
