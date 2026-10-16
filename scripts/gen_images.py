#!/usr/bin/env python3
"""SHOMIT HP 用 画像生成（gpt-image-2 / low quality）。
   実行: op run --env-file=scripts/.env -- python3 scripts/gen_images.py
"""
import base64, json, os, subprocess, sys, urllib.request, urllib.error

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("ERROR: OPENAI_API_KEY 未設定", file=sys.stderr); sys.exit(1)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT_DIR, exist_ok=True)
MODEL = os.environ.get("IMG_MODEL", "gpt-image-2")
ENDPOINT = "https://api.openai.com/v1/images/generations"

BASE = ("Cinematic editorial photography, deep navy and electric blue color palette, "
        "soft natural light, shallow depth of field, premium modern agency mood, "
        "clean composition, no text, no logos, no watermark, no people. ")

JOBS = [
    ("hero", "1536x1024",
     BASE + "Tokyo Shibuya-like city street at blue hour seen from above, long exposure light trails of traffic, "
            "glass buildings reflecting blue light, wide cinematic shot."),
    ("intro", "1024x1536",
     BASE + "Minimal modern office desk by a large window overlooking a city at dusk, laptop showing a blurred "
            "analytics dashboard, notebook and coffee, vertical composition."),
    ("ads", "1536x1024",
     BASE + "Abstract 3D visualization of a rising growth chart made of glowing glass bars and light particles, "
            "dark navy background, elegant and precise."),
    ("web", "1536x1024",
     BASE + "Clean designer workspace with a large monitor displaying a minimal landing page wireframe, "
            "wooden desk, soft daylight, slightly angled view."),
    ("creative", "1536x1024",
     BASE + "Small video production studio: camera on tripod, softbox lights, monitor with color grading, "
            "storyboard sketches on a wall, moody blue tones."),
    ("ai", "1536x1024",
     BASE + "Abstract network of glowing nodes and thin light threads forming flowing structures, "
            "dark navy background, representing AI and automation, elegant."),
    ("office", "1024x1536",
     BASE + "Modern glass office building facade in Shibuya at dusk, reflections of city lights, "
            "looking up, vertical composition."),
]


def generate(name, size, prompt):
    payload = {"model": MODEL, "prompt": prompt, "size": size, "quality": "low", "n": 1}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        print(f"[{name}] HTTP {e.code}: {e.read().decode()[:300]}", file=sys.stderr); return False
    b64 = data["data"][0].get("b64_json")
    if not b64:
        print(f"[{name}] no image data", file=sys.stderr); return False
    png = os.path.join(OUT_DIR, f"{name}.png")
    jpg = os.path.join(OUT_DIR, f"{name}.jpg")
    with open(png, "wb") as f:
        f.write(base64.b64decode(b64))
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", png, "--out", jpg],
                   check=True, capture_output=True)
    os.remove(png)
    print(f"[{name}] ok -> {os.path.getsize(jpg)//1024} KB")
    return True


if __name__ == "__main__":
    only = set(sys.argv[1:])
    ok = all(generate(n, s, p) for n, s, p in JOBS if not only or n in only)
    sys.exit(0 if ok else 1)
