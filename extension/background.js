let ws = null;
let mediaRecorder = null;
let audioStream = null;

function connectWebSocket() {
  if (ws && ws.readyState === WebSocket.OPEN) return;
  
  ws = new WebSocket('ws://localhost:8765');
  
  ws.onopen = () => {
    console.log('Connected to local backend');
  };
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'subtitle') {
        // Send subtitle to the active tab to render
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
            if(tabs[0]){
                chrome.tabs.sendMessage(tabs[0].id, {
                    action: "render_subtitle",
                    original: data.original,
                    translated: data.translated
                });
            }
        });
      }
    } catch (e) {
      console.error('Error parsing WS message', e);
    }
  };
  
  ws.onclose = () => {
    console.log('WS Connection closed');
    setTimeout(connectWebSocket, 3000); // Reconnect
  };
}

// Initial connection
connectWebSocket();

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "start_capture") {
    chrome.tabCapture.capture({ audio: true, video: false }, (stream) => {
      if (!stream) {
        console.error('Failed to capture tab audio.');
        return;
      }
      
      audioStream = stream;
      
      // Need to play the audio back to the user since tabCapture mutes the tab
      const audioCtx = new AudioContext();
      const source = audioCtx.createMediaStreamSource(stream);
      source.connect(audioCtx.destination);
      
      // Start recording and sending complete WebM chunks every 2.5 seconds
      let recordInterval = setInterval(() => {
        if (!audioStream || !audioStream.active) {
          clearInterval(recordInterval);
          return;
        }
        try {
          const recorder = new MediaRecorder(audioStream, { mimeType: 'audio/webm;codecs=opus' });
          recorder.ondataavailable = (e) => {
            if (e.data.size > 0 && ws && ws.readyState === WebSocket.OPEN) {
              ws.send(e.data); // This is a complete, decodable webm file
            }
          };
          recorder.start();
          setTimeout(() => {
            if (recorder.state === 'recording') recorder.stop();
          }, 2500);
        } catch (err) {
          console.error("Recorder error", err);
        }
      }, 2500);
      
      // Notify backend to start transcription
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: "start_transcription" }));
      }
      
      // Inject content script if not already injected (to show subtitles)
      chrome.scripting.executeScript({
        target: { tabId: request.tabId },
        files: ["content.js"]
      }).then(() => {
        // After injection, immediately render the initial waiting text
        chrome.tabs.sendMessage(request.tabId, {
            action: "render_subtitle",
            original: "",
            translated: "【请配置 OpenAI API Key以开始翻译】"
        });
      }).catch(err => console.log('Script already injected or error', err));
      
      chrome.scripting.insertCSS({
        target: { tabId: request.tabId },
        files: ["styles.css"]
      }).catch(err => console.log('CSS already injected or error', err));
    });
  } else if (request.action === "stop_capture") {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
    if (audioStream) {
      audioStream.getTracks().forEach(track => track.stop());
    }
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ action: "stop_transcription" }));
    }
  }
});