/* ===================================================================
   沖縄県トレーラーハウス協会 — 連絡先・リンク設定
   決まったらこのブロックだけ書き換えてください。
   "" のままの項目は「準備中」表示になり、リンク切れになりません。
   =================================================================== */
window.SITE = {
  orgName:  "一般社団法人 沖縄県トレーラーハウス協会",
  email:    "",   // 例 "info@example.jp" — 問い合わせフォームの送信先にも使われます
  tel:      "",   // 例 "098-000-0000"
  address:  "",   // 例 "沖縄県那覇市〇〇1-2-3"
  rep:      "",   // 代表理事名
  founded:  "",   // 設立年月
  formPost: ""    // Formspree / GAS などのURL。空ならメール送信にフォールバック
};

/* ---- 以下は共通処理。通常は編集不要です ---- */
document.addEventListener('DOMContentLoaded', function () {
  var S = window.SITE || {};

  // data-info="キー" の要素に値を差し込む。未設定なら「準備中」表示。
  document.querySelectorAll('[data-info]').forEach(function (el) {
    var v = S[el.dataset.info];
    if (v) { el.textContent = v; }
    else { el.innerHTML = '<span class="todo">準備中</span>'; }
  });

  // メール・電話リンク
  document.querySelectorAll('[data-link]').forEach(function (el) {
    var k = el.dataset.link, url = '';
    if (k === 'mail' && S.email) url = 'mailto:' + S.email;
    if (k === 'tel'  && S.tel)   url = 'tel:' + S.tel.replace(/[^0-9+]/g, '');
    if (!url) {
      el.setAttribute('data-disabled', '');
      el.removeAttribute('href');
      el.setAttribute('aria-disabled', 'true');
    } else {
      el.setAttribute('href', url);
      if (k === 'mail' && el.dataset.showtext === '1') el.textContent = S.email;
      if (k === 'tel'  && el.dataset.showtext === '1') el.textContent = S.tel;
    }
  });

  var form = document.querySelector('form[data-contact]');
  if (!form) return;
  var post = S.formPost, mail = S.email;

  // 送信先が何も決まっていなければ送信不可にする
  if (!post && !mail) {
    var b = form.querySelector('[type="submit"]');
    if (b) { b.setAttribute('data-disabled', ''); b.disabled = true; }
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    return;
  }

  if (post) { form.action = post; form.method = 'POST'; return; }

  // メールしか無い場合はメールソフトを開く方式で送信する
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = new FormData(form);
    var need = { kind: 'お問い合わせ種別', name: 'お名前', email: 'メールアドレス' };
    var miss = Object.keys(need).filter(function (k) { return !(f.get(k) || '').trim(); })
                     .map(function (k) { return need[k]; });
    var err = form.querySelector('.form-error');
    if (miss.length) {
      if (!err) {
        err = document.createElement('p');
        err.className = 'form-error';
        form.querySelector('.form-note').before(err);
      }
      err.textContent = miss.join('、') + ' を入力してください。';
      return;
    }
    if (err) err.remove();
    var body =
      'お問い合わせ種別: ' + f.get('kind') + '\n' +
      '会社・団体名: ' + (f.get('company') || '（未記入）') + '\n' +
      'お名前: ' + f.get('name') + '\n' +
      'メールアドレス: ' + f.get('email') + '\n' +
      '電話番号: ' + (f.get('tel') || '（未記入）') + '\n' +
      '\n--- お問い合わせ内容 ---\n' + (f.get('message') || '（未記入）') + '\n';
    location.href = 'mailto:' + mail
      + '?subject=' + encodeURIComponent('【協会サイト】' + f.get('kind'))
      + '&body=' + encodeURIComponent(body);
  });
});
