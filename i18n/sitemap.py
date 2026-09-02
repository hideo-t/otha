# -*- coding: utf-8 -*-
"""sitemap.xml を多言語対応で書き出す。

ページ数が少ないので既存ファイルは読まず、毎回すべて生成する。
どの言語のURLからも全言語を辿れるよう xhtml:link の相互参照を全件に付ける。

  python i18n/sitemap.py
"""
import io, os, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

SITEMAP = os.path.join(config.ROOT, "sitemap.xml")


def alternates(path):
    out = ['    <xhtml:link rel="alternate" hreflang="ja" href="%s"/>' % config.url(path, "ja")]
    for code in config.LANGS:
        out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                   % (config.LANGS[code][0], config.url(path, code)))
    out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
               % config.url(path, "ja"))
    return out


def main():
    today = datetime.date.today().isoformat()
    body = []
    for rel in config.PAGES:
        path = config.url_of(rel)
        for lang in ["ja"] + list(config.LANGS):
            body += ["  <url>",
                     "    <loc>%s</loc>" % config.url(path, lang),
                     "    <lastmod>%s</lastmod>" % today]
            body += alternates(path)
            body.append("  </url>")

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">'] + body + ["</urlset>", ""]
    io.open(SITEMAP, "w", encoding="utf-8", newline="").write("\n".join(out))
    print("sitemap.xml: 全%d URL（%d ページ × %d 言語）"
          % (len(config.PAGES) * (len(config.LANGS) + 1),
             len(config.PAGES), len(config.LANGS) + 1))


if __name__ == "__main__":
    main()
