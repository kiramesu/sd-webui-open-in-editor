onUiLoaded(function () {
    const addEditorButton = (tabId) => {
        // Prevent duplicate addition if the button already exists
        if (document.getElementById(`custom_editor_btn_${tabId}`)) return;

        // Find the reference "📐 (Send to Extras)" button
        const extrasBtn = document.getElementById(`${tabId}_send_to_extras`);
        if (!extrasBtn) return; // Abort if not found

        // Create the button to launch the paint software
        const btn = document.createElement('button');
        btn.id = `custom_editor_btn_${tabId}`;
        btn.innerHTML = '🖍'; 
        btn.title = 'Open in external paint software';

        // ★Most important point: Copy the exact same class (design and size settings) as the 📐 button
        btn.className = extrasBtn.className;

        // Process when the button is clicked
        btn.addEventListener('click', () => {
            const gallery = document.getElementById(`${tabId}_gallery`);
            if (!gallery) return;
            
            const img = gallery.querySelector('img'); 
            if (!img || !img.src) {
                alert("Image not found.");
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
                    alert("Error: " + data.message);
                }
            })
            .catch(err => console.error(err));
        });

        // ★Change in placement: Insert immediately after the 📐 button
        // This ensures they are neatly aligned side by side within the same group
        extrasBtn.insertAdjacentElement('afterend', btn);
    };

    // Execute after UI has finished loading
    addEditorButton('txt2img');
    addEditorButton('img2img');
});
