import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import json
import os
from party import HotelBookingApp_party
from json_access import check_room
from datetime import timedelta
from tkinter import messagebox

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
        self.plan_data = self.load_plan_data()  # プランデータをロード
        self.plan_names = [plan["プラン名"] for plan in self.plan_data]  # プラン名をリスト化
        self.create_widgets()

    def load_room_data(self):
        """JSONファイルから部屋データを読み込む"""
        base_dir = os.path.dirname(__file__)  # 現在のスクリプトのディレクトリを取得
        file_path = os.path.join(base_dir, "../json/room.json")  # room.json のパスを指定
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_plan_data(self):
        """JSONファイルからプランデータを取得"""
        base_dir = os.path.dirname(__file__)  # 現在のスクリプトのディレクトリを取得
        file_path = os.path.join(base_dir, "../json/plan.json")  # plan.json のパスを指定
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def create_widgets(self):
        frame1 = tk.Frame(self, relief="solid", bd=0.5)
        frame1.place(x=870, y=100, width=600, height=560)

        self.title_label = tk.Label(self, text="お客様情報入力", font=("", 30))
        self.title_label.place(x=20, y=15)

        # メモ
        self.memo_label = tk.Label(frame1, text="メモ", font=("", 20))
        self.memo_label.place(x=10, y=15)
        self.text_widget = tk.Text(frame1, height=24, width=58)
        self.text_widget.place(x=3, y=70)

        # 代表者名
        self.name_label = tk.Label(self, text="代表者名", font=("", 20))
        self.name_label.place(x=200, y=120)
        self.name_entry = tk.Entry(self, width=30, relief="solid", font=("", 14))
        self.name_entry.place(x=380, y=125, height=40)

        # 宴会ボタン
        self.party_button = tk.Button(self, text="宴会利用者はこちら", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite", command=self.go_party)
        self.party_button.place(x=480, y=20, height=60)

        # 接客マニュアルボタン
        self.manual_button = tk.Button(self, text="接客マニュアル", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite", command=self.show_manual)
        self.manual_button.place(x=780, y=20, height=60)

        # メールアドレス
        self.email_label = tk.Label(self, text="メールアドレス", font=("", 20))
        self.email_label.place(x=100, y=190)
        self.email_entry = tk.Entry(self, width=30, relief="solid", font=("", 14))
        self.email_entry.place(x=380, y=195, height=40)

        # 人数
        self.people_label = tk.Label(self, text="人数", font=("", 20))
        self.people_label.place(x=260, y=265)
        self.people_entry = tk.Entry(self, width=5, relief="solid", font=("", 14))
        self.people_entry.place(x=380, y=270, height=40)
        self.people_label = tk.Label(self, text="名", font=("", 17))
        self.people_label.place(x=460, y=273)

        # 宿泊プラン
        self.party_course_label = tk.Label(self, text="宿泊プラン", font=("", 20))
        self.party_course_label.place(x=163, y=335)
        self.party_course_combobox = ttk.Combobox(self, width=30, font=("", 13), state="readonly")
        self.party_course_combobox['values'] = self.plan_names  # プラン名を設定
        self.party_course_combobox.place(x=380, y=340, height=40)
        self.party_course_combobox.bind("<<ComboboxSelected>>", self.update_room_types)  # プラン選択時に部屋を更新

        # 部屋の種類
        self.room_type_label = tk.Label(self, text="部屋の種類", font=("", 20))
        self.room_type_label.place(x=155, y=410)
        self.room_type_combobox = ttk.Combobox(self, width=30, font=("", 13), state="readonly")
        self.room_type_combobox.place(x=380, y=415, height=40)

        # 宿泊期間
        self.checkin_label = tk.Label(self, text="宿泊期間", font=("", 20))
        self.checkin_label.place(x=190, y=490)
        self.checkin_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2, font=("", 14), date_pattern='yyyy-mm-dd')
        self.checkin_entry.place(x=380, y=495, height=40)
        self.checkin_label = tk.Label(self, text="～", font=("", 20))
        self.checkin_label.place(x=590, y=490)
        self.checkout_label = tk.Label(self, text="未選択", font=("", 20))
        self.checkout_label.place(x=650, y=495)
        self.checkin_entry.bind("<<DateEntrySelected>>", self.update_checkout_date)

        # 見積
        self.nice_guy_sawafuji = tk.Label(self, text="見積　 ¥0", font=("", 20))
        self.nice_guy_sawafuji.place(x=260, y=570)

        # 確認ボタン
        self.confirm_button = tk.Button(self, text="確認", font=('', 12), relief=tk.RIDGE, width=20, bg="skyblue", activebackground="floralwhite", command=self.act_check)
        self.confirm_button.place(x=370, y=660, height=60)

        # 人数またはプラン変更時に見積を更新
        self.people_entry.bind("<KeyRelease>", self.update_total_price)

    def update_room_types(self, event):
        """選択されたプランに応じて部屋の種類を更新"""
        selected_plan = self.party_course_combobox.get().strip()
        for plan in self.plan_data:
            if plan["プラン名"].strip() == selected_plan:
                self.room_type_combobox['values'] = plan["対応部屋"]
                return
        self.room_type_combobox['values'] = []  # プランが選択されていない場合は空にする

    def update_total_price(self, event=None):
        """人数とプランに基づいて見積金額を計算"""
        try:
            people = int(self.people_entry.get())
        except ValueError:
            people = 0

        selected_plan = self.party_course_combobox.get()
        price_per_person = 0
        for plan in self.plan_data:
            if plan["プラン名"] == selected_plan:
                price_per_person = plan["一人当たりの料金"]
                break

        total_price = people * price_per_person
        self.nice_guy_sawafuji.config(text=f"見積　 ¥{total_price:,}")

    def show_manual(self):
        """接客マニュアルウィンドウを表示"""
        manual_window = tk.Toplevel(self)
        manual_window.title("接客マニュアル")
        manual_window.geometry("700x500")
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
        result = check_room(room_type, checkin_date, checkout_date)
        if result == "OK":
            self.go_confirm()
        else:
            messagebox.showerror("戻れ", "部屋が空いていません。別の日程を選択してください。")
            return

    def update_checkout_date(self, event):
        """チェックイン日を基にチェックアウト日を更新"""
        checkin_date = self.checkin_entry.get_date()
        checkout_date = checkin_date + timedelta(days=1)
        self.checkout_label.config(text=checkout_date.strftime('%Y-%m-%d'))

    def go_confirm(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        people = self.people_entry.get()
        room_type = self.room_type_combobox.get()
        checkin_date = self.checkin_entry.get_date()
        checkout_date = self.checkout_entry.get_date()
        memo = self.text_widget.get("1.0", tk.END).strip()

        from main_confirm import Confirm
        self.destroy()
        Confirm(self.master, name, email, people, room_type, checkin_date, checkout_date, memo)


if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp(root)
    app.mainloop()