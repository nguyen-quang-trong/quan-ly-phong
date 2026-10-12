import os
import sqlite3
from datetime import *

from tkinter import Tk, Frame, Label, Entry, Button, Spinbox
from tkinter.ttk import Treeview
from tkcalendar import DateEntry

FILE_DATABASE=os.path.join(os.path.dirname(__file__), "data.db")

class thong_tin_muon_phong:
    def __init__(self,ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,vitritrongds,trangthai="Đã đăng ký",id=None):
        self.id = id
        self.vitritrongds = vitritrongds
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
        CREATE TABLE IF NOT EXISTS thong_tin_muon_phong(
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
    return

def luu_database(DSdangmuon):
    conn = sqlite3.connect(FILE_DATABASE)
    cursor=conn.cursor()

    for ttmp in DSdangmuon:
        if ttmp.id==None:
            cursor.execute("""
                INSERT INTO thong_tin_muon_phong
                (ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,trangthai)
                VALUES (?,?,?,?,?,?,?,?,?)
            """,(ttmp.ngay,ttmp.hoten,ttmp.mssv,ttmp.lop,ttmp.sdt,ttmp.giobd,ttmp.giokt,ttmp.soluong,ttmp.trangthai))
        else:
            cursor.execute("""
                UPDATE thong_tin_muon_phong
                SET ngay=?,hoten=?,mssv=?,lop=?,sdt=?,giobd=?,giokt=?,soluong=?,trangthai=?
                WHERE id=?
            """,(ttmp.ngay,ttmp.hoten,ttmp.mssv,ttmp.lop,ttmp.sdt,ttmp.giobd,ttmp.giokt,ttmp.soluong,ttmp.trangthai,ttmp.id))

    conn.commit()
    conn.close()
    return

def doc_database():
    conn = sqlite3.connect(FILE_DATABASE)
    cursor=conn.cursor()
    cursor.execute("""
        SELECT ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,trangthai,id
        FROM thong_tin_muon_phong
    """)

    duLieu=cursor.fetchall()
    ds=[]
    vt=0
    for pt in duLieu:
        tmp=thong_tin_muon_phong(pt[0],pt[1],pt[2],pt[3],pt[4],pt[5],pt[6],pt[7],pt[8],vt,pt[9])
        ds.append(tmp)
        vt+=1
    
    conn.close()
    return ds

def hien_thi(DSdangmuon,treeview_bang):
    for item in treeview_bang.get_children():
        treeview_bang.delete(item)

    stt=1
    for dong in DSdangmuon:
        thoigian=dong.ngay+" " +dong.giobd+" - "+dong.giokt
        treeview_bang.insert("","end",values=(stt,dong.hoten,dong.mssv,dong.lop,dong.sdt,thoigian,dong.soluong,dong.trangthai))
        stt+=1

def sap_xep(DSdangmuon):
    for i in range(len(DSdangmuon)-1):
        for j in range(i+1,len(DSdangmuon)):
            n1= datetime.strptime(DSdangmuon[i].ngay, "%d/%m/%Y").date()
            n2= datetime.strptime(DSdangmuon[j].ngay, "%d/%m/%Y").date()
            if n1>n2:
                DSdangmuon[i],DSdangmuon[j]=DSdangmuon[j],DSdangmuon[i]
                DSdangmuon[i].vitri,DSdangmuon[j].vitri=DSdangmuon[j].vitri,DSdangmuon[i].vitri
            elif n1==n2:
                gbd,pbd=DSdangmuon[i].giobd.split(":")
                gkt,pkt=DSdangmuon[i].giokt.split(":")
                gbd=int(gbd)*60+int(pbd)
                gkt=int(gkt)*60+int(pkt)
                gbd2,pbd2=DSdangmuon[j].giobd.split(":")
                gkt2,pkt2=DSdangmuon[j].giokt.split(":")
                gbd2=int(gbd2)*60+int(pbd2)
                gkt2=int(gkt2)*60+int(pkt2)
                if gbd>gbd2:
                    DSdangmuon[i],DSdangmuon[j]=DSdangmuon[j],DSdangmuon[i]
                    DSdangmuon[i].vitri,DSdangmuon[j].vitri=DSdangmuon[j].vitri,DSdangmuon[i].vitri

def main():
    # co_thay_doi=0
    DSdangmuon=doc_database()
    sap_xep(DSdangmuon)
    root=Tk()
    root.title('QUẢN LÝ PHÒNG')

    root.rowconfigure(3, weight=1)
    root.columnconfigure(0, weight=1)

    frame_nhap=Frame(root)
    frame_nhap.grid(row=1,column=0)
    frame_nhapGio=Frame(frame_nhap)
    frame_nhapGio.grid(row=6,column=0,columnspan=2,sticky="w")
    frame_nut=Frame(root)
    frame_nut.grid(row=2,column=0)
    frame_hienthids=Frame(root)
    frame_hienthids.grid(row=3,column=0,sticky="nsew")
    frame_hienthids.rowconfigure(1, weight=1)
    frame_hienthids.columnconfigure(0, weight=1)

    label_hoten = Label(frame_nhap, text="Họ và tên:")
    label_hoten.grid(row=0, column=0, sticky="w")
    entry_hoten = Entry(frame_nhap, width=30)
    entry_hoten.grid(row=0, column=1)
    entry_hoten.focus_set()

    label_mssv = Label(frame_nhap, text="MSSV:")
    label_mssv.grid(row=1, column=0, sticky="w")
    entry_mssv = Entry(frame_nhap, width=30)
    entry_mssv.grid(row=1, column=1)

    label_lop = Label(frame_nhap, text="Lớp:")
    label_lop.grid(row=2, column=0, sticky="w")
    entry_lop = Entry(frame_nhap, width=30)
    entry_lop.grid(row=2, column=1)

    label_sdt = Label(frame_nhap, text="SĐT:")
    label_sdt.grid(row=3, column=0, sticky="w")
    entry_sdt = Entry(frame_nhap, width=30)
    entry_sdt.grid(row=3, column=1)

    label_soluong = Label(frame_nhap, text="Số lượng:")
    label_soluong.grid(row=4, column=0, sticky="w")
    entry_soluong = Entry(frame_nhap, width=30)
    entry_soluong.grid(row=4, column=1)

    label_ngay = Label(frame_nhap, text="Ngày:")
    label_ngay.grid(row=5, column=0, sticky="w")
    dateentry_ngay = DateEntry(frame_nhap,width=12,date_pattern="dd/mm/yyyy")
    dateentry_ngay.grid(row=5, column=1, sticky="w")
    dateentry_ngay.delete(0, "end")

    label_danhsach=Label(frame_hienthids,text="DANH SÁCH MƯỢN PHÒNG")
    label_danhsach.grid(row=0,column=0)

    treeview_bang = Treeview(frame_hienthids,columns=("stt","hoten","mssv","lop","sdt","thoigian","soluong","trangthai"),show="headings")

    treeview_bang.heading("stt", text="STT")
    treeview_bang.heading("hoten", text="Họ và tên")
    treeview_bang.heading("mssv", text="MSSV")
    treeview_bang.heading("lop", text="Lớp")
    treeview_bang.heading("sdt", text="SĐT")
    treeview_bang.heading("thoigian",text="Thời gian")
    treeview_bang.heading("soluong", text="Số lượng")
    treeview_bang.heading("trangthai", text="Trạng thái")

    treeview_bang.grid(row=1,column=0,sticky="nsew")
    hien_thi(DSdangmuon,treeview_bang)

    # def lay_du_lieu_tu_form():
    #     hoten=entry_hoten.get()
    #     mssv=entry_mssv.get()
    #     lop=entry_lop.get()
    #     sdt=entry_sdt.get()
    #     ngay=dateentry_ngay.get()
    #     giobd=spin_giobd.get()+":"+spin_phutbd.get()
    #     giokt=spin_giokt.get()+":"+spin_phutkt.get()
    #     soluong=entry_soluong.get()
    #     dulieu=thong_tin_muon_phong(ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong)
    #     return dulieu

    def button_them_click():
        # dlform=lay_du_lieu_tu_form()
        giobd=spin_giobd.get()+":"+spin_phutbd.get()
        giokt=spin_giokt.get()+":"+spin_phutkt.get()
        vt=len(DSdangmuon) # xác định vị trí trong danh sách cho phần tử
        dlform=thong_tin_muon_phong(dateentry_ngay.get(),entry_hoten.get(),entry_mssv.get(),entry_lop.get(),entry_sdt.get(),giobd,giokt,entry_soluong.get(),vt)
        DSdangmuon.append(dlform)
        sap_xep(DSdangmuon)
        hien_thi(DSdangmuon,treeview_bang)
        button_them.config(state="disable")
        button_luu.config(state="normal")
        return

    def hien_nut(event=None):
        nonlocal vi_tri_dang_chon
        # dlform1=lay_du_lieu_tu_form()
        
        if (kt_trung_lich(0)==0) and (entry_hoten.get() and entry_mssv.get() and entry_lop.get() and entry_sdt.get() and entry_soluong.get()):
            button_them.config(state="normal")
        else:
            button_them.config(state="disable")
            
        if vi_tri_dang_chon!=None:
            if kt_trung_lich(1)==0:
                button_sua.config(state="normal")
            else:
                button_sua.config(state="disable")
        button_huy.config(state="normal")
        return
    
    def kt_trung_lich(dang_sua):
        nonlocal vi_tri_dang_chon
        dlform1=lay_du_lieu_tu_form()
        gbd,pbd=dlform1.giobd.split(":")
        gkt,pkt=dlform1.giokt.split(":")
        gbd=int(gbd)*60+int(pbd)
        gkt=int(gkt)*60+int(pkt)
        if gbd>=gkt:
            return 1

        for ttmp in DSdangmuon:
            gbd2,pbd2=ttmp.giobd.split(":")
            gkt2,pkt2=ttmp.giokt.split(":")
            gbd2=int(gbd2)*60+int(pbd2)
            gkt2=int(gkt2)*60+int(pkt2)
            if(dang_sua==1):
                if int(vi_tri_dang_chon)==int(ttmp.vitri):
                    continue
            if dlform1.ngay==ttmp.ngay:
                if gbd<gkt2 and gbd2<gkt:
                    return 1

        return 0 # không có trùng lịch

    def button_huy_click():
        nonlocal vi_tri_dang_chon
        entry_hoten.delete(0, "end")
        entry_mssv.delete(0, "end")
        entry_lop.delete(0, "end")
        entry_sdt.delete(0, "end")
        entry_soluong.delete(0, "end")
        dateentry_ngay.delete(0, "end")
        spin_giobd.delete(0, "end")
        spin_phutbd.delete(0, "end")
        spin_giokt.delete(0, "end")
        spin_phutkt.delete(0, "end")
        
        button_them.config(state="disable")
        button_sua.config(state="disable")
        button_huy.config(state="disable")
        vi_tri_dang_chon=None
        entry_hoten.focus_set()

    vi_tri_dang_chon = None
    def khi_chon_dong(event):
        nonlocal vi_tri_dang_chon
        item = treeview_bang.selection()

        if not item:
            return

        item = item[0]

        danh_sach_item = treeview_bang.get_children()
        vi_tri = danh_sach_item.index(item)

        ttm = DSdangmuon[vi_tri]
        button_huy_click()
        vi_tri_dang_chon = vi_tri

        # entry_hoten.delete(0, "end")
        entry_hoten.insert(0, ttm.hoten)

        # entry_mssv.delete(0, "end")
        entry_mssv.insert(0, ttm.mssv)

        # entry_lop.delete(0, "end")
        entry_lop.insert(0, ttm.lop)

        # entry_sdt.delete(0, "end")
        entry_sdt.insert(0, ttm.sdt)

        # entry_soluong.delete(0, "end")
        entry_soluong.insert(0, ttm.soluong)

        dateentry_ngay.set_date(ttm.ngay)

        giobd, phutbd = ttm.giobd.split(":")
        giokt, phutkt = ttm.giokt.split(":")

        # spin_giobd.delete(0, "end")
        spin_giobd.insert(0, giobd)

        # spin_phutbd.delete(0, "end")
        spin_phutbd.insert(0, phutbd)

        # spin_giokt.delete(0, "end")
        spin_giokt.insert(0, giokt)

        # spin_phutkt.delete(0, "end")
        spin_phutkt.insert(0, phutkt)

    treeview_bang.bind("<<TreeviewSelect>>", khi_chon_dong)

    def button_sua_click():
        nonlocal vi_tri_dang_chon
        if vi_tri_dang_chon == None:
            return

        ttm = DSdangmuon[vi_tri_dang_chon]

        # Lấy dữ liệu mới từ form
        ttm.hoten = entry_hoten.get()
        ttm.mssv = entry_mssv.get()
        ttm.lop = entry_lop.get()
        ttm.sdt = entry_sdt.get()
        ttm.soluong = entry_soluong.get()

        ttm.ngay = dateentry_ngay.get()

        ttm.giobd = (
            f"{int(spin_giobd.get()):02d}:"
            f"{int(spin_phutbd.get()):02d}"
        )

        ttm.giokt = (
            f"{int(spin_giokt.get()):02d}:"
            f"{int(spin_phutkt.get()):02d}"
        )
        
        DSdangmuon[vi_tri_dang_chon]=ttm
        # Hiển thị lại Treeview
        sap_xep(DSdangmuon)
        hien_thi(DSdangmuon,treeview_bang)
        hien_nut()
        button_luu.config(state="normal")
        button_huy_click()
        vi_tri_dang_chon=None

    def button_luu_click():
        luu_database(DSdangmuon)
        button_luu.config(state="disable")
    
    entry_hoten.bind("<KeyRelease>", hien_nut)
    entry_lop.bind("<KeyRelease>", hien_nut)
    entry_mssv.bind("<KeyRelease>", hien_nut)
    entry_sdt.bind("<KeyRelease>", hien_nut)
    entry_soluong.bind("<KeyRelease>", hien_nut)
    dateentry_ngay.bind("<<DateEntrySelected>>",hien_nut)

    lblGioBD = Label(frame_nhapGio, text="Bắt đầu:",width=8)
    lblGioBD.grid(row=0, column=0, sticky="w")
    spin_giobd = Spinbox(frame_nhapGio,from_=8,to=20,width=3,format="%02.0f",command=hien_nut)
    spin_giobd.grid(row=0, column=1, sticky="w")
    spin_giobd.delete(0, "end")
    lblHaiChamBD = Label(frame_nhapGio, text=":")
    lblHaiChamBD.grid(row=0, column=2)
    spin_phutbd = Spinbox(frame_nhapGio,from_=0,to=59,width=3,format="%02.0f",command=hien_nut)
    spin_phutbd.grid(row=0, column=3, sticky="w")
    spin_phutbd.delete(0, "end")

    lblGioKT = Label(frame_nhapGio, text="Kết thúc:")
    lblGioKT.grid(row=1, column=0, sticky="w")
    spin_giokt = Spinbox(frame_nhapGio,from_=8,to=20,width=3,format="%02.0f",command=hien_nut)
    spin_giokt.grid(row=1, column=1, sticky="w")
    spin_giokt.delete(0, "end")
    lblHaiChamKT = Label(frame_nhapGio, text=":")
    lblHaiChamKT.grid(row=1, column=2)
    spin_phutkt = Spinbox(frame_nhapGio,from_=0,to=59,width=3,format="%02.0f",command=hien_nut)
    spin_phutkt.grid(row=1, column=3, sticky="w")
    spin_phutkt.delete(0, "end")

    button_them = Button(frame_nut, text="Thêm", command=button_them_click)
    button_them.grid(row=0, column=0)

    button_sua = Button(frame_nut, text="Sửa", command=button_sua_click)
    button_sua.grid(row=0, column=1)

    button_huy = Button(frame_nut, text="Hủy", command=button_huy_click)
    button_huy.grid(row=0, column=3)

    button_luu = Button(frame_nut, text="Lưu", command=button_luu_click)
    button_luu.grid(row=0, column=4)

    button_them.config(state="disable")
    button_sua.config(state="disable")
    button_huy.config(state="disable")
    button_luu.config(state="disable")

    lblThongKe=Label(root,text="TUẦN NÀY: 0 LƯỢT ĐĂNG KÝ | 0 NGƯỜI")
    lblThongKe.grid(row=4,column=0)

    root.mainloop()

if __name__=="__main__":
    tao_database()
    main()