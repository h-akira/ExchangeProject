// Bardにより生成
// ただし，「入力時に実行」の部分は改行してないのに入力するたびに
// 大きさが変わるという不具合が生じたためfunctionの一部を変更

// ページ読み込み時に実行
document.addEventListener('DOMContentLoaded', function() {
  // classがdynamic-textareaであるtextareaを取得
  const textareas = document.querySelectorAll('.dynamic-textarea');
  // textareaの縦の大きさを調整
  textareas.forEach(textarea => {
    autoResizeTextArea(textarea);
  });
});

// 入力時に実行
document.addEventListener('input', function(event) {
  // 対象要素がtextareaタグであり、かつclass属性に"dynamic-textarea"が含まれている場合
  if (event.target.tagName.toLowerCase() === 'textarea' && event.target.classList.contains('dynamic-textarea')) {
    // textareaの縦の大きさを調整
    autoResizeTextArea(event.target);
  }
});

function autoResizeTextArea(textArea) {
  // 以下を参照
  // https://kodocode.net/design-js-textarea/
  const scrollHeight = textArea.scrollHeight;
  const temporary = document.querySelector('.temporary-height');
  temporary.style.cssText = 'height : ' + scrollHeight + 'px;';
  textArea.style.cssText = 'height : auto;';
  textArea.style.cssText = 'height : ' + scrollHeight + 'px;';
}
