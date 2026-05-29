from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ICONS = ROOT / "icons"

INK = "#1f160f"
SOY = "#4a2717"
CHILI = "#a13b16"
WOK = "#c97822"
CREAM = "#fff6e8"
PAPER = "#fffdfa"
LEAF = "#476a37"
LINE = "#ead7bd"


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/tahomabd.ttf" if bold else "C:/Windows/Fonts/tahoma.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def cover(path, size):
    image = Image.open(path).convert("RGB")
    target_w, target_h = size
    ratio = max(target_w / image.width, target_h / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def paste_rounded(base, image, box, radius):
    image = image.resize((box[2] - box[0], box[3] - box[1]), Image.LANCZOS)
    base.paste(image, box[:2], rounded_mask(image.size, radius))


def text(draw, xy, value, fill, size, bold=False, anchor=None):
    draw.text(xy, value, fill=fill, font=font(size, bold), anchor=anchor)


def draw_card(draw, box, fill=PAPER, outline=LINE, radius=38):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=3)


def build_icon(maskable=False):
    canvas = Image.new("RGB", (1024, 1024), CREAM)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((52, 52, 972, 972), radius=220, fill=PAPER)
    draw.rounded_rectangle((80, 80, 944, 944), radius=190, outline=WOK, width=18)

    photo_box = (126, 126, 898, 680) if not maskable else (178, 178, 846, 662)
    hero = cover(ASSETS / "menu-krapao.png", (photo_box[2] - photo_box[0], photo_box[3] - photo_box[1]))
    paste_rounded(canvas, hero, photo_box, 110)

    draw.rounded_rectangle((160, 710, 864, 884), radius=62, fill=INK)
    text(draw, (512, 754), "RiceBox", PAPER, 88, True, "mm")
    text(draw, (512, 826), "Home Kitchen Plan", "#f7c56b", 38, False, "mm")

    draw.ellipse((736, 122, 900, 286), fill=WOK, outline=PAPER, width=10)
    text(draw, (818, 188), "09", INK, 54, True, "mm")
    text(draw, (818, 236), "15", INK, 54, True, "mm")
    return canvas


def save_icon_set():
    ICONS.mkdir(exist_ok=True)
    base = build_icon(False)
    maskable = build_icon(True)
    base.save(ICONS / "icon-1024.png")
    maskable.resize((512, 512), Image.LANCZOS).save(ICONS / "icon-maskable-512.png")

    for size in [72, 96, 128, 144, 152, 180, 192, 384, 512]:
        base.resize((size, size), Image.LANCZOS).save(ICONS / f"icon-{size}.png")
    base.resize((180, 180), Image.LANCZOS).save(ICONS / "apple-touch-icon.png")


def mobile_screenshot():
    image = Image.new("RGB", (1080, 1920), CREAM)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1080, 180), fill=PAPER)
    text(draw, (64, 70), "Rice Box Online", INK, 54, True)
    text(draw, (64, 128), "Home kitchen operating app", CHILI, 28)
    draw.rounded_rectangle((790, 58, 1018, 122), radius=32, fill=INK)
    text(draw, (904, 91), "Install App", PAPER, 28, True, "mm")

    paste_rounded(image, cover(ASSETS / "hero-rice-box.png", (952, 590)), (64, 220, 1016, 810), 56)
    draw.rounded_rectangle((94, 630, 560, 770), radius=40, fill=PAPER)
    text(draw, (130, 680), "30 boxes first", INK, 44, True)
    text(draw, (130, 730), "09:00 - 15:00 sales window", SOY, 26)

    cards = [
        ("Start lean", "15k+", CHILI),
        ("Recommended", "35k", WOK),
        ("Daily cash", "2k", LEAF),
    ]
    x = 64
    for label, value, color in cards:
        draw_card(draw, (x, 858, x + 298, 1054), radius=38)
        text(draw, (x + 28, 910), label, SOY, 27)
        text(draw, (x + 28, 984), value, color, 66, True)
        x += 327

    text(draw, (64, 1148), "Core menu", INK, 52, True)
    menu_paths = ["menu-krapao.png", "menu-oyster-pork.png", "menu-fried-rice.png"]
    x = 64
    for menu in menu_paths:
        paste_rounded(image, cover(ASSETS / menu, (290, 290)), (x, 1230, x + 290, 1520), 46)
        x += 330

    draw.rounded_rectangle((0, 1772, 1080, 1920), fill=PAPER)
    for i, label in enumerate(["Home", "Time", "Menu", "Buy", "Money"]):
        center = 108 + i * 216
        fill = CHILI if i == 0 else SOY
        text(draw, (center, 1846), label, fill, 30, True, "mm")
    image.save(ASSETS / "app-screenshot-mobile.png")


def desktop_screenshot():
    image = Image.new("RGB", (1920, 1080), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1920, 96), fill=PAPER)
    text(draw, (80, 58), "Rice Box Online", INK, 42, True, "lm")
    for x, label in [(980, "Schedule"), (1120, "Menu Cost"), (1288, "Shopping"), (1450, "Capital"), (1590, "Forecast")]:
        text(draw, (x, 58), label, SOY, 25, True, "lm")
    draw.rounded_rectangle((1710, 30, 1840, 70), radius=22, fill=WOK)
    text(draw, (1775, 50), "Install", INK, 22, True, "mm")

    paste_rounded(image, cover(ASSETS / "hero-rice-box.png", (780, 650)), (1040, 165, 1820, 815), 58)
    text(draw, (90, 230), "Open an online rice shop", INK, 72, True)
    text(draw, (90, 318), "with schedule, cost, menu, capital and forecast ready.", SOY, 36)

    stats = [("Start lean", "15k+"), ("Sell target", "30/day"), ("Hours", "09-15"), ("Platform fee", "32.1%")]
    x = 90
    for label, value in stats:
        draw_card(draw, (x, 430, x + 200, 568), radius=32)
        text(draw, (x + 24, 476), label, SOY, 22)
        text(draw, (x + 24, 532), value, CHILI, 38, True)
        x += 230

    draw.rounded_rectangle((90, 660, 840, 900), radius=46, fill=INK)
    text(draw, (130, 725), "Recommended package", "#f7c56b", 28, True)
    text(draw, (130, 795), "Mid 35,000 THB", PAPER, 54, True)
    text(draw, (130, 850), "Ready kitchen, controlled risk", "#ffe6b0", 28)

    x = 1040
    for menu in ["menu-krapao.png", "menu-oyster-pork.png", "menu-fried-rice.png"]:
        paste_rounded(image, cover(ASSETS / menu, (240, 240)), (x, 865, x + 240, 1050), 36)
        x += 270
    image.save(ASSETS / "app-screenshot-desktop.png")


if __name__ == "__main__":
    save_icon_set()
    mobile_screenshot()
    desktop_screenshot()
    print("Generated PWA icons and app screenshots.")
