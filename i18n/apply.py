# -*- coding: utf-8 -*-
"""添字で書いた訳文を、原文キーの翻訳メモリに書き込む。

原本のHTMLは本文の途中に改行やインデントが入るため、原文キーを手で書き写すと
取り違えやすい。訳文は ja.json の並び順に対する添字で渡し、キーの対応付けは
ここで機械的に行う。

  python i18n/apply.py <訳文JSON>

  訳文JSON: {"12": {"en": "...", "zh-Hant": "...", "zh-Hans": "...", "ko": "..."}, ...}
"""
import io, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

TR = os.path.join(config.STRINGS, "_tr")


def main():
    src = json.load(io.open(os.path.join(config.STRINGS, "ja.json"), encoding="utf-8"))
    entries = src["entries"]
    data = json.load(io.open(sys.argv[1], encoding="utf-8"))

    for lang in config.LANGS:
        p = os.path.join(TR, lang + ".json")
        memory = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else {}
        n = 0
        for k, v in data.items():
            t = v.get(lang)
            if isinstance(t, str) and t.strip():
                memory[entries[int(k)]["ja"]] = t
                n += 1
        io.open(p, "w", encoding="utf-8").write(
            json.dumps(memory, ensure_ascii=False, indent=1))
        print("%-8s 追加/更新 %d 件  メモリ計 %d 件" % (lang, n, len(memory)))


if __name__ == "__main__":
    main()
