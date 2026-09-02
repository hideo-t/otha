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

`assets/links.js` の `window.SITE` が空のうちは「準備中」と表示される。
表示言語は html の lang 属性から選ばれる（同ファイル冒頭の `TODO_LABEL`）。
