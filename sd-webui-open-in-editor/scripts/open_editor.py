import os
import subprocess
import urllib.parse  # 追加: URLのエンコード（%20など）を元に戻すための標準ライブラリ
from fastapi import FastAPI, Body
from modules import script_callbacks, shared

# 外部ソフトで画像を開く関数
def open_image_in_editor(image_path: str, original_url: str):
    # 設定から.exeのパスを取得して両端のクォーテーションを削除
    editor_path = shared.opts.data.get("editor_executable_path", "")
    if editor_path:
        editor_path = editor_path.strip('\"\'')
    
    if not editor_path or not os.path.exists(editor_path):
        return {"status": "error", "message": f"Settingsで正しいペイントソフトのパスが設定されていません。認識されたパス: {editor_path}"}

    # 【変更点】エラー時に「Pythonがどんなパスを探して失敗したか」をポップアップに表示するようにしました
    if not os.path.exists(image_path):
        return {
            "status": "error", 
            "message": f"画像ファイルが見つかりません。\n[探したパス]: {image_path}\n[元のURL]: {original_url}"
        }

    try:
        # バックグラウンドでプロセスを起動
        subprocess.Popen([editor_path, image_path])
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# FastAPIにカスタムエンドポイントを追加 (JSからの通信窓口)
def on_app_started(block, app: FastAPI):
    @app.post("/custom/open-in-editor")
    def api_open_in_editor(image_path: str = Body(..., embed=True)):
        # 1. URLエンコード（%20など）を元のスペース等に戻す
        decoded_url = urllib.parse.unquote(image_path)
        
        # 2. http://.../file= 等の余分なURL部分を削ぎ落としてローカルパスだけを抽出
        clean_path = decoded_url
        if "file=" in clean_path:
            clean_path = clean_path.split("file=")[-1]
        elif "filename=" in clean_path: # WebUIのバージョン違い対策
            clean_path = clean_path.split("filename=")[-1]
            
        # 3. 万が一末尾に ?xxx のようなパラメータがあれば除去
        clean_path = clean_path.split("?")[0]
        
        return open_image_in_editor(clean_path, image_path)

# Settingsタブに設定項目を追加
def on_ui_settings():
    section = ("open_in_editor", "Paint software")
    shared.opts.add_option(
        "editor_executable_path",
        shared.OptionInfo(
            "",
            "ペイントソフトの実行ファイルパス (例: C:\\Program Files\\Adobe\\Adobe Photoshop 2024\\Photoshop.exe)",
            section=section
        )
    )

script_callbacks.on_app_started(on_app_started)
script_callbacks.on_ui_settings(on_ui_settings)