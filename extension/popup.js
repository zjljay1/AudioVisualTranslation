document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('startBtn');
  const stopBtn = document.getElementById('stopBtn');
  const sourceLang = document.getElementById('sourceLang');
  const targetLang = document.getElementById('targetLang');

  // Load saved state
  chrome.storage.local.get(['isCapturing', 'sourceLang', 'targetLang'], (result) => {
    if (result.isCapturing) {
      startBtn.style.display = 'none';
      stopBtn.style.display = 'block';
    }
    if (result.sourceLang) sourceLang.value = result.sourceLang;
    if (result.targetLang) targetLang.value = result.targetLang;
  });

  // Save settings on change
  sourceLang.addEventListener('change', () => chrome.storage.local.set({ sourceLang: sourceLang.value }));
  targetLang.addEventListener('change', () => chrome.storage.local.set({ targetLang: targetLang.value }));

  startBtn.addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.runtime.sendMessage({ action: "start_capture", tabId: tab.id });
    
    chrome.storage.local.set({ isCapturing: true });
    startBtn.style.display = 'none';
    stopBtn.style.display = 'block';
  });

  stopBtn.addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: "stop_capture" });
    
    chrome.storage.local.set({ isCapturing: false });
    startBtn.style.display = 'block';
    stopBtn.style.display = 'none';
  });
});