"""Build the three static UI screens from public source artwork.

Requires Pillow. Font files stay on the developer's machine; PNGs and RGB565
arrays are checked in so an ordinary ESP-IDF build does not need Python/Pillow.
No QR library, contact payload, cloud data or network access is used.
"""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SKY, INK, GRASS = '#80c8e8', '#25465b', '#82be2d'


def build(font_path):
    def font(size):
        return ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default(size=size)

    def rect(im, x, y, width, height, color):
        ImageDraw.Draw(im).rectangle((x, y, x+width-1, y+height-1), fill=color)

    def text(im, value, x, y, size=12, color=INK, center=False):
        draw = ImageDraw.Draw(im)
        if center:
            x -= draw.textlength(value, font=font(size))/2
        draw.text((round(x), y), value, font=font(size), fill=color)

    def grass(im):
        rect(im, 0, 298, 240, 22, GRASS)
        rect(im, 0, 297, 240, 3, '#a7d93e')
        for x in range(0, 240, 30):
            rect(im, x, 317, 18, 3, '#55951d')

    def character(kind):
        # Original code-drawn substitutes; no desktop-app atlas or logo files.
        art = Image.new('RGBA', (48, 52) if kind == 'blue' else (42, 35) if kind == 'orange' else (38, 38))
        if kind == 'blue':
            blocks = [(22,0,4,6,'#33447e'),(19,0,10,3,'#a5f6ff'),
                      (7,7,34,25,'#4978da'),(10,10,28,18,'#25355d'),
                      (14,15,5,6,'#b5fbff'),(29,15,5,6,'#b5fbff'),
                      (20,24,8,2,'#86dbe6'),(10,32,28,14,'#719af5'),
                      (2,31,6,15,'#4978da'),(40,31,6,15,'#4978da'),
                      (13,46,8,6,'#33447e'),(28,46,8,6,'#33447e'),
                      (20,36,8,5,'#ffe99a')]
        elif kind == 'orange':
            blocks = [(6,2,30,24,'#f2a34a'),(10,6,22,12,'#ffe7b7'),
                      (0,12,5,12,'#cc7542'),(37,12,5,12,'#cc7542'),
                      (13,9,4,5,'#524b57'),(25,9,4,5,'#524b57'),
                      (18,21,6,2,'#cc7542'),(9,27,8,8,'#cc7542'),
                      (25,27,8,8,'#cc7542')]
        else:
            blocks = [(6,12,24,16,'#527cf0'),(10,8,14,8,'#527cf0'),
                      (2,18,8,8,'#527cf0'),(10,25,15,5,'#a8e6ff'),
                      (18,28,6,6,'#527cf0'),(29,17,5,6,'#527cf0'),
                      (33,11,5,8,'#527cf0'),(23,13,3,3,'#fffef6'),
                      (17,2,2,4,'#c9faff'),(21,4,4,2,'#c9faff')]
        for x,y,w,h,c in blocks:
            rect(art,x,y,w,h,c)
        return art

    def sprite(im, kind, x, y):
        art = character(kind)
        im.paste(art, (x, y), art)

    # This source is the non-contact home background, with the reading penguin.
    home = Image.open(ROOT / 'assets/source/home.png').convert('RGB')
    sprite(home, 'blue', 30, 251)
    sprite(home, 'orange', 100, 263)
    sprite(home, 'whale', 176, 265)

    wechat = Image.new('RGB', (240, 320), SKY)
    for x in (68, 164):
        rect(wechat, x, 231, 9, 70, '#6b452e')
        rect(wechat, x+2, 232, 4, 67, '#b88944')
    rect(wechat, 29, 30, 188, 216, '#62aecf')
    rect(wechat, 26, 27, 188, 216, '#6b452e')
    rect(wechat, 29, 30, 182, 210, '#e8bd62')
    rect(wechat, 30, 31, 180, 21, '#ffd985')
    text(wechat, 'WeChat', 120, 32, 15, center=True)
    rect(wechat, 34, 57, 172, 174, '#fffef6')
    # Deliberately empty: even the decorative finder patterns of a QR are absent.
    ImageDraw.Draw(wechat).rectangle((44, 67, 195, 218), outline='#b3baa9', width=2)
    text(wechat, '+', 120, 95, 32, '#a0ac99', center=True)
    text(wechat, 'YOUR QR HERE', 120, 143, 15, center=True)
    text(wechat, 'placeholder', 120, 171, 11, '#7e8d78', center=True)
    sprite(wechat, 'blue', 96, 251)
    sprite(wechat, 'orange', 25, 263)
    sprite(wechat, 'whale', 178, 265)
    grass(wechat)
    text(wechat, 'UP/DOWN  |  Hold OK: Home', 120, 302, 10, '#214019', center=True)

    settings = Image.new('RGB', (240, 320), SKY)
    text(settings, 'Settings', 16, 14, 23)
    for i, name in enumerate(('Display', 'Button', 'Audio', 'Battery', 'BLE', 'Low Power')):
        x, y = 12+(i%2)*112, 52+(i//2)*44
        rect(settings, x+3, y+3, 102, 35, '#25465b')
        rect(settings, x, y, 102, 35, '#fff5e6')
        text(settings, name, x+51, y+10, 13, center=True)
    rect(settings, 15, 191, 214, 57, '#25465b')
    rect(settings, 12, 188, 214, 57, '#fff5e6')
    text(settings, 'Wi-Fi', 22, 194, 13)
    text(settings, 'home  /  phone  /  office', 120, 218, 12, center=True)
    text(settings, 'Static preview', 120, 253, 10, center=True)
    # The original settings mascot is expressed as UI rectangles, with no tests.
    for x,y,w,h,c in [(119,266,2,5,INK),(116,265,8,3,'#ee9b32'),
                        (104,271,32,22,INK),(108,275,24,14,'#b9f3ff'),
                        (112,279,4,5,INK),(124,279,4,5,INK),
                        (112,293,16,4,'#ee9b32'),(109,297,22,7,'#7557d9')]:
        rect(settings,x,y,w,h,c)
    grass(settings)
    text(settings, 'Hold OK: Home', 120, 303, 10, '#214019', center=True)

    images = {'home': home, 'wechat': wechat, 'settings': settings}
    header = ['#pragma once', '#include "lvgl.h"']
    source = ['/* Generated by tools/build_assets.py; RGB565 little-endian. */', '#include "screens.h"']
    (ROOT / 'preview/screens').mkdir(parents=True, exist_ok=True)
    for name, im in images.items():
        # Fresh PNGs carry no source metadata.
        im.save(ROOT / f'preview/screens/{name}.png')
        raw = bytearray()
        for r,g,b in im.getdata():
            v = ((r>>3)<<11)|((g>>2)<<5)|(b>>3)
            raw.extend((v&255,v>>8))
        source.append(f'static const uint8_t data_{name}[] = {{')
        for offset in range(0,len(raw),32):
            source.append('  '+','.join(f'0x{v:02x}' for v in raw[offset:offset+32])+',')
        source.extend(['};', f'const lv_image_dsc_t screen_{name} = {{',
                       '  .header = { .magic = LV_IMAGE_HEADER_MAGIC, .cf = LV_COLOR_FORMAT_RGB565,',
                       '              .w = 240, .h = 320, .stride = 480 },',
                       f'  .data_size = sizeof(data_{name}), .data = data_{name}', '};'])
        header.append(f'extern const lv_image_dsc_t screen_{name};')
    (ROOT / 'assets/screens.c').write_text('\n'.join(source)+'\n',encoding='utf-8')
    (ROOT / 'assets/screens.h').write_text('\n'.join(header)+'\n',encoding='utf-8')
    print('Static screens: home, wechat placeholder, settings (home / phone / office)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', help='Optional local TTF path; the font file is not bundled')
    build(parser.parse_args().font)
