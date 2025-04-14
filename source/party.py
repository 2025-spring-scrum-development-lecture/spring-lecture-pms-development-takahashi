import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import json
import os
from datetime import timedelta
import tkinter.messagebox as messagebox

# 解像度をあげた
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass

class HotelBookingApp_party(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=1500, height=750)
        self.pack()
        master.geometry('1500x750')
        master.title('宴会予約管理アプリ')
        self.party_data = self.load_party_data()  # 宴会データをロード
        self.room_data = self.load_room_data()  # 部屋データをロード
        self.create_widgets()

    def load_party_data(self):
        """JSONファイルから宴会コースデータを読み込む"""
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "../json/party.json")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("エラー", "party.json ファイルが見つかりません。")
            return []

    def load_room_data(self):
        """JSONファイルから部屋データを読み込む"""
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "../json/room.json")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("エラー", "room.json ファイルが見つかりません。")
            return []

    def create_widgets(self):
        # メインフレーム
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
        self.name_label.place(x=200, y=90)
        self.name_entry = tk.Entry(self, width=30, relief="solid", font=("", 14))
        self.name_entry.place(x=380, y=95, height=40)

        # メールアドレス
        self.email_label = tk.Label(self, text="メールアドレス", font=("", 20))
        self.email_label.place(x=120, y=160)
        self.email_entry = tk.Entry(self, width=30, relief="solid", font=("", 14))
        self.email_entry.place(x=380, y=165, height=40)

        # 人数
        self.people_label = tk.Label(self, text="人数", font=("", 20))
        self.people_label.place(x=275, y=235)
        self.people_entry = tk.Entry(self, width=5, relief="solid", font=("", 14))
        self.people_entry.place(x=380, y=240, height=40)
        self.people_unit_label = tk.Label(self, text="名", font=("", 17))
        self.people_unit_label.place(x=460, y=243)

        # 部屋数
        self.room_label = tk.Label(self, text="部屋数", font=("", 20))
        self.room_label.place(x=230, y=305)
        self.room_entry = tk.Entry(self, width=5, relief="solid", font=("", 14))
        self.room_entry.place(x=380, y=310, height=40)
        self.room_unit_label = tk.Label(self, text="部屋", font=("", 17))
        self.room_unit_label.place(x=460, y=313)

        # 宴会コース
        self.party_course_label = tk.Label(self, text="宴会コース", font=("", 20))
        self.party_course_label.place(x=163, y=375)
        self.party_course_combobox = ttk.Combobox(self, width=30, font=("", 13), state="readonly")
        self.party_course_combobox['values'] = [course["宴会名"] for course in self.party_data]
        self.party_course_combobox.place(x=380, y=380, height=40)

        # 宴会日
        self.party_date_label = tk.Label(self, text="宴会日", font=("", 20))
        self.party_date_label.place(x=237, y=445)
        self.party_date_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2, font=("", 14), date_pattern='yyyy-mm-dd')
        self.party_date_entry.place(x=380, y=450, height=40)
        self.party_date_entry.bind("<<DateEntrySelected>>", self.update_stay_period)

        # 宿泊期間
        self.stay_period_label = tk.Label(self, text="宿泊期間　未選択", font=("", 20))
        self.stay_period_label.place(x=190, y=515)

        # 見積
        self.estimate_label = tk.Label(self, text="見積　 ¥0", font=("", 20))
        self.estimate_label.place(x=260, y=590)

        # 確認ボタン
        self.confirm_button = tk.Button(self, text="確認", font=('', 12), relief=tk.RIDGE, width=20, bg="skyblue", activebackground="floralwhite", command=self.act_check)
        self.confirm_button.place(x=370, y=660, height=60)

        # 人数または宴会コース変更時に見積を更新
        self.people_entry.bind("<KeyRelease>", self.update_total_price)
        self.room_entry.bind("<KeyRelease>", self.update_total_price)
        self.party_course_combobox.bind("<<ComboboxSelected>>", self.update_total_price)
        
        # 宴会ボタン
        self.party_button = tk.Button(self, text="宴会不要者はこちら", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite", command=self.go_main)
        self.party_button.place(x=480, y=20, height=60)

        # 接客マニュアルボタン
        self.manual_button = tk.Button(self, text="接客マニュアル", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite", command=self.show_manual)
        self.manual_button.place(x=780, y=20, height=60)

    def update_total_price(self, event=None):
        """人数と宴会コースに基づいて見積金額を計算"""
        try:
            # 人数を取得
            people = int(self.people_entry.get())
        except ValueError:
            people = 0  # 無効な値の場合は0に設定

        try:
            # 部屋数を取得
            rooms = int(self.room_entry.get())
        except ValueError:
            rooms = 0  # 無効な値の場合は0に設定

        # 選択された宴会コースを取得
        selected_course = self.party_course_combobox.get()
        price_per_person = 0

        # 宴会コースの料金を取得
        for course in self.party_data:
            if course["宴会名"] == selected_course:
                price_per_person = course["一人あたりの料金"]
                break

        # 合計料金を計算
        total_price = people * price_per_person

        # 見積ラベルを更新
        self.estimate_label.config(text=f"見積　 ¥{total_price:,}")

    def update_stay_period(self, event):
        """宴会日を基に宿泊期間を更新"""
        self.party_date = self.party_date_entry.get_date()  # 宴会日を取得
        self.checkout_date = self.party_date + timedelta(days=1)  # 翌日を計算
        # 宿泊期間ラベルを更新
        self.stay_period_label.config(text=f"宿泊期間　{self.party_date.strftime('%Y-%m-%d')} ～ {self.checkout_date.strftime('%Y-%m-%d')}")

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

    def go_main(self):
        self.destroy()
        from main import HotelBookingApp
        HotelBookingApp(self.master)

    def act_check(self):
        """予約情報を確認し、重複がなければ確認画面に遷移"""
        name = self.name_entry.get()
        email = self.email_entry.get()
        people = self.people_entry.get()
        rooms = self.room_entry.get()
        party_course = self.party_course_combobox.get()
        party_date = self.party_date_entry.get_date().strftime('%Y-%m-%d')
        memo = self.text_widget.get("1.0", tk.END).strip()
        checkin_date = self.party_date_entry.get_date().strftime('%Y-%m-%d')
        checkout_date = self.checkout_date

        if not name or not email or not people or not rooms or not party_course:
            messagebox.showerror("エラー", "すべての必須項目を入力してください。")
            return

        try:
            people = int(people)
            rooms = int(rooms)
            if people <= 0 or rooms <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("エラー", "人数と部屋数は正の整数で入力してください。")
            return

        # 部屋の割り当て
        selected_rooms = [room for course in self.party_data if course["宴会名"] == party_course for room in course["対応部屋"]]
        assigned_rooms = selected_rooms[:rooms]  # 入力された部屋数に基づいて割り当て

        if len(assigned_rooms) < rooms:
            messagebox.showerror("エラー", "選択した宴会コースに対応する部屋が不足しています。")
            return

        # 合計料金を計算
        price_per_person = next((course["一人あたりの料金"] for course in self.party_data if course["宴会名"] == party_course), 0)
        total_price = people * price_per_person

        # 確認画面に遷移
        from party_confirm import Application
        self.destroy()
        Application(self.master, name, email, people, rooms,assigned_rooms, party_course, party_date,checkin_date,checkout_date, memo, total_price)

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp_party(root)
    app.mainloop()