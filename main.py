import os
import sqlite3

from tkinter import Tk, Frame, Label, Entry, Button, Spinbox
from tkinter.ttk import Treeview
from tkcalendar import DateEntry

FILE_DATABASE=os.path.join(os.path.dirname(__file__), "data.db")

class ThongTinMuonPhong:
    def __init__(self,ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,trangthai="Đã đăng ký",id=None):
        self.id = id
        self.ngay = ngay
        self.hoten = hoten
        self.mssv = mssv
        self.lop = lop
        self.sdt = sdt
        self.giobd = giobd
        self.giokt = giokt
        self.soluong = soluong
        self.trangthai = trangthai

def tao_database():
    conn = sqlite3.connect(FILE_DATABASE)
    cursor=conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thongtinmuonphong(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ngay TEXT NOT NULL,
            hoten TEXT NOT NULL,
            mssv TEXT NOT NULL,
            lop TEXT NOT NULL,
            sdt TEXT NOT NULL,
            giobd TEXT NOT NULL,
            giokt TEXT NOT NULL,
            soluong INTEGER NOT NULL,
            trangthai TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def hien_thi(DSdangmuon,bang):
    for item in bang.get_children():
        bang.delete(item)

    for dong in DSdangmuon:
        thoigian=dong.ngay+" " +dong.giobd+" - "+dong.giokt
        bang.insert("","end",values=(dong.id,dong.hoten,dong.mssv,dong.lop,dong.sdt,thoigian,dong.soluong,dong.trangthai))

def sua():
    # Đang phát triển
    return

def xoa():
    # Đang phát triển
    return

def huy():
    # Đang phát triển
    return

def luu_database(DSdangmuon):
    conn = sqlite3.connect(FILE_DATABASE)
    cursor=conn.cursor()

    for ttmp in DSdangmuon:
        cursor.execute("""
            INSERT INTO thongtinmuonphong
            (ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,trangthai)
            VALUES (?,?,?,?,?,?,?,?,?)
        """,(ttmp.ngay,ttmp.hoten,ttmp.mssv,ttmp.lop,ttmp.sdt,ttmp.giobd,ttmp.giokt,ttmp.soluong,ttmp.trangthai))

    print("Luu thanh cong")
    conn.commit()
    conn.close()
    return

def doc_database():
    conn = sqlite3.connect(FILE_DATABASE)
    cursor=conn.cursor()
    cursor.execute("""
        SELECT ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,trangthai,id
        FROM thongtinmuonphong
    """)

    duLieu=cursor.fetchall()
    ds=[]
    
    for pt in duLieu:
        tmp=ThongTinMuonPhong(pt[0],pt[1],pt[2],pt[3],pt[4],pt[5],pt[6],pt[7],pt[8],pt[9])
        ds.append(tmp)
    
    conn.close()
    return ds

def main():
    DSdangmuondaluu=doc_database()
    DSdangmuon=[]
    root=Tk()
    root.title('QUẢN LÝ PHÒNG')

    root.rowconfigure(3, weight=1)
    root.columnconfigure(0, weight=1)

    khungNhap=Frame(root)
    khungNhap.grid(row=1,column=0)
    khungNhapGio=Frame(khungNhap)
    khungNhapGio.grid(row=6,column=0,columnspan=2,sticky="w")
    khungNut=Frame(root)
    khungNut.grid(row=2,column=0)
    khungHienThi=Frame(root)
    khungHienThi.grid(row=3,column=0,sticky="nsew")
    khungHienThi.rowconfigure(1, weight=1)
    khungHienThi.columnconfigure(0, weight=1)

    lblHoTen = Label(khungNhap, text="Họ và tên:")
    lblHoTen.grid(row=0, column=0, sticky="w")

    entryHoTen = Entry(khungNhap, width=30)
    entryHoTen.grid(row=0, column=1)


    lblMSSV = Label(khungNhap, text="MSSV:")
    lblMSSV.grid(row=1, column=0, sticky="w")

    entryMSSV = Entry(khungNhap, width=30)
    entryMSSV.grid(row=1, column=1)


    lblLop = Label(khungNhap, text="Lớp:")
    lblLop.grid(row=2, column=0, sticky="w")

    entryLop = Entry(khungNhap, width=30)
    entryLop.grid(row=2, column=1)


    lblSDT = Label(khungNhap, text="SĐT:")
    lblSDT.grid(row=3, column=0, sticky="w")

    entrySDT = Entry(khungNhap, width=30)
    entrySDT.grid(row=3, column=1)

    lblSoLuong = Label(khungNhap, text="Số lượng:")
    lblSoLuong.grid(row=4, column=0, sticky="w")

    entrySoLuong = Entry(khungNhap, width=30)
    entrySoLuong.grid(row=4, column=1)

    lblNgay = Label(khungNhap, text="Ngày:")
    lblNgay.grid(row=5, column=0, sticky="w")

    dateNgay = DateEntry(khungNhap,width=12,date_pattern="dd/mm/yyyy")
    dateNgay.grid(row=5, column=1, sticky="w")

    lblGioBD = Label(khungNhapGio, text="Bắt đầu:",width=8)
    lblGioBD.grid(row=0, column=0, sticky="w")

    spinGioBD = Spinbox(
        khungNhapGio,
        from_=0,
        to=23,
        width=3,
        format="%02.0f"
    )
    spinGioBD.grid(row=0, column=1, sticky="w")

    lblHaiChamBD = Label(khungNhapGio, text=":")
    lblHaiChamBD.grid(row=0, column=2)

    spinPhutBD = Spinbox(
        khungNhapGio,
        from_=0,
        to=59,
        width=3,
        format="%02.0f"
    )
    spinPhutBD.grid(row=0, column=3, sticky="w")

    lblGioKT = Label(khungNhapGio, text="Kết thúc:")
    lblGioKT.grid(row=1, column=0, sticky="w")

    spinGioKT = Spinbox(
        khungNhapGio,
        from_=8,
        to=20,
        width=3,
        format="%02.0f"
    )
    spinGioKT.grid(row=1, column=1, sticky="w")

    lblHaiChamKT = Label(khungNhapGio, text=":")
    lblHaiChamKT.grid(row=1, column=2)

    spinPhutKT = Spinbox(
        khungNhapGio,
        from_=0,
        to=59,
        width=3,
        format="%02.0f"
    )
    spinPhutKT.grid(row=1, column=3, sticky="w")

    def them():
        hoten=entryHoTen.get()
        mssv=entryMSSV.get()
        lop=entryLop.get()
        sdt=entrySDT.get()
        ngay=dateNgay.get()
        giobd=spinGioBD.get()+":"+spinPhutBD.get()
        giokt=spinGioKT.get()+":"+spinPhutKT.get()
        soluong=entrySoLuong.get()
        ttmp=ThongTinMuonPhong(ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong)
        DSdangmuon.append(ttmp)
        ds=DSdangmuondaluu+DSdangmuon
        hien_thi(ds,bang)
        return

    btnThem = Button(khungNut, text="Thêm", command=them)
    btnThem.grid(row=0, column=0)

    btnSua = Button(khungNut, text="Sửa", command=sua)
    btnSua.grid(row=0, column=1)

    btnXoa = Button(khungNut, text="Xóa", command=xoa)
    btnXoa.grid(row=0, column=2)

    btnHuy = Button(khungNut, text="Hủy", command=huy)
    btnHuy.grid(row=0, column=3)

    btnLuu = Button(khungNut, text="Lưu", command=lambda: luu_database(DSdangmuon))
    btnLuu.grid(row=0, column=4)

    lblDanhSach=Label(khungHienThi,text="DANH SÁCH MƯỢN PHÒNG")
    lblDanhSach.grid(row=0,column=0)

    bang = Treeview(khungHienThi,columns=("id","hoten","mssv","lop","sdt","thoigian","soluong","trangthai"),show="headings")

    bang.heading("id", text="STT")
    bang.heading("hoten", text="Họ và tên")
    bang.heading("mssv", text="MSSV")
    bang.heading("lop", text="Lớp")
    bang.heading("sdt", text="SĐT")
    bang.heading("thoigian",text="Thời gian")
    bang.heading("soluong", text="Số lượng")
    bang.heading("trangthai", text="Trạng thái")

    bang.grid(row=1,column=0,sticky="nsew")

    hien_thi(DSdangmuondaluu,bang)

    lblThongKe=Label(root,text="TUẦN NÀY: 0 LƯỢT ĐĂNG KÝ | 0 NGƯỜI")
    lblThongKe.grid(row=4,column=0)

    root.mainloop()

if __name__=="__main__":
    tao_database()
    main()