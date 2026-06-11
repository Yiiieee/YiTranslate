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

  const header = document.createElement('div');
  header.className = 'quick-translator-header';
  
  const dragHandle = document.createElement('span');
  dragHandle.className = 'quick-translator-drag-handle';
  dragHandle.innerText = '⋮⋮';
  
  const closeBtn = document.createElement('span');
  closeBtn.className = 'quick-translator-close';
  closeBtn.innerText = '×';
  closeBtn.onclick = removeTooltip;

  header.appendChild(dragHandle);
  header.appendChild(closeBtn);

  const content = document.createElement('div');
  content.className = 'quick-translator-content';
  content.innerText = text;

  tooltip.appendChild(header);
  tooltip.appendChild(content);

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
  
  // 拖曳邏輯
  let isDragging = false;
  let dragOffsetX = 0;
  let dragOffsetY = 0;

  const onMouseDown = (e) => {
    if (e.target === closeBtn) return;
    isDragging = true;
    dragOffsetX = e.clientX - tooltip.getBoundingClientRect().left;
    dragOffsetY = e.clientY - tooltip.getBoundingClientRect().top;
    tooltip.style.transition = 'none'; // 停止 transition 以避免拖曳時卡頓
    e.preventDefault();
  };

  const onMouseMove = (e) => {
    if (!isDragging) return;
    tooltip.style.left = `${e.clientX - dragOffsetX + window.scrollX}px`;
    tooltip.style.top = `${e.clientY - dragOffsetY + window.scrollY}px`;
  };

  const onMouseUp = () => {
    if (isDragging) {
      isDragging = false;
      tooltip.style.transition = 'opacity 0.2s ease-in-out, transform 0.2s ease-in-out';
    }
  };

  header.addEventListener('mousedown', onMouseDown);
  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);

  tooltip._dragCleanup = () => {
    header.removeEventListener('mousedown', onMouseDown);
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
  };

  // 顯示動畫
  setTimeout(() => {
    tooltip.classList.add('show');
  }, 10);

  activeTooltip = tooltip;
}

function removeTooltip() {
  if (activeTooltip) {
    if (activeTooltip._dragCleanup) activeTooltip._dragCleanup();
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