import sqlite3
from tkinter import *
from tkinter.ttk import *
from datetime import datetime

conn=sqlite3.connect("data.db")
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS thongtinmuonphong(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hoten TEXT NOT NULL,
        mssv TEXT NOT NULL,
        thoigianbd TEXT,
        thoigiankt TEXT,
        trangthai TEXT
    )
""")

root=Tk()
root.title('QUẢN LÝ PHÒNG')

lblHoTen=Label(root,text="Họ và tên:")
lblHoTen.grid(row=0,column=0)
entryHoTen=Entry(root)
entryHoTen.grid(row=0,column=1)

lblMSSV=Label(root,text="MSSV:")
lblMSSV.grid(row=1,column=0)
entryMSSV=Entry(root)
entryMSSV.grid(row=1,column=1)

ngay=[f"{i:02}" for i in range(1,32)]
thang=[f"{i:02}" for i in range(1,13)]
nam=list(range(datetime.now().year,datetime.now().year+5))
gio=[f"{i:02}" for i in range(7,21)]
phut=[f"{i:02}" for i in range(60)]

lblNgay=Label(root,text="Ngày:")
lblNgay.grid(row=2,column=0)
comboNgay=Combobox(root,values=ngay,width=3,state="readonly")
comboNgay.grid(row=2,column=1)
comboThang=Combobox(root,values=thang,width=3,state="readonly")
comboThang.grid(row=2,column=2)
comboNam=Combobox(root,values=nam,width=5,state="readonly")
comboNam.grid(row=2,column=3)

lblThoiGianBD=Label(root,text="Bắt đầu:")
lblThoiGianBD.grid(row=3,column=0)
comboGioBD=Combobox(root,values=gio,width=3,state="readonly")
comboGioBD.grid(row=3,column=1)
comboPhutBD=Combobox(root,values=phut,width=3,state="readonly")
comboPhutBD.grid(row=3,column=2)

lblThoiGianKT=Label(root,text="Kết thúc:")
lblThoiGianKT.grid(row=4,column=0)
comboGioKT=Combobox(root,values=gio,width=3,state="readonly")
comboGioKT.grid(row=4,column=1)
comboPhutKT=Combobox(root,values=phut,width=3,state="readonly")
comboPhutKT.grid(row=4,column=2)

btnLuu=Button(root,text="Lưu")
btnLuu.grid(row=5,column=0)

lblDanhSach=Label(root,text="DANH SÁCH MƯỢN PHÒNG")
lblDanhSach.grid(row=6,column=0,columnspan=5)
lblSTT=Label(root,text="STT")
lblSTT.grid(row=7,column=0)
lblHoTenDS=Label(root,text="Họ và tên")
lblHoTenDS.grid(row=7,column=1)
lblMSSVDS=Label(root,text="MSSV")
lblMSSVDS.grid(row=7,column=2)
lblThoiGianBDDS=Label(root,text="Bắt đầu")
lblThoiGianBDDS.grid(row=7,column=3)
lblThoiGianKTDS=Label(root,text="Kết thúc")
lblThoiGianKTDS.grid(row=7,column=4)
lblTrangThaiDS=Label(root,text="Trạng thái")
lblTrangThaiDS.grid(row=7,column=5)

lblThongKe=Label(root,text="TUẦN NÀY: 0 LƯỢT ĐĂNG KÝ | 0 NGƯỜI")
lblThongKe.grid(row=8,column=0,columnspan=6)

root.mainloop()