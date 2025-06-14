import os
from collections import defaultdict, Counter

# --- 設定項目 ---
INPUT_FILE = 'wiki_texts.txt'
OUTPUT_MODEL_FILE = 'ngram_model.txt' 
N = 2

def main():
    """
    テキストファイルからn-gramモデルを学習し、テキストファイルとして保存する。
    """
    print(f"n-gramモデルの学習を開始します... (n={N})")
    if not os.path.exists(INPUT_FILE):
        print(f"エラー: 入力ファイル '{INPUT_FILE}' が見つかりません。")
        return

    ngram_model = defaultdict(Counter)
    line_count = 0
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            if len(words) < N: continue
            for i in range(len(words) - N + 1):
                context = tuple(words[i : i + N - 1])
                target = words[i + N - 1]
                ngram_model[" ".join(context)][target] += 1
            
            line_count += 1
            if line_count % 100000 == 0:
                print(f"{line_count} 行を処理しました...")

    print("\n学習が完了しました！新しい形式でモデルをファイルに保存します...")
    with open(OUTPUT_MODEL_FILE, 'w', encoding='utf-8') as f:
        for context, targets in ngram_model.items():
            target_str = ",".join([f"{word}:{count}" for word, count in targets.items()])
            f.write(f"{context}\t{target_str}\n")
    
    print(f"モデルを '{OUTPUT_MODEL_FILE}' という名前で保存しました。")


# ★★★ これが、プログラムを起動するための重要な部分 ★★★
if __name__ == '__main__':
    main()