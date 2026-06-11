// content.js

let activeTooltip = null;

// 監聽來自 Background Script 的訊息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "get_selection") {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    
    if (text) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      
      sendResponse({
        text: text,
        rect: {
          top: rect.top,
          bottom: rect.bottom,
          left: rect.left,
          right: rect.right,
          width: rect.width,
          height: rect.height
        }
      });
    } else {
      sendResponse({ text: null });
    }
  } 
  else if (request.action === "show_translation") {
    showTooltip(request.text, request.rect);
    sendResponse({ success: true });
  }
  return true;
});

function showTooltip(text, rect) {
  removeTooltip();

  const tooltip = document.createElement('div');
  tooltip.className = 'quick-translator-tooltip';
  tooltip.innerText = text;

  document.body.appendChild(tooltip);

  // 計算位置
  let top, left;
  if (rect) {
    // 預設顯示在反白文字下方
    top = rect.bottom + window.scrollY + 10;
    left = rect.left + window.scrollX;
    
    // 確保不會超出右邊界
    const tooltipRect = tooltip.getBoundingClientRect();
    if (left + tooltipRect.width > window.innerWidth) {
      left = window.innerWidth - tooltipRect.width - 20;
    }
    
    // 如果下方空間不足，則顯示在上方
    if (top + tooltipRect.height > window.scrollY + window.innerHeight) {
      top = rect.top + window.scrollY - tooltipRect.height - 10;
    }
  } else {
    // 沒有座標資訊時，顯示在畫面中央
    top = window.scrollY + (window.innerHeight / 2);
    left = window.scrollX + (window.innerWidth / 2) - 150;
  }

  tooltip.style.top = `${top}px`;
  tooltip.style.left = `${left}px`;
  
  // 顯示動畫
  setTimeout(() => {
    tooltip.classList.add('show');
  }, 10);

  activeTooltip = tooltip;
}

function removeTooltip() {
  if (activeTooltip) {
    activeTooltip.remove();
    activeTooltip = null;
  }
}

// 點擊空白處關閉翻譯視窗
document.addEventListener('mousedown', (e) => {
  if (activeTooltip && !activeTooltip.contains(e.target)) {
    removeTooltip();
  }
});