let subtitleContainer = null;
let originalTextElem = null;
let translatedTextElem = null;

function initSubtitleUI() {
    if (document.getElementById('avt-subtitle-container')) return;

    subtitleContainer = document.createElement('div');
    subtitleContainer.id = 'avt-subtitle-container';
    
    translatedTextElem = document.createElement('div');
    translatedTextElem.id = 'avt-translated';
    translatedTextElem.innerText = "等待识别中...";
    
    originalTextElem = document.createElement('div');
    originalTextElem.id = 'avt-original';
    
    subtitleContainer.appendChild(translatedTextElem);
    subtitleContainer.appendChild(originalTextElem);
    
    document.body.appendChild(subtitleContainer);

    // Make it draggable
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    subtitleContainer.addEventListener("mousedown", dragStart);
    document.addEventListener("mouseup", dragEnd);
    document.addEventListener("mousemove", drag);

    function dragStart(e) {
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;
        if (e.target === subtitleContainer || e.target.parentNode === subtitleContainer) {
            isDragging = true;
        }
    }

    function dragEnd(e) {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
            xOffset = currentX;
            yOffset = currentY;
            setTranslate(currentX, currentY, subtitleContainer);
        }
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
    }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "render_subtitle") {
        initSubtitleUI();
        
        if (request.translated) {
            translatedTextElem.innerText = request.translated;
            translatedTextElem.style.display = 'block';
        }
        
        if (request.original) {
            originalTextElem.innerText = request.original;
            originalTextElem.style.display = 'block';
        } else {
            originalTextElem.style.display = 'none';
        }
    }
});