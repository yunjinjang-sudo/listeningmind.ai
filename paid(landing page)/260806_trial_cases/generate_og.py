# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
CENTER_X = W // 2

# ---- colors (matching site palette) ----
INK = (27, 24, 21)
SUB = (114, 108, 102)
PINK = (255, 59, 103)
PINK_DEEP = (225, 42, 84)
GOLD = (201, 161, 90)
WHITE = (255, 255, 255)

# ---- base canvas ----
img = Image.new("RGB", (W, H), WHITE)

# ---- soft blurred gradient blobs (symmetric for a centered layout) ----
blob_layer = Image.new("RGB", (W, H), WHITE)
draw_blob = ImageDraw.Draw(blob_layer)
draw_blob.ellipse((-260, -340, 440, 300), fill=(255, 210, 222))   # pink blob top-left
draw_blob.ellipse((760, -340, 1460, 300), fill=(247, 230, 200))   # gold blob top-right
draw_blob.ellipse((360, 440, 840, 900), fill=(247, 244, 255))     # soft lavender wash bottom-center
blob_layer = blob_layer.filter(ImageFilter.GaussianBlur(90))
img = Image.blend(img, blob_layer, 0.55)

draw = ImageDraw.Draw(img)

FONT_DIR = "."
def font(weight_file, size):
    return ImageFont.truetype(f"{FONT_DIR}/Paperlogy-{weight_file}.ttf", size)

f_headline = font("8ExtraBold", 56)
f_sub = font("5Medium", 27)
f_btn = font("7Bold", 26)

def text_w(d, text, fnt):
    b = d.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0]

def draw_text_center(d, cx, y, text, fnt, fill):
    w = text_w(d, text, fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)

# ---- logo, centered top ----
logo = Image.open("listeningmind-logo.png").convert("RGBA")
logo_h = 50
logo_w = round(logo.width * logo_h / logo.height)
logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
img.paste(logo, (CENTER_X - logo_w // 2, 58), logo)

# ---- headline (centered) ----
y = 178
line_gap = 72
headline_lines = ["검색창 속 소비자 키워드가", "이번 분기 성과를 결정합니다."]
for line in headline_lines:
    draw_text_center(draw, CENTER_X, y, line, f_headline, INK)
    y += line_gap

# ---- subcopy (centered) ----
y += 12
sub_lines = ["브랜드 전략과 연결되는 소비자 고민,", "리스닝마인드에서 발견하세요."]
for line in sub_lines:
    draw_text_center(draw, CENTER_X, y, line, f_sub, SUB)
    y += 40

# ---- CTA button (centered) ----
btn_text = "실제 활용사례 확인하기  →"
pad_x = 34
bw = text_w(draw, btn_text, f_btn) + pad_x * 2
bh = 62
bx = CENTER_X - bw // 2
by = y + 32

# gradient fill for button
btn_grad = Image.new("RGB", (bw, bh), PINK)
for i in range(bw):
    t = i / max(bw - 1, 1)
    r = round(PINK[0] + (PINK_DEEP[0] - PINK[0]) * t)
    g = round(PINK[1] + (PINK_DEEP[1] - PINK[1]) * t)
    b = round(PINK[2] + (PINK_DEEP[2] - PINK[2]) * t)
    ImageDraw.Draw(btn_grad).line([(i, 0), (i, bh)], fill=(r, g, b))

mask = Image.new("L", (bw, bh), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw, bh), radius=16, fill=255)
img.paste(btn_grad, (bx, by), mask)

btn_draw = ImageDraw.Draw(img)
tb = btn_draw.textbbox((0, 0), btn_text, font=f_btn)
tw, th = tb[2] - tb[0], tb[3] - tb[1]
btn_draw.text((bx + (bw - tw) / 2 - tb[0], by + (bh - th) / 2 - tb[1]), btn_text, font=f_btn, fill=WHITE)

img.save("og-image.png", optimize=True)
print("saved", img.size)
