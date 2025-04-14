import json
import os

def test_write():
    base_dir = os.path.dirname(__file__)
    json_dir = os.path.join(base_dir, "json")  # json フォルダのパス
    file_path = os.path.join(json_dir, "reservations.json")

    # json フォルダが存在しない場合は作成
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
        print(f"json フォルダを作成しました: {json_dir}")

    # テストデータ
    test_data = [{"代表者名": "テスト 太郎", "メールアドレス": "test@example.com"}]

    # ファイルに書き込み
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(test_data, file, ensure_ascii=False, indent=4)
        print(f"テストデータを書き込みました: {file_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

test_write()