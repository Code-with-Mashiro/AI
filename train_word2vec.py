import logging
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

# --- 設定項目 ---
# 入力ファイル名（前回作成した、Wikipediaのテキストデータ）
input_filename = 'wiki_texts.txt'
# 出力ファイル名（学習済みモデルを保存する名前）
output_model_name = 'word2vec.model'

def main():
    """
    Wikipediaのテキストデータを学習し、Word2Vecモデルを作成・保存する。
    """
    # 処理の進捗を表示するための設定
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    print(f"'{input_filename}' から文章を読み込んでいます...")
    # 巨大なテキストファイルを一行ずつ効率よく読み込む
    sentences = LineSentence(input_filename)

    print("Word2Vecモデルの学習を開始します...")
    print("この処理もPCの性能によっては数時間かかることがあります。")

    # Word2Vecモデルの学習
    # vector_size: 単語を表現するベクトルの次元数（100〜300が一般的）
    # window: 注目する単語の、前後何単語までを文脈として考慮するか
    # min_count: この回数未満しか出現しない単語は無視する（ノイズ除去）
    # workers: 学習に使うCPUコア数（-1は利用可能な全コアを使う）
    model = Word2Vec(sentences,
                     vector_size=200,
                     window=5,
                     min_count=5,
                     workers=-1)
    
    print("学習が完了しました！")

    # 学習したモデルをファイルに保存
    model.save(output_model_name)
    print(f"学習済みモデルを '{output_model_name}' という名前で保存しました。")
    print("これでいつでも学習結果を呼び出せます。")


if __name__ == '__main__':
    main()