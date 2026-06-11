// options.js
document.addEventListener('DOMContentLoaded', restoreOptions);
document.getElementById('saveBtn').addEventListener('click', saveOptions);

function saveOptions() {
  const sourceLang = document.getElementById('sourceLang').value;
  const targetLang = document.getElementById('targetLang').value;

  chrome.storage.sync.set({
    sourceLang: sourceLang,
    targetLang: targetLang
  }, () => {
    const status = document.getElementById('status');
    status.textContent = '設定已儲存！';
    setTimeout(() => {
      status.textContent = '';
    }, 2000);
  });
}

function restoreOptions() {
  chrome.storage.sync.get({
    sourceLang: 'auto',
    targetLang: 'zh-TW'
  }, (items) => {
    document.getElementById('sourceLang').value = items.sourceLang;
    document.getElementById('targetLang').value = items.targetLang;
  });
}