onUiLoaded(function () {
    const addEditorButton = (tabId) => {
        // すでにボタンがある場合の二重追加防止
        if (document.getElementById(`custom_editor_btn_${tabId}`)) return;

        // 基準となる「📐（Extrasへ送る）」ボタンを探す
        const extrasBtn = document.getElementById(`${tabId}_send_to_extras`);
        if (!extrasBtn) return; // 見つからなければ処理を中断

        // ペイントソフト起動用ボタンの作成
        const btn = document.createElement('button');
        btn.id = `custom_editor_btn_${tabId}`;
        btn.innerHTML = '🖍'; 
        btn.title = '外部ペイントソフトで開く';

        // ★最重要ポイント: 📐ボタンと全く同じクラス（デザイン・サイズ設定）をコピーする
        btn.className = extrasBtn.className;

        // ボタンクリック時の処理
        btn.addEventListener('click', () => {
            const gallery = document.getElementById(`${tabId}_gallery`);
            if (!gallery) return;
            
            const img = gallery.querySelector('img'); 
            if (!img || !img.src) {
                alert("画像が見つかりません。");
                return;
            }

            fetch('/custom/open-in-editor', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image_path: img.src })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'error') {
                    alert("エラー: " + data.message);
                }
            })
            .catch(err => console.error(err));
        });

        // ★配置の変更: 📐ボタンの「直後」に挿入する
        // これにより、同じグループ内で隣同士に綺麗に並びます
        extrasBtn.insertAdjacentElement('afterend', btn);
    };

    // UI読み込み完了時に実行
    addEditorButton('txt2img');
    addEditorButton('img2img');
});