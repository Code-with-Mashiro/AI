import os
from gensim.corpora import WikiCorpus

# --- 設定項目 ---
# 入力ファイル名（ダウンロードしたWikipediaのダンプファイル）
input_filename = 'jawiki-latest-pages-articles.xml.bz2'
# 出力ファイル名（抽出したテキストを保存するファイル）
output_filename = 'wiki_texts.txt'

def main():
    """Wikipediaのダンプファイルからテキストを抽出し、ファイルに保存する"""

    # 入力ファイルが存在するかチェック
    if not os.path.exists(input_filename):
        print(f"エラー: 入力ファイル '{input_filename}' が見つかりません。")
        print("ダウンロードしたWikipediaのファイルと同じフォルダで実行してください。")
        return

    print(f"'{input_filename}' からテキストの抽出を開始します...")
    print("この処理は数時間かかることがあります。気長にお待ちください。")

    # WikiCorpusを使ってテキストを抽出
    wiki = WikiCorpus(input_filename, dictionary={})
    
    article_count = 0
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        # 1記事ずつ処理してファイルに書き込む
        for text in wiki.get_texts():
            # 分かち書きされた単語を、スペースで連結して1行の文章にする
            line = ' '.join(text)
            output_file.write(line + '\n')
            
            article_count += 1
            # 1000記事処理するごとに進捗を表示
            if article_count % 1000 == 0:
                print(f"{article_count} 件の記事を処理しました...")

    print("\n処理が完了しました！")
    print(f"合計 {article_count} 件の記事を抽出し、'{output_filename}' に保存しました。")


if __name__ == '__main__':
    main()