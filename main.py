import os
import sqlite3

from tkinter import Tk, Frame, Label, Entry, Button, Spinbox
from tkinter.ttk import Treeview
from tkcalendar import DateEntry

FILE_DATABASE=os.path.join(os.path.dirname(__file__), "data.db")

class ThongTinMuonPhong:
    def __init__(self,ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,trangthai="Đã đăng ký",vitri=None,id=None):
        self.id = id
        self.vitri = vitri
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

    stt=1
    for dong in DSdangmuon:
        thoigian=dong.ngay+" " +dong.giobd+" - "+dong.giokt
        bang.insert("","end",values=(stt,dong.hoten,dong.mssv,dong.lop,dong.sdt,thoigian,dong.soluong,dong.trangthai))
        stt+=1

# def sua():
#     # Đang phát triển
#     return

def xoa():
    # Đang phát triển
    return

def huy():
    # Đang phát triển
    return

def khi_chon_dong(event):
    item = bang.selection()

    if not item:
        return

    item = item[0]

    danh_sach_item = bang.get_children()
    vi_tri = danh_sach_item.index(item)

    ttm = DSdangmuon[vi_tri]

    entryHoTen.delete(0, "end")
    entryHoTen.insert(0, ttm.hoten)

    entryMSSV.delete(0, "end")
    entryMSSV.insert(0, ttm.mssv)

    entryLop.delete(0, "end")
    entryLop.insert(0, ttm.lop)

    entrySDT.delete(0, "end")
    entrySDT.insert(0, ttm.sdt)

    entrySoLuong.delete(0, "end")
    entrySoLuong.insert(0, ttm.soluong)

    dateEntry.set_date(ttm.ngay)

    giobd, phutbd = ttm.giobd.split(":")
    giokt, phutkt = ttm.giokt.split(":")

    spinGioBD.delete(0, "end")
    spinGioBD.insert(0, giobd)

    spinPhutBD.delete(0, "end")
    spinPhutBD.insert(0, phutbd)

    spinGioKT.delete(0, "end")
    spinGioKT.insert(0, giokt)

    spinPhutKT.delete(0, "end")
    spinPhutKT.insert(0, phutkt)

def luu_database(DSdangmuon):
    conn = sqlite3.connect(FILE_DATABASE)
    cursor=conn.cursor()

    for ttmp in DSdangmuon:
        if ttmp.id==None:
            cursor.execute("""
                INSERT INTO thongtinmuonphong
                (ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,trangthai)
                VALUES (?,?,?,?,?,?,?,?,?)
            """,(ttmp.ngay,ttmp.hoten,ttmp.mssv,ttmp.lop,ttmp.sdt,ttmp.giobd,ttmp.giokt,ttmp.soluong,ttmp.trangthai))
        else:
            cursor.execute("""
                UPDATE thongtinmuonphong
                SET ngay=?,hoten=?,mssv=?,lop=?,sdt=?,giobd=?,giokt=?,soluong=?,trangthai=?
                WHERE id=?
            """,(ttmp.ngay,ttmp.hoten,ttmp.mssv,ttmp.lop,ttmp.sdt,ttmp.giobd,ttmp.giokt,ttmp.soluong,ttmp.trangthai,ttmp.id))

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
    vt=0
    for pt in duLieu:
        tmp=ThongTinMuonPhong(pt[0],pt[1],pt[2],pt[3],pt[4],pt[5],pt[6],pt[7],pt[8],vt,pt[9])
        ds.append(tmp)
        vt+=1
    
    conn.close()
    return ds

def main():
    # DSdangmuondaluu=doc_database()
    co_thay_doi=0
    DSdangmuon=doc_database()
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

    spinGioBD = Spinbox(khungNhapGio,from_=0,to=23,width=3,format="%02.0f")
    spinGioBD.grid(row=0, column=1, sticky="w")

    lblHaiChamBD = Label(khungNhapGio, text=":")
    lblHaiChamBD.grid(row=0, column=2)

    spinPhutBD = Spinbox(khungNhapGio,from_=0,to=59,width=3,format="%02.0f")
    spinPhutBD.grid(row=0, column=3, sticky="w")

    lblGioKT = Label(khungNhapGio, text="Kết thúc:")
    lblGioKT.grid(row=1, column=0, sticky="w")

    spinGioKT = Spinbox(khungNhapGio,from_=8,to=20,width=3,format="%02.0f")
    spinGioKT.grid(row=1, column=1, sticky="w")

    lblHaiChamKT = Label(khungNhapGio, text=":")
    lblHaiChamKT.grid(row=1, column=2)

    spinPhutKT = Spinbox(khungNhapGio,from_=0,to=59,width=3,format="%02.0f")
    spinPhutKT.grid(row=1, column=3, sticky="w")

    lblDanhSach=Label(khungHienThi,text="DANH SÁCH MƯỢN PHÒNG")
    lblDanhSach.grid(row=0,column=0)

    bang = Treeview(khungHienThi,columns=("stt","hoten","mssv","lop","sdt","thoigian","soluong","trangthai"),show="headings")

    bang.heading("stt", text="STT")
    bang.heading("hoten", text="Họ và tên")
    bang.heading("mssv", text="MSSV")
    bang.heading("lop", text="Lớp")
    bang.heading("sdt", text="SĐT")
    bang.heading("thoigian",text="Thời gian")
    bang.heading("soluong", text="Số lượng")
    bang.heading("trangthai", text="Trạng thái")

    bang.grid(row=1,column=0,sticky="nsew")

    hien_thi(DSdangmuon,bang)

    def lay_du_lieu_tu_form():
        hoten=entryHoTen.get()
        mssv=entryMSSV.get()
        lop=entryLop.get()
        sdt=entrySDT.get()
        ngay=dateNgay.get()
        giobd=spinGioBD.get()+":"+spinPhutBD.get()
        giokt=spinGioKT.get()+":"+spinPhutKT.get()
        soluong=entrySoLuong.get()
        dulieu=ThongTinMuonPhong(ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong)
        return dulieu

    def them():
        dlform=lay_du_lieu_tu_form()
        # hoten=entryHoTen.get()
        # mssv=entryMSSV.get()
        # lop=entryLop.get()
        # sdt=entrySDT.get()
        # ngay=dateNgay.get()
        # giobd=spinGioBD.get()+":"+spinPhutBD.get()
        # giokt=spinGioKT.get()+":"+spinPhutKT.get()
        # soluong=entrySoLuong.get()

        # ttmp=ThongTinMuonPhong(ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong)
        DSdangmuon.append(dlform)
        hien_thi(DSdangmuon,bang)
        # ds=DSdangmuondaluu+DSdangmuon
        # hien_thi(ds,bang)
        btnThem.config(state="diable")
        btnLuu.config(state="normal")
        nonlocal co_thay_doi
        co_thay_doi=1
        return

    def hien_nut(event=None):
        nonlocal vi_tri_dang_chon
        dlform=lay_du_lieu_tu_form()
        if kt_trung_lich()==0 and (dlform.hoten and dlform.lop and dlform.mssv and dlform.sdt and dlform.soluong):
            btnThem.config(state="normal")
        else:
            btnThem.config(state="disable")

        if vi_tri_dang_chon!=None:
            btnSua.config(state="normal")
            btnXoa.config(state="normal")
            btnHuy.config(state="normal")
    
    def kt_trung_lich():
        nonlocal vi_tri_dang_chon
        dlform1=lay_du_lieu_tu_form()
        if vi_tri_dang_chon!=None:
            dlform2=DSdangmuon[vi_tri_dang_chon]
            if dlform1.ngay!=dlform2.ngay or dlform1.giobd!=dlform2.giobd or dlform1.giokt!=dlform2.giokt:
                return 0 # không trùng lịch
        else:
            for ttmp in DSdangmuon:
                if dlform1.ngay!=ttmp.ngay or dlform1.giobd!=ttmp.giobd or dlform1.giokt!=ttmp.giokt:
                    return 0 # không trùng lịch
        return 1

    def lam_trong_form():
        entryHoTen.delete(0, "end")
        entryMSSV.delete(0, "end")
        entryLop.delete(0, "end")
        entrySDT.delete(0, "end")
        entrySoLuong.delete(0, "end")
        spinGioBD.delete(0, "end")
        spinPhutBD.delete(0, "end")
        spinGioKT.delete(0, "end")
        spinPhutKT.delete(0, "end")

    vi_tri_dang_chon = None
    def khi_chon_dong(event):
        nonlocal vi_tri_dang_chon
        item = bang.selection()

        if not item:
            return

        item = item[0]

        danh_sach_item = bang.get_children()
        vi_tri = danh_sach_item.index(item)

        ttm = DSdangmuon[vi_tri]
        vi_tri_dang_chon = vi_tri

        lam_trong_form()
        # entryHoTen.delete(0, "end")
        entryHoTen.insert(0, ttm.hoten)

        # entryMSSV.delete(0, "end")
        entryMSSV.insert(0, ttm.mssv)

        # entryLop.delete(0, "end")
        entryLop.insert(0, ttm.lop)

        # entrySDT.delete(0, "end")
        entrySDT.insert(0, ttm.sdt)

        # entrySoLuong.delete(0, "end")
        entrySoLuong.insert(0, ttm.soluong)

        dateNgay.set_date(ttm.ngay)

        giobd, phutbd = ttm.giobd.split(":")
        giokt, phutkt = ttm.giokt.split(":")

        # spinGioBD.delete(0, "end")
        spinGioBD.insert(0, giobd)

        # spinPhutBD.delete(0, "end")
        spinPhutBD.insert(0, phutbd)

        # spinGioKT.delete(0, "end")
        spinGioKT.insert(0, giokt)

        # spinPhutKT.delete(0, "end")
        spinPhutKT.insert(0, phutkt)

    bang.bind("<<TreeviewSelect>>", khi_chon_dong)

    def sua():
        nonlocal vi_tri_dang_chon
        if vi_tri_dang_chon == None:
            return

        ttm = DSdangmuon[vi_tri_dang_chon]

        # Lấy dữ liệu mới từ form
        ttm.hoten = entryHoTen.get()
        ttm.mssv = entryMSSV.get()
        ttm.lop = entryLop.get()
        ttm.sdt = entrySDT.get()
        ttm.soluong = entrySoLuong.get()

        ttm.ngay = dateNgay.get()

        ttm.giobd = (
            f"{int(spinGioBD.get()):02d}:"
            f"{int(spinPhutBD.get()):02d}"
        )

        ttm.giokt = (
            f"{int(spinGioKT.get()):02d}:"
            f"{int(spinPhutKT.get()):02d}"
        )

        vi_tri_dang_chon=None
        lam_trong_form()
        # Hiển thị lại Treeview
        hien_thi(DSdangmuon,bang)
        hien_nut()
        btnLuu.config(state="normal")
        nonlocal co_thay_doi
        co_thay_doi=1
    
    entryHoTen.bind("<KeyRelease>", hien_nut)
    entryLop.bind("<KeyRelease>", hien_nut)
    entryMSSV.bind("<KeyRelease>", hien_nut)
    entrySDT.bind("<KeyRelease>", hien_nut)
    entrySoLuong.bind("<KeyRelease>", hien_nut)

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

    btnThem.config(state="disable")
    btnSua.config(state="disable")
    btnXoa.config(state="disable")
    btnHuy.config(state="disable")
    btnLuu.config(state="disable")

    lblThongKe=Label(root,text="TUẦN NÀY: 0 LƯỢT ĐĂNG KÝ | 0 NGƯỜI")
    lblThongKe.grid(row=4,column=0)

    root.mainloop()

if __name__=="__main__":
    tao_database()
    main()