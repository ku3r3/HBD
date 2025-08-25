# -*- coding: utf-8 -*-
"""
Kue Ulang Tahun dengan Lilin Bergerak & Api Berkelip (Python + Tkinter)
- Tidak butuh library tambahan selain Python standar.
- Jalankan: python kue_ulang_tahun.py
"""

import tkinter as tk
import random
import math

W, H = 600, 500
CAKE_W, CAKE_H = 360, 200
CAKE_X = (W - CAKE_W) // 2
CAKE_Y = H - CAKE_H - 60
TOP_Y = CAKE_Y + 40  # posisi lapisan atas

class Candle:
    def __init__(self, canvas: tk.Canvas, x_center: int, top_y: int):
        self.cv = canvas
        self.x = x_center
        self.top_y = top_y

        # ukuran lilin
        self.body_w = 22
        self.body_h = 60
        self.wick_h = 10

        # animasi gerak kiri-kanan
        self.base_x = x_center
        self.phase = 0.0
        self.amplitude = 70  # amplitudo gerak
        self.speed = 0.06    # kecepatan gerak

        # objek canvas ids
        self.body_id = None
        self.wax_stripes = []
        self.wick_id = None
        self.flame_ids = []

        # warna
        self.body_color = "#54a0ff"
        self.stripe_color = "#c8dffc"
        self.wick_color = "#2e2e2e"

        self.draw()

    def draw(self):
        # posisi body lilin
        x0 = self.x - self.body_w//2
        x1 = self.x + self.body_w//2
        y1 = self.top_y - 8  # sedikit tertanam di krim
        y0 = y1 - self.body_h
        # body
        if self.body_id is None:
            self.body_id = self.cv.create_rectangle(x0, y0, x1, y1, fill=self.body_color, outline="")
        else:
            self.cv.coords(self.body_id, x0, y0, x1, y1)

        # garis-garis lilin
        # bersihkan lama
        for sid in self.wax_stripes:
            self.cv.delete(sid)
        self.wax_stripes.clear()
        # gambar diagonal stripes
        for i in range(-self.body_h//2, self.body_h, 12):
            x_start = x0 - 10
            y_start = y0 + i
            x_end = x1 + 10
            y_end = y0 + i + 10
            self.wax_stripes.append(self.cv.create_line(x_start, y_start, x_end, y_end,
                                                        fill=self.stripe_color, width=3))

        # sumbu
        wick_x0 = self.x - 1
        wick_x1 = self.x + 1
        wick_y1 = y0 - 2
        wick_y0 = wick_y1 - self.wick_h
        if self.wick_id is None:
            self.wick_id = self.cv.create_rectangle(wick_x0, wick_y0, wick_x1, wick_y1, fill=self.wick_color, outline="")
        else:
            self.cv.coords(self.wick_id, wick_x0, wick_y0, wick_x1, wick_y1)

        # api
        self.draw_flame()

    def draw_flame(self):
        # hapus flame lama
        for fid in self.flame_ids:
            self.cv.delete(fid)
        self.flame_ids.clear()

        # posisi api di atas sumbu
        wick_coords = self.cv.coords(self.wick_id)
        wick_cx = (wick_coords[0] + wick_coords[2]) / 2
        wick_top = min(wick_coords[1], wick_coords[3])

        # variasi berkelip
        flicker = random.uniform(-2.0, 2.0)
        flame_h = random.randint(18, 26)
        flame_w = random.randint(10, 16)

        # warna berlapis (oranye -> kuning -> putih)
        # layer 1 (oranye)
        self.flame_ids.append(self._flame_oval(wick_cx + flicker, wick_top - flame_h, flame_w, flame_h, fill="#ff8c42"))
        # layer 2 (kuning)
        self.flame_ids.append(self._flame_oval(wick_cx + flicker/2, wick_top - int(flame_h*0.8), int(flame_w*0.8), int(flame_h*0.8), fill="#ffd166"))
        # layer 3 (putih)
        self.flame_ids.append(self._flame_oval(wick_cx, wick_top - int(flame_h*0.45), int(flame_w*0.45), int(flame_h*0.45), fill="#ffffff"))

        # efek cahaya (glow) samar
        self.flame_ids.append(self.cv.create_oval(wick_cx-18, wick_top-36, wick_cx+18, wick_top+2, outline="", fill="#fff6b380"))

    def _flame_oval(self, cx, top, w, h, fill):
        # oval vertikal menyerupai tetesan
        return self.cv.create_oval(cx - w/2, top, cx + w/2, top + h, outline="", fill=fill)

    def update(self):
        # gerak sinusoidal kiri-kanan di atas kue
        self.phase += self.speed
        offset = math.sin(self.phase) * self.amplitude
        self.x = self.base_x + offset
        self.draw()


def draw_cake(canvas: tk.Canvas):
    # piring
    plate = canvas.create_oval(CAKE_X-60, CAKE_Y + CAKE_H - 20, CAKE_X + CAKE_W + 60, CAKE_Y + CAKE_H + 30,
                               fill="#e6e6e6", outline="")

    # badan kue (2 layer)
    # layer bawah
    canvas.create_rectangle(CAKE_X, CAKE_Y + 70, CAKE_X + CAKE_W, CAKE_Y + CAKE_H - 10, fill="#f7c6a3", outline="")
    # krim sela layer
    create_drip_cream(canvas, CAKE_X, CAKE_Y + 54, CAKE_W, 24, base_color="#ffe9f2")

    # layer atas
    canvas.create_rectangle(CAKE_X + 30, CAKE_Y + 20, CAKE_X + CAKE_W - 30, CAKE_Y + 70, fill="#f8d5b5", outline="")

    # krim atas dengan tetesan
    create_drip_cream(canvas, CAKE_X + 20, CAKE_Y, CAKE_W - 40, 32, base_color="#fff1f7")

    # dekorasi sprinkle
    add_sprinkles(canvas, CAKE_X + 20, CAKE_Y, CAKE_W - 40, 32)

    # ucapan
    canvas.create_text(W//2, CAKE_Y + CAKE_H + 10, text="Selamat Ulang Tahun!", font=("Segoe UI", 22, "bold"), fill="#444")


def create_drip_cream(cv: tk.Canvas, x, y, w, h, base_color="#fff6fb"):
    # permukaan krim
    cv.create_rectangle(x, y, x + w, y + h, fill=base_color, outline="")
    # tetesan (drips)
    random.seed(7)
    for i in range(x + 10, x + w - 10, 28):
        drip_h = random.randint(10, int(h * 1.2))
        cv.create_oval(i-8, y + h - 6, i+8, y + h + drip_h, fill=base_color, outline="")


def add_sprinkles(cv: tk.Canvas, x, y, w, h):
    colors = ["#ff6b6b", "#4ecdc4", "#ffe66d", "#6c5ce7", "#48dbfb"]
    for _ in range(90):
        cx = random.randint(x+8, x + w - 8)
        cy = random.randint(y+6, y + h - 6)
        angle = random.uniform(0, math.pi)
        r = 6
        dx = r * math.cos(angle)
        dy = r * math.sin(angle)
        cv.create_line(cx-dx, cy-dy, cx+dx, cy+dy, width=2, fill=random.choice(colors))


def main():
    root = tk.Tk()
    root.title("Kue Ulang Tahun - Lilin Bergerak")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=W, height=H, bg="#fafafa", highlightthickness=0)
    canvas.pack()

    # latar confetti halus
    for _ in range(160):
        x = random.randint(0, W)
        y = random.randint(0, H)
        r = random.randint(1, 3)
        canvas.create_oval(x-r, y-r, x+r, y+r, fill="#eaeaea", outline="")

    draw_cake(canvas)

    # satu lilin yang bergerak di permukaan kue
    candle = Candle(canvas, x_center=W//2, top_y=CAKE_Y + 20)

    def tick():
        candle.update()
        root.after(60, tick)  # ~16 fps

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
