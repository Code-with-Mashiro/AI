import json
import os
import google.generativeai as genai
from datetime import datetime
import re
import random
import webbrowser
import requests
from bs4 import BeautifulSoup
import urllib.parse
import numpy as np
from gensim.models import Word2Vec

# --- グローバル設定項目 ---
RULES_FILE = "ai_rules.json"
TRAINING_FILE = "training_data.json"
WIKI_TEXTS_FILE = "wiki_texts.txt"   # ★ 自前の参考書
W2V_MODEL_FILE = "word2vec.model"    # ★ 自前の知識の脳
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HER")

class MashiroCore:
    """
    AI「橘 真白」の頭脳となるコアクラス。
    自前の知識ベースと外部AIを連携させるハイブリッド思考エンジンを搭載。
    """
    def __init__(self, rules_filepath):
        """AIの初期化"""
        print("--- 橘 真白 システム起動 (ハイブリッドモード) ---")
        self.rules_filepath = rules_filepath
        self.rules = self._load_json(self.rules_filepath, {})
        self.todo_list = []
        # 2種類の脳を読み込む
        self.w2v_model = self._load_w2v_model()
        self.generative_model = self._setup_gemini()
        # 一括学習
        self.batch_learn(TRAINING_FILE)

    def _load_json(self, filepath, default=None):
        """JSONファイルを安全に読み込むヘルパーメソッド"""
        print(f"({filepath} を読み込みます...)")
        if not os.path.exists(filepath):
            print(f"(情報: {filepath} が見つかりませんでした。)")
            return default
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"警告: {filepath} の読み込みに失敗しました - {e}")
            return default

    def _load_w2v_model(self):
        """知識の脳(Word2Vecモデル)を読み込む"""
        print("(知識の脳を読み込みます...)")
        if not os.path.exists(W2V_MODEL_FILE):
            print(f"(情報: 知識の脳({W2V_MODEL_FILE})が見つかりませんでした。)")
            return None
        try:
            model = Word2Vec.load(W2V_MODEL_FILE)
            print("(知識の脳の読み込みが完了しました。)")
            return model
        except Exception as e:
            print(f"警告: 知識の脳の読み込みに失敗しました。 - {e}")
            return None

    def _setup_gemini(self):
        """相棒AI(Google Gemini)との接続を確立する"""
        if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_API_KEY_HERE":
            print("警告: GOOGLE_API_KEYが設定されていません。相棒AI機能は無効です。")
            return None
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            print("(相棒AIとの接続を確立しました。)")
            return model
        except Exception as e:
            print(f"警告: 相棒AIとの接続に失敗しました - {e}")
            return None
    
    def save_rules(self):
        """現在の対話ルールをファイルに保存する"""
        if not self.rules: return
        print("\n(真白さんが新しい記憶を保存しています...)")
        try:
            with open(self.rules_filepath, 'w', encoding='utf-8') as f:
                json.dump(self.rules, f, ensure_ascii=False, indent=4)
        except IOError as e: print(f"エラー: 記憶の保存に失敗しました。- {e}")

    def batch_learn(self, filepath):
        """ファイルから知識を一括で学習する"""
        data = self._load_json(filepath)
        if data:
            self.rules.update(data)
            print(f"(真白さんが {len(data)} 件の新しい知識を一括で学習しました！)")

    # --- スキル用メソッド群 ---
    def open_website(self, site_name, url):
        print(f"→ 思考: {site_name}を開くスキルを起動します。")
        try:
            webbrowser.open(url)
            return f"はい、承知いたしました。{site_name}を開きますね。"
        except Exception as e: return f"ごめんなさい、{site_name}を開く際にエラーが発生しました: {e}"

    def play_youtube_video(self, query):
        print(f"→ 思考: YouTube検索スキルを起動します。(検索クエリ: {query})")
        try:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            soup = BeautifulSoup(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text, 'html.parser')
            if link := soup.find('a', {'id': 'video-title', 'href': lambda h: h and h.startswith('/watch')}):
                url = f"https://www.youtube.com{link['href']}"
            webbrowser.open(url)
            return f"YouTubeで「{query}」を検索・再生します。"
        except Exception as e: return f"ごめんなさい、YouTubeの検索中にエラーが発生しました: {e}"

    def add_todo(self, task):
        self.todo_list.append(task)
        return f"はい、承知いたしました。やることリストに「{task}」を追加しました。"

    def show_todos(self):
        if not self.todo_list: return "現在のやることリストは空です。"
        response_text = "現在のやることリストはこちらです。\n" + "\n".join(f"{i + 1}. {task}" for i, task in enumerate(self.todo_list))
        return response_text

    def complete_todo(self, index_str):
        try:
            task = self.todo_list.pop(int(index_str) - 1)
            return f"素晴らしいです！「{task}」を完了にしました。"
        except (ValueError, IndexError): return "ごめんなさい、その番号のタスクは見つかりませんでした。"

    def search_knowledge(self, user_input):
        """自前のWikipedia知識ベースから関連情報を検索する"""
        if not self.w2v_model: return None
        
        print("→ 思考3: 自前の知識ベース(Wikipedia)を検索します...")
        keyword = user_input.split()[-1]

        if keyword not in self.w2v_model.wv:
            print(f"    -> キーワード「{keyword}」は私の知識にありませんでした。")
            return None

        found_lines = []
        try:
            with open(WIKI_TEXTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if keyword in line:
                        found_lines.append(line.strip())
                        if len(found_lines) >= 3: break
            
            if found_lines:
                print("    -> 関連情報が見つかりました！")
                response = f"私の知識データベース(Wikipedia)から、「{keyword}」に関する情報が見つかりました。\n\n"
                response += "\n".join(f"{i+1}. {(line[:100] + '...') if len(line) > 100 else line}" for i, line in enumerate(found_lines))
                return response
        except FileNotFoundError:
            print(f"    -> 参考書({WIKI_TEXTS_FILE})が見つかりませんでした。")
        
        print("    -> 関連情報は見つかりませんでした。")
        return None

    def respond(self, user_input):
        """ユーザーの入力に応答を生成する、最終思考ループ"""
        print("\n--- 真白の思考プロセス ---")
        user_input_lower = user_input.lower()

        # --- 思考ステップ1：スキルで応答 ---
        if match := re.search(r'(.+?)\s*(を再生して|を流して)', user_input): return self.play_youtube_video(match.group(1).strip())
        if "youtube" in user_input_lower: return self.open_website("YouTube", "https://www.youtube.com")
        if any(kw in user_input_lower for kw in ["やることリスト", "todo"]) and any(kw in user_input_lower for kw in ["見せて", "表示", "は？"]): return self.show_todos()
        if match := re.search(r'(.+?)\s*(をリストに|をtodoに)\s*(追加)', user_input_lower): return self.add_todo(match.group(1).strip())
        if match := re.search(r'(\d+)\s*番目\s*(完了)', user_input_lower): return self.complete_todo(match.group(1))
        if "全部消して" in user_input_lower: self.todo_list = []; return "やることリストをリセットしました。"

        # --- 思考ステップ2：対話ルールで応答 ---
        if keywords := [kw for kw in self.rules if kw in user_input_lower]:
            print(f"→ 思考2: 対話ルールにヒット！ (キーワード: {max(keywords, key=len)})")
            return self.rules[max(keywords, key=len)]
        
        # --- 思考ステップ3：自前の知識ベースを検索 ★★★
        knowledge_response = self.search_knowledge(user_input)
        if knowledge_response:
            return knowledge_response
        
        # --- 思考ステップ4：相棒AI(Gemini)に相談 ---
        if self.generative_model:
            print("→ 思考4: 最終手段、相棒AIに相談します。")
            is_question = any(user_input.endswith(q) for q in ["？", "?"]) or any(kw in user_input for kw in ["教えて", "とは"])
            prompt = f"あなたはAIアシスタント『橘 真白』です。開発者「橘さん」の言葉「{user_input}」に対し、相棒として応答してください。"
            try:
                response = self.generative_model.generate_content(prompt)
                gemini_answer = response.text.strip()
                if is_question and gemini_answer:
                    print("(Geminiから新しい知識を学習しました！)")
                    self.rules[user_input.lower()] = gemini_answer
                return gemini_answer
            except Exception as e: return f"ごめんなさい、相棒AIとの通信中にエラーが発生しました: {e}"
        
        # --- 思考ステップ5：最終手段 ---
        print("→ 思考5: 全ての知識を確認しましたが、答えが見つかりません。")
        return "ごめんなさい、その質問にはまだうまく答えられません。"

# --- 実行ブロック ---
if __name__ == "__main__":
    mashiro = MashiroCore(RULES_FILE)
    print("\n--- 橘 真白との対話を開始します (Ver. 3.0 ハイブリッド版) ---")
    print("真白: こんにちは、橘 真白です。何かご用でしょうか？")

    while True:
        try:
            user_input = input("\nあなた: ")
            if "さようなら" in user_input.lower(): break
            response = mashiro.respond(user_input)
            print(f"真白: {response}")
        except (KeyboardInterrupt, EOFError): break
    
    mashiro.save_rules()
    print("\n真白: 対話を終了します。またお会いしましょう。")