import tkinter as tk
from tkinter import messagebox  # メッセージボックスを使用するためにインポート
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass
  
class Confirm(tk.Frame):
    def __init__(self, master, name, email, people, room_type, checkin_date, checkout_date, memo):
        super().__init__(master, width=1500, height=750)
        self.pack()
        master.geometry('1500x750')  
        master.title('予約内容確認')

        # 情報を表示するウィジェットを作成
        self.create_widgets(name, email, people, room_type, checkin_date, checkout_date, memo)

    def create_widgets(self, name, email, people, room_type, checkin_date, checkout_date, memo):
        self.title_label = tk.Label(self, text="お客様情報確認", font=("", 30))
        self.title_label.place(x=20, y=15)
        
        # 確定ボタン
        self.confirm_button = tk.Button(self, text="予約確定", font=('', 12), relief=tk.RIDGE, width=20, bg="skyblue", activebackground="floralwhite")
        self.confirm_button.place(x=1200, y=20, height=60)  
        
        # やり直しボタン
        self.return_button = tk.Button(self, text="やり直す", font=('', 12), relief=tk.RIDGE, width=20, bg="white", activebackground="floralwhite", command=self.confirm_reset)
        self.return_button.place(x=900, y=20, height=60)  
        
        # 名前とメールアドレスフレーム
        name_email_frame = tk.Frame(self, relief="solid", bd=0.5)
        name_email_frame.place(x=120, y=120, width=620, height=200)
        tk.Label(name_email_frame, text="代表者情報", font=("", 16)).pack(anchor="w", padx=10, pady=5)
        tk.Label(name_email_frame, text=f"代表者名: {name}", font=("", 14)).pack(anchor="w", padx=10, pady=5)
        tk.Label(name_email_frame, text=f"メールアドレス: {email}", font=("", 14)).pack(anchor="w", padx=10, pady=5)

        # 宿泊プランフレーム
        plan_frame = tk.Frame(self, relief="solid", bd=0.5)
        plan_frame.place(x=120, y=330, width=620, height=370)
        tk.Label(plan_frame, text="宿泊プラン", font=("", 16)).pack(anchor="w", padx=10, pady=5)
        tk.Label(plan_frame, text=f"人数: {people}名", font=("", 14)).pack(anchor="w", padx=10, pady=5)
        tk.Label(plan_frame, text=f"部屋の種類: {room_type}", font=("", 14)).pack(anchor="w", padx=10, pady=5)
        tk.Label(plan_frame, text=f"チェックイン日: {checkin_date}", font=("", 14)).pack(anchor="w", padx=10, pady=5)
        tk.Label(plan_frame, text=f"チェックアウト日: {checkout_date}", font=("", 14)).pack(anchor="w", padx=10, pady=5)

        # 料金フレーム
        price_frame = tk.Frame(self, relief="solid", bd=0.5)
        price_frame.place(x=750, y=120, width=620, height=200)
        tk.Label(price_frame, text="料金情報", font=("", 16)).pack(anchor="w", padx=10, pady=5)
        # 料金情報はここに追加（例: 料金計算結果など）

        # メモフレーム
        memo_frame = tk.Frame(self, relief="solid", bd=0.5)
        memo_frame.place(x=750, y=330, width=620, height=370)
        tk.Label(memo_frame, text="メモ", font=("", 16)).pack(anchor="w", padx=10, pady=5)
        tk.Label(memo_frame, text=memo, font=("", 14), wraplength=600, justify="left").pack(anchor="w", padx=10, pady=5)

    def confirm_reset(self):
        """やり直し確認メッセージを表示"""
        result = messagebox.askokcancel(
            "確認",
            "本当にやり直しますか？現在入力したものはリセットされます。"
        )
        if result:  # OKが押された場合
            self.go_main()

    def go_main(self):
        """メイン画面に遷移"""
        from main import HotelBookingApp
        self.destroy()
        HotelBookingApp(self.master)



if __name__ == '__main__':
    root = tk.Tk()
    app = Confirm(root, "田中 太郎", "tanaka@example.com", "3", "岩手山側 露天風呂付和室（本館）", "2025-04-10", "2025-04-12", "アレルギー: 甲殻類")
    app.mainloop()