import json
import os

# 設定項目
TRAINING_DATA_FILE = "training_data.json"

def load_data(filepath):
    """JSONファイルを読み込む。なければ空の辞書を返す。"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(filepath, data):
    """データをJSONファイルに書き込む。"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n完了: データを '{filepath}' に保存しました。")

def main():
    """対話形式で新しい知識を training_data.json に追加する"""
    print("--- 橘 真白 教育モード ---")
    print("これから真白に新しいことを教えます。（終了するにはキーワード入力で何も入力せずEnter）")

    # 既存のデータを読み込む
    training_data = load_data(TRAINING_DATA_FILE)
    
    while True:
        # 1. キーワード（質問）を受け取る
        keyword = input("\n[質問] 真白に教えるキーワードを入力してください: ")
        
        # 何も入力されなければループを終了
        if not keyword:
            print("教育モードを終了します。")
            break
            
        # 2. 応答を受け取る
        response = input(f"[応答] 「{keyword}」に対する真白の応答を入力してください: ")
        
        # 3. データを更新
        training_data[keyword] = response
        print(f"学習内容: 【{keyword}】->【{response}】")

    # 4. 変更をファイルに保存
    if training_data:
        save_data(TRAINING_DATA_FILE, training_data)

if __name__ == '__main__':
    main()