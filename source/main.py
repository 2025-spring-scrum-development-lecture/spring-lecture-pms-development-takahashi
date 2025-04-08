import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import json
import os
from party import HotelBookingApp_party
from json_access import check_room
from datetime import timedelta 

# 解像度をあげた
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass

class HotelBookingApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=1500, height=750)
        self.pack()
        master.geometry('1500x750')
        master.title('予約管理アプリ')
        self.room_data = self.load_room_data()
        self.create_widgets()  
    
    def load_room_data(self):
        """JSONファイルから部屋データを読み込む"""
        base_dir = os.path.dirname(__file__)  # 現在のスクリプトのディレクトリを取得
        file_path = os.path.join(base_dir, "../json/room.json")  # room.json のパスを指定
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)    

    def create_widgets(self):   
        frame1 = tk.Frame(self, relief="solid", bd=0.5)
        frame1.place(x=870, y=100, width=600, height=560)
        
        self.title_label = tk.Label(self, text="お客様情報入力", font=("", 30))
        self.title_label.place(x=20, y=15)
        
        # メモ
        self.memo_label = tk.Label(frame1,text="メモ",font=("",20))
        self.memo_label.place(x=10,y=15)
        self.text_widget = tk.Text(frame1, height=24, width=58)
        self.text_widget.place(x=3, y=70)
        
        # 代表者名
        self.name_label = tk.Label(self, text="代表者名", font=("", 20))
        self.name_label.place(x=200, y=150)  # yを130から150に変更
        self.name_entry = tk.Entry(self, width=30, relief="solid", font=("", 14))
        self.name_entry.place(x=380, y=155, height=40)  # yを135から155に変更

        # 宴会ボタン
        self.party_button = tk.Button(self, text="宴会利用者はこちら", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite",command=self.go_party)
        self.party_button.place(x=480, y=20, height=60)  

        # 接客マニュアルボタン
        self.manual_button = tk.Button(self, text="接客マニュアル", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite", command=self.show_manual)
        self.manual_button.place(x=780, y=20, height=60)

        # メールアドレス
        self.email_label = tk.Label(self, text="メールアドレス", font=("", 20))
        self.email_label.place(x=120, y=220)  # yを200から220に変更
        self.email_entry = tk.Entry(self, width=30, relief="solid", font=("", 14))
        self.email_entry.place(x=380, y=225, height=40)  # yを205から225に変更

        # 人数
        self.people_label = tk.Label(self, text="人数", font=("", 20))
        self.people_label.place(x=275, y=295)  # yを275から295に変更
        self.people_entry = tk.Entry(self, width=5, relief="solid", font=("", 14))
        self.people_entry.place(x=380, y=300, height=40)  # yを280から300に変更
        self.people_label = tk.Label(self, text="名", font=("", 17))
        self.people_label.place(x=460, y=303)  # yを283から303に変更

        # 宿泊プラン
        self.party_course_label = tk.Label(self, text="宿泊プラン", font=("", 20))
        self.party_course_label.place(x=163, y=365)  # yを345から365に変更
        self.party_course_combobox = ttk.Combobox(self, width=30, font=("", 13), state="readonly")
        self.party_course_combobox['values'] = ("行わない", "豪華コース", "雅コース", "錦コース", "椿コース")
        self.party_course_combobox.place(x=380, y=370, height=40)  # yを350から370に変更

        # 部屋の種類
        self.room_type_label = tk.Label(self, text="部屋の種類", font=("", 20))
        self.room_type_label.place(x=155, y=440)  # yを420から440に変更
        self.room_type_combobox = ttk.Combobox(self, width=30, font=("", 13), state="readonly")
        self.room_type_combobox.place(x=380, y=445, height=40)  # yを425から445に変更

        # 宿泊期間
        self.checkin_label = tk.Label(self, text="宿泊期間", font=("", 20))
        self.checkin_label.place(x=190, y=520)  # yを500から520に変更
        self.checkin_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2, font=("", 14), date_pattern='yyyy-mm-dd')
        self.checkin_entry.place(x=380, y=525, height=40)  # yを505から525に変更
        self.checkin_label = tk.Label(self, text="～", font=("", 20))
        self.checkin_label.place(x=590, y=520)  # yを500から520に変更
        # チェックアウト日（ラベルに変更）
        self.checkout_label = tk.Label(self, text="未選択", font=("", 20))
        self.checkout_label.place(x=650, y=525)
        self.checkin_entry.bind("<<DateEntrySelected>>", self.update_checkout_date)
        
        # 確認ボタン
        self.confirm_button = tk.Button(self, text="確認", font=('', 12), relief=tk.RIDGE, width=20, bg="skyblue", activebackground="floralwhite",command=self.act_check)
        self.confirm_button.place(x=370, y=620, height=60)  # yを650から670に変更

    def show_manual(self):
        """接客マニュアルウィンドウを表示"""
        manual_window = tk.Toplevel(self)
        manual_window.title("接客マニュアル")
        manual_window.geometry("700x500")
        # マニュアル内容
        manual_text = """接客マニュアル:
1. 宴会をするかどうかきく
2. 各自項目に対する要望をきく
3. アレルギーなどの必要な情報をメモにまとめておく
"""

        manual_label = tk.Label(manual_window, text=manual_text, font=("", 14), justify="left")
        manual_label.pack(padx=20, pady=20)
    
    def go_party(self):
        self.destroy()
        HotelBookingApp_party(self.master)
        
    def act_check(self):
        room_type = self.room_type_combobox.get()
        checkin_date = self.checkin_entry.get_date()
        checkout_date = self.checkout_entry.get_date()
        result = check_room(room_type,checkin_date,checkout_date)
        if result == "OK":
            self.go_confirm
        else:
            self.go_room_list  
            
    def update_checkout_date(self, event):
        """チェックイン日を基にチェックアウト日を更新"""
        checkin_date = self.checkin_entry.get_date()
        checkout_date = checkin_date + timedelta(days=1)  # 翌日を計算
        self.checkout_label.config(text=checkout_date.strftime('%Y-%m-%d'))

                           
    def go_confirm(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        people = self.people_entry.get()
        room_type = self.room_type_combobox.get()
        checkin_date = self.checkin_entry.get_date()
        checkout_date = self.checkout_entry.get_date()
        memo = self.text_widget.get("1.0", tk.END).strip()

        # 確認画面に遷移
        from main_confirm import Confirm
        self.destroy()
        Confirm(self.master, name, email, people, room_type, checkin_date, checkout_date, memo)
                
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp(root)
    app.mainloop()