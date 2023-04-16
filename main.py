#kütüphaneler
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import colorchooser
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
from datetime import datetime

#global veriler
border = 2
box_size = 50
fill_color = '#000000'
back_color = '#ffffff'
filename = ''

#fonksiyonlar
def fg_choose():
    global fill_color
    color_code = colorchooser.askcolor(title ="Ön plan rengi seç")
    fill_color = color_code[1]
    fg_button.configure(bg=fill_color)

def bg_choose():
    global back_color
    color_code = colorchooser.askcolor(title ="Arka plan rengi seç")
    back_color = color_code[1]
    bg_button.configure(bg=back_color)

def qr_olustur():
    global border, box_size, fill_color, back_color
    if data_entry.get() == '':
        print('Lütfen içerik ekleyin..')
    else:
        if box_entry.get() != '':
            box_size = box_entry.get()
        if border_entry.get() != '':
            border = border_entry.get()

        code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=50, border=2)
        code.add_data(data_entry.get())

        an = datetime.now()
        tarih = datetime.strftime(an, '%X').replace(':','-')
        code.make_image(fill_color=fill_color, back_color=back_color).save(f'qr_{tarih}.png')
        print('QR Kod oluşturuldu.')
    

def dosya_sec():
    global filename
    filename = filedialog.askopenfilename(title='QR Kod', filetypes=(('image files', '*.png'),('All files', '*.*')))
    path_label['text'] = filename.split('/')[-1]

def delete_msg():
    result_text['state'] = 'normal'
    result_text.delete('1.0', 'end')
    result_text['state'] = 'disabled'

def qr_oku():
    if filename != '':
        text = ''
        for i in decode(Image.open(filename)):
            text += str(i.data)[2:-1]
        result_text['state'] = 'normal'
        result_text.insert('1.0',text)
        result_text['state'] = 'disabled'

#genel ayarlar
app = Tk()
app.iconbitmap('icon.ico')
app.geometry('250x210')
app.resizable(0,0)
app.title('QR Kod Oluştur ve Oku')

#frames
tabControl = ttk.Notebook(app)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='QR Oluşturma')
tabControl.add(tab2, text='QR Okuma')
tabControl.place(x=0,y=0,height=210,width=250)

#tab1
border_label = ttk.Label(tab1, text='Kenar kalınlığı :')
border_label.place(x=20, y=5, height=20, width=100)
border_entry = Entry(tab1)
border_entry.place(x=130, y=5, height=20, width=20)
ttk.Label(tab1, text='px').place(x=150, y=5, height=20)
ttk.Label(tab1, text='(ÖR: 3)', foreground='gray').place(x=170, y=5, height=20)
box_label = ttk.Label(tab1, text='Kutu boyutu :')
box_label.place(x=20, y=35, height=20, width=100)
box_entry = Entry(tab1)
box_entry.place(x=130, y=35, height=20, width=20)
ttk.Label(tab1, text='px').place(x=150, y=35, height=20)
ttk.Label(tab1, text='(ÖR: 50)', foreground='gray').place(x=170, y=35, height=20)
fg_label = ttk.Label(tab1, text='Ön plan rengi :')
fg_label.place(x=20, y=65, height=20, width=100)
fg_button = Button(tab1, bg=fill_color, command=fg_choose)
fg_button.place(x=130, y=65, height=20, width=20)
bg_label = ttk.Label(tab1, text='Arka plan rengi :')
bg_label.place(x=20, y=95, height=20, width=100)
bg_button = Button(tab1, bg=back_color, command=bg_choose)
bg_button.place(x=130, y=95, height=20, width=20)
data_label = ttk.Label(tab1, text='İçerik :')
data_label.place(x=20, y=125, height=20, width=100)
data_entry = Entry(tab1)
data_entry.place(x=130, y=125, height=20, width=80)
photo = PhotoImage(file = r"create_button.png")
create_button = Button(tab1, image = photo, borderwidth=0, command=qr_olustur)
create_button.place(x=50, y=155, height=25, width=150)


#tab2
select_button = Button(tab2, text='Dosya Seç', command=dosya_sec)
select_button.place(x=20, y=0, height=20, width=80)
path_label = ttk.Label(tab2)
path_label.place(x=110, y=0, height=20, width=120)
read_button = Button(tab2, text='QR Kodu Oku', command=qr_oku)
read_button.place(x=20, y=30, height=20, width=80)
result_text = Text(tab2, state='disabled')
result_text.place(x=20, y=60, height=80, width=210)
delete_button = Button(tab2, text='mesajı temizle', command=delete_msg)
delete_button.place(x=130, y=150, height=20, width=100)

app.mainloop()
