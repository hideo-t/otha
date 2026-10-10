# -*- coding: utf-8 -*-
"""多言語ビルドの共通設定。

日本語版（リポジトリ直下）を原本とし、言語ごとのディレクトリに
翻訳済み静的HTMLを生成する。

公開先を変えるときは SITE と BASE の2つだけを書き換える:
  GitHub Pages のプロジェクトURL  SITE="https://hideo-t.github.io"  BASE="/otha"
  独自ドメイン                    SITE="https://example.org"        BASE=""
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, "i18n")
STRINGS = os.path.join(I18N, "strings")

# ---- 公開先。ここだけ差し替える -------------------------------------------
SITE = "https://trailer-okinawa.jp"
BASE = ""

# 暫定URLのうちは検索インデックスを止めておく。ここで拾われてしまうと
# 本ドメインに移したときに評価が分散し、重複コンテンツ扱いにもなりうる。
# 独自ドメインに切り替えるときに False にする。
NOINDEX = True
# ---------------------------------------------------------------------------

# 出力先ディレクトリ名 -> (html lang属性, og:locale, 言語切替UIの表示名)
LANGS = {
    "en":      ("en",      "en_US", "English"),
    "zh-Hant": ("zh-Hant", "zh_TW", "繁體中文"),
    "zh-Hans": ("zh-Hans", "zh_CN", "简体中文"),
    "ko":      ("ko",      "ko_KR", "한국어"),
}
JA_LABEL = "日本語"

# 翻訳版の冒頭に出す注記。法令・通知の解説を載せるサイトなので、
# 訳文を根拠に実務判断されないよう、原文が日本語であることを明示する。
NOTICE = {
    "en": "This page is a translation provided for reference. The Japanese original is authoritative for all legal matters.",
    "zh-Hant": "本頁為方便閱覽的翻譯版本。法令相關事項均以日文原文為準。",
    "zh-Hans": "本页为方便阅览的翻译版本。法令相关事项均以日文原文为准。",
    "ko": "본 페이지는 참고용 번역본입니다. 법령에 관한 사항은 모두 일본어 원문이 기준입니다.",
}

PAGES = [
    "index.html",
]

PAGESET = set(PAGES)


def src_path(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def out_path(lang, rel):
    return os.path.join(ROOT, lang, rel.replace("/", os.sep))


def url_of(rel):
    """リポジトリ相対パス -> サイト内パス。BASE は含めない。"""
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    if rel == "index.html":
        return "/"
    return "/" + rel


def href(path, lang="ja"):
    """サイト内パスを、実際にHTMLへ書くルート絶対パスにする。"""
    prefix = "" if lang == "ja" else "/" + lang
    return BASE + prefix + path


def url(path, lang="ja"):
    """サイト内パスを、canonical等に書く完全URLにする。"""
    return SITE + href(path, lang)
