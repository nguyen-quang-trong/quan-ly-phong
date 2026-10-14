import os
import sqlite3

from tkinter import Tk, Frame, Label, Entry, Button, Spinbox, LabelFrame, messagebox
from tkinter.ttk import Treeview, Combobox, Scrollbar
from tkcalendar import DateEntry
from datetime import *

FILE_DATABASE=os.path.join(os.path.dirname(__file__), "data.db")

class thong_tin_muon_phong:
    def __init__(self,vitritrongds,ngay,hoten,mssv,lop,sdt,giobd,giokt,soluong,trangthai="Đã đăng ký",id=None):
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
        self.id = id

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

    for ttmp in DSdangmuon:
        cursor=conn.cursor()
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
        tmp=thong_tin_muon_phong(vt,pt[0],pt[1],pt[2],pt[3],pt[4],pt[5],pt[6],pt[7],pt[8],pt[9])
        ds.append(tmp)
        vt+=1
    
    conn.close()
    return ds

def hien_thi(DSdangmuon,treeview_bang):
    for item in treeview_bang.get_children():
        treeview_bang.delete(item)

    stt=1
    for ttmp in DSdangmuon:
        thoigian=ttmp.ngay+" " +ttmp.giobd+" - "+ttmp.giokt
        treeview_bang.insert("","end",values=(stt,ttmp.hoten,ttmp.mssv,ttmp.lop,ttmp.sdt,thoigian,ttmp.soluong,ttmp.trangthai))
        stt+=1
    return

def sap_xep(DSdangmuon):
    for i in range(len(DSdangmuon)-1):
        for j in range(i+1,len(DSdangmuon)):
            n1= datetime.strptime(DSdangmuon[i].ngay, "%d/%m/%Y").date()
            n2= datetime.strptime(DSdangmuon[j].ngay, "%d/%m/%Y").date()
            if n1>n2:
                DSdangmuon[i],DSdangmuon[j]=DSdangmuon[j],DSdangmuon[i]
                DSdangmuon[i].vitritrongds,DSdangmuon[j].vitritrongds=DSdangmuon[j].vitritrongds,DSdangmuon[i].vitritrongds
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
                    DSdangmuon[i].vitritrongds,DSdangmuon[j].vitritrongds=DSdangmuon[j].vitritrongds,DSdangmuon[i].vitritrongds
    return

def main():
    DSdangmuon=doc_database()
    sap_xep(DSdangmuon)
    root=Tk()
    root.title('QUẢN LÝ PHÒNG')

    WIDTH=1000
    HEIGHT=500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - WIDTH) // 2
    y = (screen_height - HEIGHT) // 2

    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}") # căn cửa sổ ở giữa màn hình
    root.resizable(False, False)  # khóa chiều ngang và chiều dọc

    frame_nhap=Frame(root)
    frame_nhap.grid(row=1,column=0)
    frame_nhap_thoigian=Frame(frame_nhap)
    frame_nhap_thoigian.grid(row=0,column=0,sticky="wn")
    frame_nhap_thongtin=Frame(frame_nhap)
    frame_nhap_thongtin.grid(row=0,column=1,sticky="w")
    frame_nhap_trangthai=LabelFrame(frame_nhap,text="Trạng thái")
    frame_nhap_trangthai.grid(row=0,column=2,sticky="wn")
    frame_nut=Frame(root)
    frame_nut.grid(row=2,column=0)
    frame_hienthids=Frame(root)
    frame_hienthids.grid(row=3,column=0,sticky="nsew")
    frame_hienthids.rowconfigure(1, weight=1)
    frame_hienthids.columnconfigure(0, weight=1)
    frame_locds=Frame(frame_hienthids)
    frame_locds.grid(row=1,column=0,sticky="w")

    label_hoten = Label(frame_nhap_thongtin, text="Họ và tên:")
    label_hoten.grid(row=0, column=0, sticky="w")
    entry_hoten = Entry(frame_nhap_thongtin, width=30)
    entry_hoten.grid(row=0, column=1)

    label_mssv = Label(frame_nhap_thongtin, text="MSSV:")
    label_mssv.grid(row=1, column=0, sticky="w")
    entry_mssv = Entry(frame_nhap_thongtin, width=30)
    entry_mssv.grid(row=1, column=1)

    label_lop = Label(frame_nhap_thongtin, text="Lớp:")
    label_lop.grid(row=2, column=0, sticky="w")
    entry_lop = Entry(frame_nhap_thongtin, width=30)
    entry_lop.grid(row=2, column=1)

    label_sdt = Label(frame_nhap_thongtin, text="SĐT:")
    label_sdt.grid(row=3, column=0, sticky="w")
    entry_sdt = Entry(frame_nhap_thongtin, width=30)
    entry_sdt.grid(row=3, column=1)

    label_soluong = Label(frame_nhap_thongtin, text="Số lượng:")
    label_soluong.grid(row=4, column=0, sticky="w")
    entry_soluong = Entry(frame_nhap_thongtin, width=30)
    entry_soluong.grid(row=4, column=1)

    tt=["Đã đăng ký", "Hủy đăng ký", "Đã trả phòng"]
    combo_tt=Combobox(frame_nhap_trangthai,value=tt,state="disable")
    combo_tt.grid(row=0,column=0)
    combo_tt.current(0)

    label_ngay = Label(frame_nhap_thoigian, text="Ngày:")
    label_ngay.grid(row=0, column=0, sticky="w")
    dateentry_ngay = DateEntry(frame_nhap_thoigian,width=12,date_pattern="dd/mm/yyyy")
    dateentry_ngay.grid(row=0, column=1,columnspan=3, sticky="w")
    dateentry_ngay.delete(0, "end")

    label_danhsach=Label(frame_hienthids,text="DANH SÁCH MƯỢN PHÒNG")
    label_danhsach.grid(row=0,column=0)

    label_locds=Label(frame_locds,text="Lọc danh sách:")
    label_locds.grid(row=0,column=0,sticky="w")
    dateentry_locds_ngaybd = DateEntry(frame_locds,width=12,date_pattern="dd/mm/yyyy")
    dateentry_locds_ngaybd.grid(row=0, column=1, sticky="w")
    dateentry_locds_ngaybd.delete(0, "end")
    label_locds=Label(frame_locds,text="->")
    label_locds.grid(row=0,column=2,sticky="w")
    dateentry_locds_ngaykt = DateEntry(frame_locds,width=12,date_pattern="dd/mm/yyyy")
    dateentry_locds_ngaykt.grid(row=0, column=3, sticky="w")
    dateentry_locds_ngaykt.delete(0, "end")

    label_thongke=Label(frame_locds,text="Lọc để xem thống kê!")
    label_thongke.grid(row=1,column=0,columnspan=4,sticky="w")

    treeview_bang = Treeview(frame_hienthids,columns=("stt","hoten","mssv","lop","sdt","thoigian","soluong","trangthai"),show="headings")

    treeview_bang.heading("stt", text="STT")
    treeview_bang.heading("hoten", text="Họ và tên")
    treeview_bang.heading("mssv", text="MSSV")
    treeview_bang.heading("lop", text="Lớp")
    treeview_bang.heading("sdt", text="SĐT")
    treeview_bang.heading("thoigian",text="Thời gian")
    treeview_bang.heading("soluong", text="Số lượng")
    treeview_bang.heading("trangthai", text="Trạng thái")

    treeview_bang.column("stt",width=int(WIDTH*0.04))
    treeview_bang.column("hoten",width=int(WIDTH*0.2))
    treeview_bang.column("mssv",width=int(WIDTH*0.12))
    treeview_bang.column("lop",width=int(WIDTH*0.12))
    treeview_bang.column("sdt",width=int(WIDTH*0.1))
    treeview_bang.column("thoigian",width=int(WIDTH*0.18))
    treeview_bang.column("soluong",width=int(WIDTH*0.1))
    treeview_bang.column("trangthai",width=int(WIDTH*0.12))

    treeview_bang.grid(row=2,column=0,sticky="nsew")
    hien_thi(DSdangmuon,treeview_bang)

    scrollbar_bang = Scrollbar(frame_hienthids, orient="vertical", command=treeview_bang.yview)
    treeview_bang.configure(yscrollcommand=scrollbar_bang.set)
    scrollbar_bang.grid(row=2, column=1, sticky="ns")

    def button_them_click():
        giobd=spin_giobd.get()+":"+spin_phutbd.get()
        giokt=spin_giokt.get()+":"+spin_phutkt.get()
        vt=len(DSdangmuon) # xác định vị trí trong danh sách cho phần tử
        dlform=thong_tin_muon_phong(vt,dateentry_ngay.get(),entry_hoten.get(),entry_mssv.get(),entry_lop.get(),entry_sdt.get(),giobd,giokt,entry_soluong.get())
        DSdangmuon.append(dlform)
        sap_xep(DSdangmuon)
        hien_thi(DSdangmuon,treeview_bang)
        button_them.config(state="disable")
        button_sua.config(state="disable")
        button_luu.config(state="normal")
        return

    def hien_nut(event=None):
        nonlocal vi_tri_dang_chon
        
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
        gbd=int(spin_giobd.get())*60+int(spin_phutbd.get())
        gkt=int(spin_giokt.get())*60+int(spin_phutkt.get())
        if gbd>=gkt:
            return 1

        for ttmp in DSdangmuon:
            gbd2,pbd2=ttmp.giobd.split(":")
            gkt2,pkt2=ttmp.giokt.split(":")
            gbd2=int(gbd2)*60+int(pbd2)
            gkt2=int(gkt2)*60+int(pkt2)
            if(dang_sua==1):
                if int(vi_tri_dang_chon)==int(ttmp.vitritrongds):
                    continue
            if dateentry_ngay.get()==ttmp.ngay:
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
        
        entry_hoten.config(state="disable")
        entry_lop.config(state="disable")
        entry_mssv.config(state="disable")
        entry_sdt.config(state="disable")
        entry_soluong.config(state="disable")
        button_them.config(state="disable")
        button_sua.config(state="disable")
        button_huy.config(state="disable")
        combo_tt.config(state="disable")
        button_sua_tt.config(state="disable")
        vi_tri_dang_chon=None
        return

    vi_tri_dang_chon = None
    def treeview_bang_selected(event):
        nonlocal vi_tri_dang_chon
        item = treeview_bang.selection()

        if not item:
            return

        item = item[0]

        danh_sach_item = treeview_bang.get_children()
        vi_tri = danh_sach_item.index(item)

        ttm = DSdangmuon[vi_tri]
        entry_hoten.config(state="normal")
        entry_lop.config(state="normal")
        entry_mssv.config(state="normal")
        entry_sdt.config(state="normal")
        entry_soluong.config(state="normal")
        vi_tri_dang_chon = vi_tri

        entry_hoten.delete(0, "end")
        entry_hoten.insert(0, ttm.hoten)

        entry_mssv.delete(0, "end")
        entry_mssv.insert(0, ttm.mssv)

        entry_lop.delete(0, "end")
        entry_lop.insert(0, ttm.lop)

        entry_sdt.delete(0, "end")
        entry_sdt.insert(0, ttm.sdt)

        entry_soluong.delete(0, "end")
        entry_soluong.insert(0, ttm.soluong)

        dateentry_ngay.set_date(ttm.ngay)

        giobd, phutbd = ttm.giobd.split(":")
        giokt, phutkt = ttm.giokt.split(":")

        spin_giobd.delete(0, "end")
        spin_giobd.insert(0, giobd)

        spin_phutbd.delete(0, "end")
        spin_phutbd.insert(0, phutbd)

        spin_giokt.delete(0, "end")
        spin_giokt.insert(0, giokt)

        spin_phutkt.delete(0, "end")
        spin_phutkt.insert(0, phutkt)
        button_huy.config(state="normal")
        combo_tt.config(state="readonly")
        combo_tt.set(ttm.trangthai)
        return

    treeview_bang.bind("<<TreeviewSelect>>", treeview_bang_selected)

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
        ttm.giobd = spin_giobd.get()+":"+spin_phutbd.get()
        ttm.giokt = spin_giokt.get()+":"+spin_phutkt.get()
        
        DSdangmuon[vi_tri_dang_chon]=ttm

        sap_xep(DSdangmuon)
        hien_thi(DSdangmuon,treeview_bang)

        button_them.config(state="disable")
        button_sua.config(state="disable")
        button_luu.config(state="normal")
        return

    def button_luu_click():
        luu_database(DSdangmuon)
        button_luu.config(state="disable")
        return

    def button_sua_tt_click():
        nonlocal vi_tri_dang_chon
        DSdangmuon[vi_tri_dang_chon].trangthai=combo_tt.get()
        button_sua_tt.config(state="disable")
        button_luu.config(state="normal")
        hien_thi(DSdangmuon,treeview_bang)
        return

    def button_locds_macdinh_click():
        dateentry_locds_ngaybd.delete(0,"end")
        dateentry_locds_ngaykt.delete(0,"end")
        hien_thi(DSdangmuon,treeview_bang)
        label_thongke.config(text="Lọc để xem thống kê!")
        button_locds_macdinh.config(state="disable")
        return

    def dateentry_ngay_change(event=None):
        if not (spin_giobd.get() and spin_phutbd.get() and spin_giokt.get() and spin_phutkt.get()):
            return
        nonlocal vi_tri_dang_chon
        if vi_tri_dang_chon==None:
            if kt_trung_lich(0)==0:
                entry_hoten.config(state="normal")
                entry_lop.config(state="normal")
                entry_mssv.config(state="normal")
                entry_sdt.config(state="normal")
                entry_soluong.config(state="normal")
            else:
                entry_hoten.config(state="disable")
                entry_lop.config(state="disable")
                entry_mssv.config(state="disable")
                entry_sdt.config(state="disable")
                entry_soluong.config(state="disable")
        else:
            if kt_trung_lich(0)==0:
                button_them.config(state="normal")
            else:
                button_them.config(state="disable")

            if kt_trung_lich(1)==0:
                button_sua.config(state="normal")
            else:
                button_sua.config(state="disable")
        return

    def spin_giobd_change(event=None):
        dateentry_ngay_change()
        return
    
    def spin_phutbd_change(event=None):
        dateentry_ngay_change()
        return
    
    def spin_giokt_change(event=None):
        dateentry_ngay_change()
        return
    
    def spin_phutkt_change(event=None):
        dateentry_ngay_change()
        return

    def entry_hoten_change(event=None):
        nonlocal vi_tri_dang_chon
        if vi_tri_dang_chon==None:
            if entry_hoten.get() and entry_mssv.get() and entry_lop.get() and entry_sdt.get() and entry_soluong.get():
                button_them.config(state="normal")
            else:
                button_them.config(state="disable")
        else:
            button_sua.config(state="normal")
        button_huy.config(state="normal")
        return
    
    def entry_mssv_change(event=None):
        entry_hoten_change()
        return

    def entry_lop_change(event=None):
        entry_hoten_change()
        return
    
    def entry_sdt_change(event=None):
        entry_hoten_change()
        return
    
    def entry_soluong_change(event=None):
        entry_hoten_change()
        return

    def combo_tt_change(event=None):
        button_sua_tt.config(state="normal")
        return

    def dateentry_locds_ngaybd_change(event=None):
        if not dateentry_locds_ngaykt.get():
            return
        
        DSdangmuon_loc=[]
        soluongdk=0
        ngaybd=datetime.strptime(dateentry_locds_ngaybd.get(), "%d/%m/%Y").date()
        ngaykt=datetime.strptime(dateentry_locds_ngaykt.get(), "%d/%m/%Y").date()
        for ttmp in DSdangmuon:
            ngaymuon=datetime.strptime(ttmp.ngay, "%d/%m/%Y").date()
            if ngaybd<=ngaymuon and ngaymuon<=ngaykt and ttmp.trangthai!="Hủy đăng ký":
                DSdangmuon_loc.append(ttmp)
                soluongdk+=int(ttmp.soluong)

        hien_thi(DSdangmuon_loc,treeview_bang)
        soluotdk=len(DSdangmuon_loc)
        label_thongke.config(text=str(soluotdk)+" lượt đăng ký | "+str(soluongdk)+" số lượng sinh viên đăng ký")
        label_thongke.grid(row=1,column=0,columnspan=4,sticky="w")
        button_locds_macdinh.config(state="normal")
        return

    def dateentry_locds_ngaykt_change(event=None):
        dateentry_locds_ngaybd_change()
        return

    def root_exit():
        xac_nhan=messagebox.askyesnocancel("Xác nhận","Lưu dữ liệu trước khi thoát?")
        if xac_nhan==None:
            return
        if xac_nhan:
            luu_database(DSdangmuon)
        root.destroy()
        return
        
    entry_hoten.bind("<KeyRelease>", entry_hoten_change)
    entry_lop.bind("<KeyRelease>", entry_lop_change)
    entry_mssv.bind("<KeyRelease>", entry_mssv_change)
    entry_sdt.bind("<KeyRelease>", entry_sdt_change)
    entry_soluong.bind("<KeyRelease>", entry_soluong_change)
    dateentry_ngay.bind("<<DateEntrySelected>>", dateentry_ngay_change)
    dateentry_ngay.bind("<KeyRelease>", dateentry_ngay_change)
    combo_tt.bind("<<ComboboxSelected>>", combo_tt_change)
    dateentry_locds_ngaybd.bind("<<DateEntrySelected>>",dateentry_locds_ngaybd_change)
    dateentry_locds_ngaykt.bind("<<DateEntrySelected>>",dateentry_locds_ngaykt_change)
    root.protocol("WM_DELETE_WINDOW", root_exit)

    lblGioBD = Label(frame_nhap_thoigian, text="Bắt đầu:",width=8)
    lblGioBD.grid(row=1, column=0, sticky="w")
    spin_giobd = Spinbox(frame_nhap_thoigian,from_=7,to=20,width=3,format="%02.0f",command=spin_giobd_change)
    spin_giobd.bind("<KeyRelease>",spin_giobd_change)
    spin_giobd.grid(row=1, column=1, sticky="w")
    spin_giobd.delete(0, "end")
    lblHaiChamBD = Label(frame_nhap_thoigian, text=":")
    lblHaiChamBD.grid(row=1, column=2)
    spin_phutbd = Spinbox(frame_nhap_thoigian,from_=0,to=59,width=3,format="%02.0f",command=spin_phutbd_change)
    spin_phutbd.bind("<KeyRelease>",spin_phutbd_change)
    spin_phutbd.grid(row=1, column=3, sticky="w")
    spin_phutbd.delete(0, "end")

    lblGioKT = Label(frame_nhap_thoigian, text="Kết thúc:")
    lblGioKT.grid(row=2, column=0, sticky="w")
    spin_giokt = Spinbox(frame_nhap_thoigian,from_=7,to=20,width=3,format="%02.0f",command=spin_giokt_change)
    spin_giokt.bind("<KeyRelease>",spin_giokt_change)
    spin_giokt.grid(row=2, column=1, sticky="w")
    spin_giokt.delete(0, "end")
    lblHaiChamKT = Label(frame_nhap_thoigian, text=":")
    lblHaiChamKT.grid(row=2, column=2)
    spin_phutkt = Spinbox(frame_nhap_thoigian,from_=0,to=59,width=3,format="%02.0f",command=spin_phutkt_change)
    spin_phutkt.bind("<KeyRelease>",spin_phutkt_change)
    spin_phutkt.grid(row=2, column=3, sticky="w")
    spin_phutkt.delete(0, "end")

    button_them = Button(frame_nut, text="Thêm", command=button_them_click)
    button_them.grid(row=0, column=0)

    button_sua = Button(frame_nut, text="Sửa", command=button_sua_click)
    button_sua.grid(row=0, column=1)

    button_huy = Button(frame_nut, text="Hủy", command=button_huy_click)
    button_huy.grid(row=0, column=3)

    button_luu = Button(frame_nut, text="Lưu", command=button_luu_click)
    button_luu.grid(row=0, column=4)

    button_sua_tt=Button(frame_nhap_trangthai,text="Sửa trạng thái", command=button_sua_tt_click)
    button_sua_tt.grid(row=1,column=0)

    button_locds_macdinh=Button(frame_locds,text="Mặc định",command=button_locds_macdinh_click)
    button_locds_macdinh.grid(row=0,column=5)

    entry_hoten.config(state="disable")
    entry_lop.config(state="disable")
    entry_mssv.config(state="disable")
    entry_sdt.config(state="disable")
    entry_soluong.config(state="disable")
    button_them.config(state="disable")
    button_sua.config(state="disable")
    button_huy.config(state="disable")
    button_luu.config(state="disable")
    button_sua_tt.config(state="disable")
    button_locds_macdinh.config(state="disable")

    root.mainloop()

if __name__=="__main__":
    tao_database()
    main()
