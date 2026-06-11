// background.js

// 建立右鍵選單
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "translate-selection",
    title: "翻譯選取文字",
    contexts: ["selection"]
  });
});

// 處理右鍵選單點擊
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "translate-selection" && info.selectionText) {
    handleTranslation(info.selectionText, tab);
  }
});

// 處理快捷鍵觸發
chrome.commands.onCommand.addListener((command) => {
  if (command === "translate_shortcut") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length === 0) return;
      const tab = tabs[0];
      
      // 向 Content Script 請求當前選取的文字
      chrome.tabs.sendMessage(tab.id, { action: "get_selection" }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("無法與頁面通訊:", chrome.runtime.lastError.message);
          return;
        }
        if (response && response.text) {
          handleTranslation(response.text, tab, response.rect);
        }
      });
    });
  }
});

// 處理翻譯邏輯
async function handleTranslation(text, tab, rect = null) {
  try {
    const items = await chrome.storage.sync.get({ sourceLang: 'auto', targetLang: 'zh-TW' });
    const sl = items.sourceLang;
    const tl = items.targetLang;
    
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sl}&tl=${tl}&dt=t&q=${encodeURIComponent(text)}`;
    
    const res = await fetch(url);
    const data = await res.json();
    
    let translatedText = "";
    if (data && data[0]) {
      data[0].forEach(item => {
        if (item[0]) translatedText += item[0];
      });
    }

    if (!translatedText) throw new Error("Translation empty");

    // 嘗試在網頁中顯示浮動視窗 (透過 Content Script)
    chrome.tabs.sendMessage(tab.id, { 
      action: "show_translation", 
      text: translatedText,
      rect: rect 
    }, (response) => {
      // 如果 Content Script 沒有回應 (例如在 PDF 原生閱讀器中)
      if (chrome.runtime.lastError) {
        showNotification(translatedText);
      }
    });

  } catch (error) {
    console.error("Translation error:", error);
    showNotification("翻譯失敗，請稍後再試。");
  }
}

// PDF 等不支援 Content Script 的頁面，使用系統通知作為備案
function showNotification(message) {
  chrome.notifications.create({
    type: "basic",
    iconUrl: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4Ij48cmVjdCB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgZmlsbD0iIzAwN2JmZiIvPjx0ZXh0IHg9IjMyIiB5PSI4MCIgZmlsbD0iI2ZmZiIgZm9udC1zaXplPSI2NCI+VDwvdGV4dD48L3N2Zz4=",
    title: "Quick Translator",
    message: message
  });
}