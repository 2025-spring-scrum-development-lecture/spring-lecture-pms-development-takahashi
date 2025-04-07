import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import json
import os

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
        
        # 宴会ボタン
        self.party_button = tk.Button(self, text="宴会不要者はこちら", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite")
        self.party_button.place(x=480, y=20, height=60)
        
        # 接客マニュアルボタン
        self.manual_button = tk.Button(self, text="接客マニュアル", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite", command=self.show_manual)
        self.manual_button.place(x=780, y=20, height=60)

        
        # メモ
        self.memo_label = tk.Label(frame1,text="メモ",font=("",20))
        self.memo_label.place(x=10,y=15)
        self.text_widget = tk.Text(frame1, height=24, width=58)
        self.text_widget.place(x=3, y=70)
        
        # 代表者名
        self.name_label = tk.Label(self, text="代表者名", font=("", 20))
        self.name_label.place(x=200, y=120)  # yを150から120に変更
        self.name_entry = tk.Entry(self, width=30, relief="solid", font=("", 14))
        self.name_entry.place(x=380, y=125, height=40)  # yを155から125に変更

        # メールアドレス
        self.email_label = tk.Label(self, text="メールアドレス", font=("", 20))
        self.email_label.place(x=120, y=190)  # yを220から190に変更
        self.email_entry = tk.Entry(self, width=30, relief="solid", font=("", 14))
        self.email_entry.place(x=380, y=195, height=40)  # yを225から195に変更

        # 人数
        self.people_label = tk.Label(self, text="人数", font=("", 20))
        self.people_label.place(x=275, y=265)  # yを295から265に変更
        self.people_entry = tk.Entry(self, width=5, relief="solid", font=("", 14))
        self.people_entry.place(x=380, y=270, height=40)  # yを300から270に変更
        self.people_label = tk.Label(self, text="名", font=("", 17))
        self.people_label.place(x=460, y=273)  # yを303から273に変更

        # 部屋数
        self.room_label = tk.Label(self, text="宿泊部屋数", font=("", 20))
        self.room_label.place(x=160, y=335)  # yを295から265に変更
        self.room_entry = tk.Entry(self, width=5, relief="solid", font=("", 14))
        self.room_entry.place(x=380, y=340, height=40)  # yを300から270に変更
        self.room_label = tk.Label(self, text="部屋", font=("", 17))
        self.room_label.place(x=460, y=343)  # yを303から273に変更

        # 宴会コース
        self.party_course_label = tk.Label(self, text="宴会コース", font=("", 20))
        self.party_course_label.place(x=163, y=405)  # yを335から405に変更
        self.party_course_combobox = ttk.Combobox(self, width=30, font=("", 13), state="readonly")
        self.party_course_combobox['values'] = ("行わない", "豪華コース", "雅コース", "錦コース", "椿コース")
        self.party_course_combobox.place(x=380, y=410, height=40)  # yを340から410に変更

        # 宴会
        self.party_date_label = tk.Label(self, text="宴会日", font=("", 20))
        self.party_date_label.place(x=237, y=490)  # yを490から560に変更
        self.party_date_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2, font=("", 14), date_pattern='yyyy-mm-dd')
        self.party_date_entry.place(x=380, y=495, height=40)  # yを495から565に変更
        
        # 宿泊期間
        self.checkin_label = tk.Label(self, text="宿泊期間", font=("", 20))
        self.checkin_label.place(x=190, y=560)  # yを490から560に変更
        self.checkin_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2, font=("", 14), date_pattern='yyyy-mm-dd')
        self.checkin_entry.place(x=380, y=565, height=40)  # yを495から565に変更
        self.checkin_label = tk.Label(self, text="～", font=("", 20))
        self.checkin_label.place(x=590, y=560)  # yを490から560に変更
        self.checkout_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2, font=("", 14), date_pattern='yyyy-mm-dd')
        self.checkout_entry.place(x=650, y=565, height=40)  # yを495から565に変更
       
        # 確認ボタン
        self.reserve_button = tk.Button(self, text="確認", font=('', 12), relief=tk.RIDGE, width=20, bg="skyblue", activebackground="floralwhite")
        self.reserve_button.place(x=370, y=650, height=60)  # yを650から670に変更
            
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

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp(root)
    app.mainloop()