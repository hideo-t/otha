# 一般社団法人 沖縄県トレーラーハウス協会

https://hideo-t.github.io/otha/


## 多言語（日 / 英 / 繁 / 簡 / 韓）

日本語の `index.html` を原本に、`en/` `zh-Hant/` `zh-Hans/` `ko/` を生成する。
生成物は直接編集しない。

    python i18n/extract.py    # 原文を抽出
    python i18n/merge.py      # 未訳の確認
    python i18n/build.py      # 全言語 + sitemap.xml を生成
    python i18n/verify.py     # 構造・リンク・未訳の検証

新しい文言を足したら、`i18n/apply.py` に添字指定の訳文JSONを渡して
翻訳メモリ（`i18n/strings/_tr/`）に入れる。原文キーは改行を含むことがあり
手で書き写すと取り違えるため、添字で渡す。

### 公開先を変えるとき

`i18n/config.py` の先頭を書き換えて `python i18n/build.py` を流し直す。

| 設定 | GitHub Pages（現状） | 独自ドメイン |
|---|---|---|
| `SITE` | `https://hideo-t.github.io` | `https://example.org` |
| `BASE` | `/otha` | `""` |
| `NOINDEX` | `True` | `False` |

あわせて `robots.txt` の `Disallow: /` を戻し、`CNAME` を置く。

### 連絡先

連絡先は日本語原本の静的HTMLに記載し、他言語は通常の翻訳フローで生成する。
JavaScriptによる日本語の上書きは行わない。送信先のないフォームは掲載せず、代表電話へ案内する。
住所・電話・FAXは2026-10-10に提供資料の確定テキストと既存公式サイトの会社概要を照合済み。

### 検証

Python環境に `beautifulsoup4` を導入し、通常の生成後に次も実行する。

```sh
python i18n/verify.py
python scripts/check_site.py
```

後者は原本も含む全ページの内部リンク・アンカー・画像ファイルと連絡先を検証する。
ブラウザーでのスマートフォン表示とキーボード操作は別途確認する。

### 独自ドメイン移行（未実施）

`trailer-okinawa.jp` は既存WordPressサイトが稼働中。DNS切替前に承認を得ること。
2026-10-10の読み取り確認では apex / www のAは `157.120.209.178`、
MXは `10 mail74.onamae.ne.jp`、SPFは `v=spf1 include:_spf.onamae.ne.jp ~all`。
ネームサーバーは `ns-rs1.gmoserver.jp` / `ns-rs2.gmoserver.jp`。移行直前に再確認する。

1. WordPressのデータベース・ファイル・アップロード・URL一覧とDNSゾーンをバックアップし、復元方法を確認する。
2. GitHub Pagesへ移す場合は、現行の公式手順に沿ってドメイン所有権確認、Pagesの独自ドメイン設定、apexとwwwのWeb向けレコードのみの変更を具体化して承認を得る。NS・MX・SPF・DKIM・DMARC等のメール設定を変更しない。
3. 承認後にSITE/BASE、CNAME、robots設定を変更して全言語を再生成する。旧WordPressの会社概要・ブログ・お問い合わせURLの扱いも決定する。
4. DNS反映・TLS証明書・HTTPS強制・全言語URL・画像・連絡先を確認してから検索除外を解除する。失敗時は記録したWeb向けDNSへ戻せるよう旧ホスティングを保持する。

代表者・設立日・会員一覧・会費・正式な入会条件は資料未確認。推測で補わない。
