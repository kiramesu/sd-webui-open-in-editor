# sd-webui-open-in-editor

Stable Diffusion WebUI (AUTOMATIC1111) で生成した画像を、ワンクリックで直接Photoshopなどの外部ペイントソフトに送って開くための拡張機能です。

## インストール方法
1. WebUIの `Extensions` タブを開く
2. `Install from URL` タブを開く
3. `URL for extension's git repository` にこのリポジトリのURLを入力:
   `https://github.com/あなたのユーザー名/sd-webui-open-in-editor`
4. `Install` ボタンを押す
5. `Installed` タブで `Apply and restart UI` を押す

## 使い方
1. `Settings` ＞ `Paint software` を開きます。

2. 使用したいペイントソフトの `.exe` ファイルのフルパスを入力し、設定を保存します。
   *(例: `C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe`)*

3. ギャラリーの下に追加された「🖍」ボタンを押すと、現在表示されている画像が指定したソフトで瞬時に開かれます。