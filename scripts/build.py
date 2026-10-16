#!/usr/bin/env python3
"""src/*.body.html + テンプレート片 → ルートのHTMLを生成する。"""
import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://shomit.biz"

PAGES = {
    "index": {
        "title": "株式会社SHOMIT ｜ 広告で、事業を動かす。",
        "desc": "株式会社SHOMITは、Web広告運用・LP制作・SEO・動画制作・AI活用を一体で提供する渋谷の広告代理店です。成果に直結する広告を、運用・制作・計測をひとつのチームで設計します。",
        "header_class": " on-dark", "cur": "HOME", "url": "/", "robots": "",
    },
    "service": {
        "title": "事業内容 ｜ 株式会社SHOMIT",
        "desc": "Web広告運用、LP・Webサイト制作、SEO・コンテンツ制作、動画・クリエイティブ制作、AI活用・業務自動化。SHOMITの事業内容をご紹介します。",
        "header_class": "", "cur": "SERVICE", "url": "/service.html", "robots": "",
    },
    "company": {
        "title": "会社概要 ｜ 株式会社SHOMIT",
        "desc": "株式会社SHOMITの会社概要・代表挨拶。東京都渋谷区道玄坂の広告代理店。代表取締役 木下翔大。",
        "header_class": "", "cur": "COMPANY", "url": "/company.html", "robots": "",
    },
    "contact": {
        "title": "お問い合わせ ｜ 株式会社SHOMIT",
        "desc": "Web広告・LP制作・SEO・動画・AI活用のご相談は株式会社SHOMITへ。お問い合わせフォームよりご連絡ください。",
        "header_class": "", "cur": "CONTACT", "url": "/contact.html", "robots": "",
    },
    "404": {
        "title": "ページが見つかりません ｜ 株式会社SHOMIT",
        "desc": "お探しのページは見つかりませんでした。",
        "header_class": "", "cur": "", "url": "/404.html", "robots": '<meta name="robots" content="noindex">\n',
    },
}

ORG_JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"株式会社SHOMIT","alternateName":"SHOMIT Inc.","url":"https://shomit.biz/","logo":"https://shomit.biz/assets/img/logo-mark.svg","founder":{"@type":"Person","name":"木下 翔大"},"foundingDate":"2022-09-30","address":{"@type":"PostalAddress","postalCode":"150-0043","addressRegion":"東京都","addressLocality":"渋谷区","streetAddress":"道玄坂1丁目10番8号 渋谷道玄坂東急ビル2F-C","addressCountry":"JP"}}
</script>
"""


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def build(name, meta):
    head = read("_head.tpl")
    header = read("_header.tpl").replace("__CLASS__", meta["header_class"])
    for key in ("HOME", "SERVICE", "COMPANY", "CONTACT"):
        header = header.replace(f"__CUR_{key}__", ' aria-current="page"' if meta["cur"] == key else "")
    body = read(f"src/{name}.body.html")
    footer = read("_footer.tpl")
    html = (
        "<!DOCTYPE html>\n<html lang=\"ja\">\n<head>\n<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        f"<title>{meta['title']}</title>\n<meta name=\"description\" content=\"{meta['desc']}\">\n"
        f"{meta['robots']}<link rel=\"canonical\" href=\"{SITE}{meta['url']}\">\n"
        f"<meta property=\"og:title\" content=\"{meta['title']}\">\n<meta property=\"og:description\" content=\"{meta['desc']}\">\n"
        f"<meta property=\"og:url\" content=\"{SITE}{meta['url']}\">\n"
        + head + (ORG_JSONLD if name == "index" else "")
        + "</head>\n<body>\n\n" + header + "\n" + body + "\n" + footer
    )
    out = os.path.join(ROOT, f"{name}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"built {name}.html ({len(html)//1024} KB)")


if __name__ == "__main__":
    for n, m in PAGES.items():
        build(n, m)
