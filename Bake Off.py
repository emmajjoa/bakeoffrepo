import math
import os
import random
import sys
import time
import tkinter as tk
from pathlib import Path

W, H = 960, 640
INK = "#42324a"
CREAM = "#fff8ee"
MINT = "#b6e7d4"
PINK = "#f7aec2"
GOLD = "#ffcf79"
ROUNDS = ("Signature", "Technical", "Showstopper")
BAKES = ("Swiss roll", "Custard tarts", "Three-tier celebration cake")
FLAVORS = (
    ("Lemon & blueberry", "#f5d66a", "#6962a5"),
    ("Chocolate & orange", "#c28764", "#ff9f56"),
    ("Raspberry & vanilla", "#f5b1be", "#bf456b"),
    ("Pistachio & rose", "#cbdc93", "#e484a0"),
    ("Blackberry & Earl Grey", "#dbc2bd", "#734974"),
    ("Apple & cinnamon", "#ebc491", "#a76342"),
    ("Rhubarb & custard", "#f5d778", "#d75582"),
    ("Ginger & pear", "#dfae6d", "#829643"),
    ("Espresso & walnut", "#d0a895", "#795448"),
    ("Lime & coconut", "#f7e6b5", "#60ac71"),
    ("Cherry & almond", "#f0c9a7", "#b23f64"),
    ("Honey & lavender", "#f5ca75", "#9673c4"),
    ("Mango & passion fruit", "#f7b974", "#e97743"),
    ("Fig & cardamom", "#e5bb9b", "#8c5174"),
    ("Strawberry & elderflower", "#f2bdcc", "#c6486c"),
    ("Banana & caramel", "#efda88", "#ae6a41"),
)
COLORS = {"Flour": CREAM, "Sugar": "#def2fa", "Eggs": GOLD,
          "Butter": "#f4df88", "Milk": "#ffffff"}


class BakeOff:
    def __init__(self, root):
        self.root = root
        root.title("Bake Off | Under the Tent")
        root.resizable(False, False)
        self.c = tk.Canvas(root, width=W, height=H, highlightthickness=0)
        self.c.pack()
        self.c.bind("<Button-1>", self.click)
        self.c.bind("<Motion>", self.hover)
        self.c.bind("<Leave>", lambda event: self.c.configure(cursor=""))
        self.c.bind("<B1-Motion>", self.drag)
        self.c.bind("<ButtonRelease-1>", self.release)
        self.root.bind("<Escape>", lambda event: self.home())
        self.tick_job = None
        self.flavor_menu = []
        self.flavor_deck = []
        self.home()

    def box(self, x, y, w, h, color, outline=""):
        self.c.create_rectangle(x, y, x+w, y+h, fill=color, outline=outline, width=2)

    def oval(self, x, y, w, h, color, outline=""):
        self.c.create_oval(x, y, x+w, y+h, fill=color, outline=outline, width=2)

    def poly(self, coords, color, outline=""):
        self.c.create_polygon(coords, fill=color, outline=outline, width=2)

    def label(self, x, y, message, size=16, color=INK, bold=False, width=0):
        self.c.create_text(x, y, text=message, fill=color, width=width, justify="center",
                           font=("Georgia" if size >= 26 else "Trebuchet MS",
                                 size, "bold" if bold else "normal"))

    def pill(self, x, y, w, h, color, radius=16, outline=""):
        points = (x+radius,y, x+w-radius,y, x+w,y, x+w,y+radius,
                  x+w,y+h-radius, x+w,y+h, x+w-radius,y+h, x+radius,y+h,
                  x,y+h, x,y+h-radius, x,y+radius, x,y)
        return self.c.create_polygon(points, smooth=True, splinesteps=24, fill=color, outline=outline, width=3)

    def button(self, x, y, w, h, message, action, color=MINT, icon_space=0):
        self.pill(x, y+5, w, h, "#7d4749")
        self.pill(x, y, w, h, color, outline=INK)
        self.pill(x+11, y+5, w-22, 5, "#fff3e7", 3)
        self.label(x+(w+icon_space)/2, y+h/2, message, 13, bold=True,
                   width=w-icon_space-16)
        self.buttons.append((x, y, x+w, y+h, action))

    def hover(self, event):
        active = any(x <= event.x <= right and y <= event.y <= bottom
                     for x, y, right, bottom, _ in self.buttons)
        self.c.configure(cursor="hand2" if active else "")

    def frame(self, title, subtitle):
        self.c.delete("all")
        self.c.configure(cursor="")
        self.buttons = []
        self.box(0, 0, W, H, "#f4ddd4")
        for x in range(0, W, 96):
            self.box(x, 0, 48, 118, "#fff0e2")
        self.box(0, 112, W, 426, "#a3dec9")
        for y in range(153, 530, 39):
            for x in range(-24, W, 58):
                left = x+(29 if y%2 else 0)
                self.pill(left, y, 54, 35, "#b6e7d2" if (x+y)%3 else "#c1eddb", 6)
        self.box(0, 507, W, 32, "#67ab9a", "#4d817a")
        for x in (19, 793):
            self.window(x, 179)
        self.pill(177, 151, 606, 378, "#5c9f92", 29)
        self.pill(177, 147, 606, 375, "#fff9ef", 29, INK)
        for i in range(12):
            x = 8+i*80
            self.oval(x, 98, 79, 29, "#f4ddd4" if i%2 else "#fff0e2")
        self.c.create_line(0, 11, 480, 29, W, 11, smooth=True, fill="#a47988", width=2)
        for i in range(14):
            x = 12+i*70
            y = 12 + 16*(1-abs(x-480)/480)
            self.poly((x,y,x+38,y,x+32,y+24,x+19,y+17,x+6,y+24),
                      ("#e694af", "#edbf6d", "#83c6ad", "#8bbbd6")[i%4])
        self.poly((0,568,160,517,800,517,W,568,W,H,0,H), "#d79069", INK)
        self.poly((0,568,160,517,800,517,W,568), "#ffd5a1", INK)
        self.box(0, 567, W, 7, "#f2ba88")
        for x in (44, 122, 839):
            self.c.create_line(x, 595, x+55, 595, fill="#be795e", width=2, capstyle="round")
        self.counter_props()
        self.box(0, 629, W, 11, "#cc8f81")
        for x in range(14, W, 26):
            self.c.create_line(x, 624, x+12, 624, fill="#f5c9a7", width=2)
        self.label(480, 73, title, 30, bold=True)
        self.label(480, 128, subtitle, 12, "#624558", bold=True)

    def counter_props(self):
        self.oval(23, 520, 114, 31, "#d8936d")
        self.oval(41, 465, 78, 19, "#e9dde6", INK)
        self.pill(41, 471, 78, 62, "#ecacb6", 17, INK)
        self.pill(48, 476, 9, 43, "#f7cdd1", 4)
        self.oval(45, 457, 70, 23, "#fcce87", INK)
        self.pill(54, 492, 52, 23, "#fff2da", 6, INK)
        self.label(80, 504, "SUGAR", 8, bold=True)
        self.oval(825, 520, 113, 31, "#d8936d")
        for x, tilt in ((851,-14),(870,4),(894,17)):
            self.c.create_line(x, 500, x+tilt, 450, fill=INK, width=8, capstyle="round")
            self.c.create_line(x, 500, x+tilt, 450, fill="#c89f72", width=4, capstyle="round")
            self.oval(x+tilt-9, 439, 18, 25, "#eebd7d", INK)
        self.oval(838, 477, 73, 20, "#acd5ed", INK)
        self.pill(839, 485, 72, 48, "#7baaca", 14, INK)
        self.pill(845, 491, 12, 32, "#aed7ef", 6)
        self.oval(871, 498, 15, 15, "#ffdf85", INK)

    def window(self, x, y):
        self.pill(x, y, 148, 310, "#94beb2", 54)
        self.pill(x+5, y+4, 138, 299, "#fff9e9", 51, INK)
        self.pill(x+13, y+13, 122, 275, "#b8def1", 49)
        self.oval(x+82, y+49, 28, 28, "#ffda8b")
        for cx, cy in ((25, 85), (60, 101)):
            self.oval(x+cx, y+cy, 45, 12, "#e5f4f6")
            self.oval(x+cx+8, y+cy-8, 24, 15, "#e5f4f6")
        self.oval(x+13, y+148, 122, 140, "#94cca0")
        self.oval(x+13, y+187, 122, 101, "#b1da9f")
        for i in range(11):
            px, py = x+21+i*9, y+224+(i*17)%38
            self.c.create_line(px, py, px, py+9, fill="#608e72", width=2)
            self.oval(px-3, py-3, 6, 6, ("#fff4bd", "#fdadbd", "#fff9e9")[i%3])
        self.box(x+71, y+15, 6, 274, "#fff9e9")
        self.box(x+11, y+144, 126, 6, "#fff9e9")
        self.pill(x-4, y+282, 156, 18, "#fff9e9", 8)

    def cake(self, x, y, scale=1):
        _, sponge, jam = FLAVORS[getattr(self, "flavor", 0)]
        self.oval(x-106*scale, y-6*scale, 212*scale, 23*scale, "#ead8cf")
        self.oval(x-100*scale, y-11*scale, 200*scale, 22*scale, "#a2c8c6")
        self.oval(x-90*scale, y-10*scale, 180*scale, 14*scale, "#daebe5")
        for tier, w in enumerate((155, 118, 80)):
            left = x-w*scale/2
            top = y-(tier+1)*32*scale
            self.pill(left, top, w*scale, 32*scale, sponge, 6*scale)
            self.pill(left, top, w*scale, 10*scale, jam, 5*scale)
            for i in range(5):
                self.oval(left+(i+.27)*w*scale/5, top+4*scale, 10*scale, (9+i%3)*scale, jam)
                self.oval(left+(i+.55)*w*scale/5, top+21*scale, 4*scale, 4*scale, "#fff0da")
        for dx, dy in ((-17, -101), (0, -108), (17, -101)):
            self.oval(x+(dx-7)*scale, y+dy*scale, 14*scale, 14*scale, jam)
            self.oval(x+(dx-4)*scale, y+(dy+2)*scale, 4*scale, 4*scale, "#fff0da")

    def swiss_roll(self, x, y, scale=1):
        _, sponge, filling = FLAVORS[self.flavor]
        self.oval(x-187*scale, y+35*scale, 406*scale, 27*scale, "#e7d6d0")
        self.pill(x-182*scale, y-48*scale, 375*scale, 97*scale, sponge, 32*scale)
        self.pill(x-177*scale, y-47*scale, 365*scale, 20*scale, "#fff0da", 10*scale)
        self.oval(x+135*scale, y-48*scale, 70*scale, 97*scale, filling)
        self.c.create_arc(x+148*scale, y-30*scale, x+194*scale, y+33*scale,
                          start=5, extent=285, outline=CREAM, style="arc", width=5)

    def tart(self, x, y, scale=1):
        self.oval(x-50*scale, y-33*scale, 100*scale, 76*scale, "#ead8cf")
        self.oval(x-50*scale, y-37*scale, 100*scale, 74*scale, "#cf9256")
        for i in range(14):
            angle = i*math.tau/14
            self.oval(x+(44*math.cos(angle)-6)*scale, y+(30*math.sin(angle)-6)*scale,
                      12*scale, 12*scale, "#e4af66")
        self.oval(x-41*scale, y-27*scale, 82*scale, 54*scale, "#f7c36b")
        self.oval(x-31*scale, y-22*scale, 62*scale, 39*scale, "#ffe49f")

    def face(self, x, y, paul):
        # Large heads, small hands and shoes, and simple silhouettes keep the
        # expressions readable at the same size on the title and judging screens.
        hair = "#9da5b3" if paul else "#43263a"
        shirt = "#4f96b7" if paul else "#c44d7d"
        skin = "#efb489" if paul else "#efbb98"
        self.oval(x-52, y+87, 104, 13, "#e1c8bd")
        for dx in (-22, 5):
            self.pill(x+dx, y+75, 16, 20, "#383444", 6, INK)
            self.oval(x+dx-4, y+88, 24, 10, "#373447", INK)
        self.pill(x-30, y+39, 60, 47, shirt, 14, INK)
        for side in (-1, 1):
            self.poly((x+side*22,y+41,x+side*39,y+52,x+side*43,y+69,
                       x+side*33,y+74,x+side*22,y+59), shirt, INK)
            self.oval(x+side*38-8, y+64, 16, 13, skin, INK)
        self.poly((x-18,y+45,x,y+53,x+18,y+45,x+11,y+60,x,y+56,x-11,y+60),
                  "#d5ebf2" if paul else "#f0c879", INK)
        self.oval(x-2, y+64, 4, 4, "#fff2c8")
        self.oval(x-2, y+73, 4, 4, "#fff2c8")

        if not paul:
            self.oval(x-53, y-44, 106, 110, hair, INK)
            self.pill(x-50, y-13, 22, 71, "#5e3249", 10, INK)
            self.pill(x+33, y-9, 20, 65, "#5e3249", 10, INK)
        self.oval(x-48, y-47, 96, 88, hair, INK)
        self.oval(x-47, y-6, 21, 29, skin, INK)
        self.oval(x+26, y-6, 21, 29, skin, INK)
        self.pill(x-41, y-33, 82, 81, skin, 31, INK)
        if paul:
            self.poly((x-43,y-13,x-43,y-32,x-32,y-42,x-12,y-48,x+15,y-48,
                       x+41,y-36,x+43,y-14,x+28,y-25,x+7,y-30,x-25,y-22), hair, INK)
            self.c.create_line(x-29,y-35,x-14,y-43,x+10,y-40,fill="#e4e7ef",
                               width=4,smooth=True,capstyle="round")
            self.pill(x-29, y+22, 59, 23, "#aab0bb", 12, INK)
        else:
            self.poly((x-43,y-12,x-49,y-30,x-29,y-44,x+6,y-47,x+29,y-38,
                       x+44,y-27,x+46,y-8,x+31,y-21,x+10,y-32,x-8,y-18,
                       x-25,y-14,x-35,y-8), hair, INK)
            self.c.create_line(x-34,y-30,x-21,y-39,x-5,y-41,fill="#885567",
                               width=4,smooth=True,capstyle="round")
            self.oval(x-44, y+16, 10, 13, GOLD, INK)
            self.oval(x+34, y+16, 10, 13, GOLD, INK)

        for dx in (-17, 17):
            self.oval(x+dx-12, y-15, 22, 30, "#fffdf3", INK)
            self.oval(x+dx-2, y-8, 9, 15, "#3778a1" if paul else "#322337")
            self.oval(x+dx+1, y-6, 3, 4, "#fffdf3")
            self.c.create_line(x+dx-9,y-19,x+dx+5,y-22,fill=hair,width=4,capstyle="round")
        self.oval(x-8, y+4, 21, 15, "#eaa57c", INK)
        self.oval(x-34, y+17, 12, 6, "#e98f8b")
        self.oval(x+23, y+17, 12, 6, "#e98f8b")
        if paul:
            self.pill(x-14, y+25, 28, 10, "#653742", 5, INK)
            self.pill(x-10, y+25, 20, 4, "#fff6de", 2)
        else:
            self.oval(x-16,y+22,32,16,"#963f60",INK)
            self.pill(x-12,y+23,24,5,"#fff6de",2)
            self.oval(x-8,y+32,16,3,"#e08394")

    def cancel_timer(self):
        if self.tick_job is not None:
            self.root.after_cancel(self.tick_job)
            self.tick_job = None

    def home(self):
        self.cancel_timer()
        self.phase = "home"
        self.frame("Bake Off: Under the Tent", "A FAN-MADE BAKING GAME")
        self.label(480, 187, "On your marks, get set… bake!", 22, bold=True)
        self.face(267, 324, True)
        self.face(693, 324, False)
        self.cake(480, 415, 1.35)
        self.label(267, 461, "Paul Hollywood", 14, bold=True)
        self.label(693, 461, "Nigella Lawson", 14, bold=True)
        self.label(480, 503, "Cake Week: bake three challenges and earn a shot at Star Baker.", 14)
        self.button(370, 555, 220, 49, "Enter the tent", self.start, PINK)

    def start(self):
        self.r = 0
        self.scores = []
        self.handshakes = 0
        self.choose()

    def rotate_flavors(self):
        if not self.flavor_deck:
            available = [i for i in range(len(FLAVORS)) if i not in self.flavor_menu]
            random.shuffle(available)
            self.flavor_deck = available + self.flavor_menu
        self.flavor_menu = self.flavor_deck[:4]
        self.flavor_deck = self.flavor_deck[4:]

    def choose(self):
        self.rotate_flavors()
        self.phase = "choose"
        self.frame(ROUNDS[self.r], f"CAKE WEEK  /  CHALLENGE {self.r+1} OF 3")
        self.label(480, 197, BAKES[self.r], 30, bold=True)
        note = ("Choose the filling for your signature roll.",
                "The judges set the tart recipe. Choose a flavor for the finishing cream.",
                "Choose the flavor of your three-tier centerpiece.")[self.r]
        self.label(480, 244, note, 14)
        for i, flavor in enumerate(self.flavor_menu):
            name, base, accent = FLAVORS[flavor]
            x = 216 + (i%2)*277
            y = 296 + (i//2)*80
            self.button(x, y, 251, 55, name, lambda flavor=flavor: self.begin(flavor), base, icon_space=40)
            self.oval(x+11, y+25, 20, 13, "#fff6e6", INK)
            self.oval(x+13, y+15, 16, 14, accent, INK)
            self.oval(x+17, y+17, 4, 4, "#fff6e6")
        self.label(480, 565, ("Weigh • Whisk • Bake • Decorate", "Memorize • Whisk • Bake • Decorate",
                         "Stack • Whisk • Bake • Decorate")[self.r], 15, bold=True)

    def begin(self, flavor):
        self.flavor = flavor
        self.steps = []
        self.index = 0
        self.prep_scores = []
        if self.r == 0:
            self.weights = [(name, random.randint(12, 32)*5) for name in ("Flour", "Sugar")]
            self.weigh()
        elif self.r == 1:
            self.order = random.sample(list(COLORS), 5)
            duplicate = random.choice(self.order)
            slots = [i for i in range(6)
                     if duplicate not in self.order[max(0,i-1):i+1]]
            self.order.insert(random.choice(slots), duplicate)
            self.options = random.sample(list(COLORS), len(COLORS))
            self.entered = []
            self.memo(True)
        else:
            self.layers = []
            self.stack()

    def stage(self, phase, instruction):
        self.phase = phase
        self.frame(ROUNDS[self.r], f"{BAKES[self.r]}   •   {FLAVORS[self.flavor][0]}")
        self.label(480, 185, instruction, 16, bold=True, width=566)

    def weigh(self):
        self.stage("weigh", "Hold to pour. Release when the scale reaches the recipe weight.")
        self.ingredient_name, self.grams_target = self.weights[self.index]
        self.grams = 0
        self.pour_started = None
        self.label(480, 242, f"{self.ingredient_name}  /  Target {self.grams_target} g", 19, bold=True)
        self.oval(364, 423, 232, 27, "#e8cdbc")
        self.pill(394, 392, 172, 52, "#93c4ba")
        self.pill(423, 402, 114, 33, "#37594f", 8)
        self.poly((377,298,583,298,560,343,531,374,429,374,400,343), "#bbdce2")
        self.oval(377, 278, 206, 40, "#80b5c3")
        self.button(363, 556, 234, 49, "Hold to pour", self.start_pour, GOLD)
        self.draw_weight()

    def draw_weight(self):
        self.c.delete("grams")
        if self.grams:
            width = min(176, self.grams*.8)
            self.c.create_oval(480-width/2,285,480+width/2,310,
                               fill=COLORS[self.ingredient_name], outline="", tags="grams")
        self.c.create_text(480, 418, text=f"{self.grams} g", fill="#f9f6cb",
                           font=("Consolas", 17, "bold"), tags="grams")

    def start_pour(self):
        if self.pour_started is None:
            self.pour_started = time.monotonic()
            self.pour_tick()

    def pour_tick(self):
        self.tick_job = None
        elapsed = time.monotonic()-self.pour_started
        self.grams = min(250, round(elapsed*70 + 23*elapsed**2))
        self.draw_weight()
        if self.grams >= 250:
            self.finish_pour()
        else:
            self.tick_job = self.root.after(16, self.pour_tick)

    def finish_pour(self):
        self.cancel_timer()
        self.pour_started = None
        error = abs(self.grams-self.grams_target)
        self.prep_scores.append(max(0, 100 - max(0,error-1)*4))
        self.phase = "weighed"
        self.buttons = []
        self.label(480, 482, f"{error} g off  •  {self.prep_scores[-1]} / 100", 14, bold=True)
        self.button(357, 556, 246, 49,
                    "Weigh the sugar" if self.index == 0 else "Start whisking",
                    self.next_weight, MINT)

    def next_weight(self):
        self.index += 1
        if self.index == len(self.weights):
            self.steps.append(round(sum(self.prep_scores)/len(self.weights)))
            self.mix()
        else:
            self.weigh()

    def memo(self, preview=False):
        self.stage("memo_preview" if preview else "memo",
                   "Memorize the order before the recipe card is taken away." if preview
                   else "Rebuild the six-step recipe. One ingredient appears twice.")
        for i in range(len(self.order)):
            x = 202+i*93
            self.pill(x, 274, 91, 108, "#f1e4d9", 17)
            name = self.order[i] if preview else self.entered[i] if i < len(self.entered) else ""
            if name:
                self.oval(x+24, 290, 44, 32, COLORS[name], "#be9795")
            self.label(x+45, 351, name or str(i+1), 14, bold=True)
        if preview:
            self.preview_end = time.monotonic() + 4.6
            self.memo_tick()
        else:
            for i, name in enumerate(self.options):
                self.button(151+i*133, 551, 119, 49, name,
                            lambda name=name: self.recall(name), COLORS[name])

    def memo_tick(self):
        self.tick_job = None
        left = self.preview_end-time.monotonic()
        self.c.delete("memo_time")
        if left <= 0:
            self.memo()
        else:
            self.c.create_text(480, 431, text=f"Recipe card closes in {math.ceil(left)}",
                               fill=INK, font=("Trebuchet MS", 14, "bold"), tags="memo_time")
            self.tick_job = self.root.after(100, self.memo_tick)

    def recall(self, name):
        self.entered.append(name)
        if len(self.entered) == len(self.order):
            self.steps.append(round(100*sum(a == b for a,b in zip(self.entered, self.order))/len(self.order)))
            self.mix()
        else:
            self.memo()

    def stack(self):
        self.stage("stack", "Drop each moving sponge layer directly over the one beneath it.")
        self.oval(323, 459, 314, 31, "#d3e3e2")
        self.pill(356, 452, 248, 24, "#91bcb9", 10)
        for i, center in enumerate(self.layers):
            self.sponge(center, i, 413-i*43)
        base = self.layers[-1] if self.layers else 480
        self.c.create_line(base, 245, base, 455, dash=(4, 5), fill="#8aaea5", width=2)
        self.button(366, 556, 228, 49, "Drop layer", self.drop_layer, PINK)
        self.stack_started = time.monotonic()
        self.stack_offset = random.choice((-math.pi/2, math.pi/2))
        self.stack_tick()

    def sponge(self, x, index, y, tag=None):
        width = 170-30*index
        left = x-width/2
        _, dough, filling = FLAVORS[self.flavor]
        for item in (self.pill(left,y,width,42,dough,12),
                     self.pill(left+5,y+24,width-10,8,filling,4)):
            if tag:
                self.c.addtag_withtag(tag, item)

    def stack_tick(self):
        self.tick_job = None
        speed = 2.1+.52*self.index
        elapsed = time.monotonic()-self.stack_started
        self.layer_x = 480+174*math.sin(elapsed*speed+self.stack_offset)
        self.c.delete("moving_layer")
        self.sponge(self.layer_x, self.index, 365-self.index*43, "moving_layer")
        self.tick_job = self.root.after(16, self.stack_tick)

    def drop_layer(self):
        self.cancel_timer()
        base = self.layers[-1] if self.layers else 480
        error = abs(self.layer_x-base)
        self.prep_scores.append(max(0, round(100-max(0,error-2.2)*2.7)))
        self.layers.append(self.layer_x)
        self.index += 1
        if self.index == 3:
            self.steps.append(round(sum(self.prep_scores)/len(self.prep_scores)))
            self.mix()
        else:
            self.stack()

    def mix(self):
        self.stage("mix", "Hold the mouse button and whisk in circles inside the bowl.")
        self.box(256, 562, 448, 20, CREAM, INK)
        self.angle = None
        self.direction = 0
        self.turn = 0
        self.started = time.monotonic()
        self.whisk_goal = math.tau * (3.45 + self.r*.55)
        self.mix_draw(0)
        self.mix_tick()

    def mix_draw(self, angle):
        self.c.delete("whisk")
        self.c.create_oval(343, 220, 617, 494, fill="#7dbac2", outline=INK, width=3, tags="whisk")
        self.c.create_oval(357, 234, 603, 480, fill=FLAVORS[self.flavor][1],
                           outline=INK, width=2, tags="whisk")
        for i in range(8):
            theta = i*math.tau/8 + self.turn/2
            x, y = 480+82*math.cos(theta), 357+82*math.sin(theta)
            self.c.create_oval(x-4, y-4, x+4, y+4, fill=CREAM, outline="", tags="whisk")
        x, y = 480+77*math.cos(angle), 357+77*math.sin(angle)
        self.c.create_line(x, y, x+41, y-49, fill=INK, width=8, capstyle="round", tags="whisk")
        self.c.create_oval(x-13, y-10, x+13, y+10, outline=INK, width=3, tags="whisk")
        self.c.create_rectangle(258, 564, 258+444*min(1,self.turn/self.whisk_goal), 580,
                                fill="#64b59c", width=0, tags="whisk")

    def mix_tick(self):
        self.tick_job = None
        remaining = 9.5-(time.monotonic()-self.started)
        self.c.delete("clock")
        self.c.create_text(480, 605, text=f"{max(0, math.ceil(remaining))} seconds",
                           font=("Segoe UI", 13, "bold"), fill=INK, tags="clock")
        if remaining <= 0:
            self.finish_mix()
        else:
            self.tick_job = self.root.after(100, self.mix_tick)

    def stir(self, event):
        if self.phase != "mix":
            return
        dx, dy = event.x-480, event.y-357
        if not 26 < math.hypot(dx, dy) < 143:
            self.angle = None
            return
        angle = math.atan2(dy, dx)
        if self.angle is not None:
            delta = (angle-self.angle+math.pi) % math.tau-math.pi
            if .01 < abs(delta) < 1.45:
                if not self.direction:
                    self.direction = math.copysign(1, delta)
                self.turn = max(0, self.turn + delta*self.direction)
        self.angle = angle
        self.mix_draw(angle)
        if self.turn >= self.whisk_goal:
            self.finish_mix()

    def release(self, _event):
        self.angle = None
        if self.phase == "weigh" and self.pour_started is not None:
            self.finish_pour()

    def finish_mix(self):
        self.cancel_timer()
        self.steps.append(round(min(1, self.turn/self.whisk_goal)*100))
        self.stage("oven", "Take your bake out when the needle reaches the green zone.")
        self.pill(289, 231, 382, 237, "#547c95", 27, INK)
        self.pill(301, 239, 358, 37, "#88bdd1", 15, INK)
        for x in (324, 357, 636):
            self.oval(x-9, 248, 18, 16, GOLD if x == 636 else CREAM, INK)
        self.pill(311, 280, 338, 155, "#a96c57", 22, INK)
        self.pill(320, 290, 320, 137, "#ffe4a0", 18, INK)
        if self.r == 0:
            self.swiss_roll(470, 363, .62)
        elif self.r == 1:
            for x in (390, 480, 570):
                self.tart(x, 363, .77)
        else:
            self.cake(480, 412, .90)
        self.box(254, 492, 452, 24, CREAM, INK)
        self.oven_time = 4.0-.34*self.r
        self.target = random.uniform(.65, .82)
        self.zone = .036-.006*self.r
        self.box(255+450*(self.target-self.zone), 493, 900*self.zone, 22, "#70bf99")
        self.button(374, 556, 212, 48, "Take it out", self.finish_oven, GOLD)
        self.started = time.monotonic()
        self.oven_tick()

    def oven_tick(self):
        self.tick_job = None
        self.needle = min(1, (time.monotonic()-self.started)/self.oven_time)
        self.c.delete("needle")
        x = 255+450*self.needle
        self.c.create_line(x, 484, x, 525, width=4, fill=INK, tags="needle")
        if self.needle >= 1:
            self.finish_oven()
        else:
            self.tick_job = self.root.after(16, self.oven_tick)

    def finish_oven(self):
        self.cancel_timer()
        position = min(1, (time.monotonic()-self.started)/self.oven_time)
        self.needle = position
        error = max(0, abs(position-self.target)-self.zone)
        self.steps.append(max(0, round(100-error*445)))
        self.decorate()

    def decorate(self):
        instruction = ("Place a berry on each marked spot.",
                       "Pipe a cream rosette onto each tart.",
                       "Place a decoration on every tier.")[self.r]
        self.stage("decorate", instruction + " Click or drag across the spots.")
        if self.r == 0:
            self.swiss_roll(480, 385)
            points = [(332+i*61, 356+(i%2)*42) for i in range(5)]
        elif self.r == 1:
            points = [(x,y) for y in (302,408) for x in (351,480,609)]
            for x,y in points:
                self.tart(x, y)
        else:
            self.cake(480, 464, 2.05)
            points = [(450,282),(510,282),(413,344),(480,344),(547,344),
                      (370,410),(444,410),(516,410),(590,410)]
        self.targets = points
        self.total_targets = len(points)
        self.misses = 0
        self.radius = 17-2*self.r
        for i,(x,y) in enumerate(points):
            self.c.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius,
                               outline=INK, dash=(3, 4), width=2, tags=f"spot{i}")
        self.button(370, 553, 220, 42, "Present your bake", self.finish_decor, PINK)
        self.decorate_end = time.monotonic() + (4.5+.6*self.r)
        self.decor_tick()

    def decor_tick(self):
        self.tick_job = None
        remaining = self.decorate_end-time.monotonic()
        self.c.delete("decor_time")
        if remaining <= 0:
            self.finish_decor()
        else:
            self.c.create_text(480, 612, text=f"{remaining:.1f} s left", fill=INK,
                               font=("Trebuchet MS", 12, "bold"), tags="decor_time")
            self.tick_job = self.root.after(60, self.decor_tick)

    def place(self, x, y, count_miss=True):
        if not (280 <= x <= 685 and 235 <= y <= 480):
            return
        for i, spot in enumerate(self.targets):
            if spot and math.hypot(x-spot[0], y-spot[1]) <= self.radius:
                self.targets[i] = None
                self.c.delete(f"spot{i}")
                accent = FLAVORS[self.flavor][2]
                for j in range(5):
                    a = j*math.tau/5
                    self.oval(x+7*math.cos(a)-6, y+7*math.sin(a)-6, 12, 12, accent, INK)
                self.oval(x-4, y-4, 8, 8, CREAM)
                return
        if count_miss:
            self.misses += 1

    def drag(self, event):
        if self.phase == "decorate":
            self.place(event.x, event.y, count_miss=False)
        elif self.phase == "mix":
            self.stir(event)

    def finish_decor(self):
        self.cancel_timer()
        filled = self.targets.count(None)
        self.steps.append(max(0, round(100*filled/self.total_targets)-5*self.misses))
        score = round(sum(self.steps)/len(self.steps))
        self.scores.append(score)
        self.phase = "review"
        self.frame(ROUNDS[self.r] + " judging", f"{BAKES[self.r]}   •   {FLAVORS[self.flavor][0]}")
        self.face(255, 251, True)
        self.face(705, 251, False)
        self.label(480, 279, f"{score} / 100", 38, bold=True)
        self.label(255, 370, "Paul Hollywood", 14, bold=True)
        self.label(705, 370, "Nigella Lawson", 14, bold=True)
        paul, nigella = self.critiques()
        self.quote(255, 388, paul, "#dceef1")
        self.quote(705, 388, nigella, "#f7e3ea")
        for i, name in enumerate((("Weighing", "Memory", "Stacking")[self.r], "Whisk", "Oven", "Finish")):
            self.label(276+i*136, 499, f"{name}  {self.steps[i]}", 12, bold=True)
        if sum(self.steps) >= 396 and min(self.steps) >= 98:
            self.label(480, 365, "Paul is offering you\nhis handshake!", 13, "#92542c", bold=True)
            self.button(361, 554, 238, 50, "Accept the handshake", self.handshake, GOLD)
        else:
            self.continue_judging()

    def quote(self, x, y, message, color):
        self.poly((x-14,y+3,x-8,y-9,x+10,y+5), color, INK)
        self.pill(x-114,y,228,84,color,15,INK)
        self.label(x,y+42,message,12,width=210)

    def critiques(self):
        prep, whisk, oven, finish = self.steps
        if oven < 70 and self.needle < self.target:
            paul = ("That needed more time. The oven barely got to know it.",
                    "You've got a lovely bake. It's still in the future.")
        elif oven < 70:
            paul = ("It's a bake, not an archaeological find.",
                    "You can take it out now. It's already filed for retirement.")
        elif prep < 65:
            paul = ("That recipe has had a very eventful afternoon.",
                    "I can see you took liberties. Several of them are still at large.")
        elif whisk < 70:
            paul = ("There are lumps in there with their own postcode.",
                    "Give that whisk a proper job next time. It looks bored.")
        elif oven >= 98 and prep >= 95 and whisk >= 95:
            paul = ("That's annoyingly good. I had a whole speech ready.",
                    "I was looking for a fault. Give me another minute.")
        else:
            paul = ("I'd have another slice. Strictly for research.",
                    "Good bake. Don't look so surprised. That's my job.")
        if finish >= 98:
            nigella = ("I was going to cut a modest slice. That was a brief phase.",
                       "I'd eat the decoration first, then deny it with great conviction.",
                       "I could gaze at that all evening. Obviously I'd rather eat it.")
        elif finish < 65:
            nigella = ("It's got the charm of a cake decorated in the back of a taxi.",
                       "The piping's gone rogue. I admire its independence.",
                       "A little wild around the edges. We've all had evenings like that.")
        else:
            nigella = ("I'd serve it by candlelight. A little mystery is delicious.",
                       "It's gloriously homemade. I'd call that a compliment before Paul gets a go.")
        return random.choice(paul), random.choice(nigella)

    def continue_judging(self):
        self.button(361, 554, 238, 50, "Next challenge" if self.r < 2 else "See Cake Week results",
                    self.next_round, MINT)

    def handshake(self):
        self.phase = "handshake"
        self.handshakes += 1
        self.frame("Hollywood Handshake", f"{ROUNDS[self.r]}   •   {BAKES[self.r]}")
        self.face(480, 222, True)
        self.pill(317, 378, 124, 51, "#6497ad", 12, INK)
        self.pill(519, 378, 124, 51, "#a7416c", 12, INK)
        self.poly((420,382,452,375,478,386,507,373,540,383,540,417,503,419,
                   488,438,457,423,420,422), "#efb890", INK)
        self.c.create_line(452,375,480,403,496,397,512,412, fill=INK, width=3, smooth=True)
        for x,y in ((368,353),(587,352),(400,452),(561,456)):
            self.poly((x-13,y,x-4,y-3,x,y-14,x+4,y-3,x+13,y,x+4,y+3,x,y+14,x-4,y+3), GOLD, INK)
        self.label(480, 485, "Nigella: Goodness. He usually makes them wait until Christmas.", 14, bold=True)
        self.continue_judging()

    def next_round(self):
        if self.r == 2:
            self.finale()
        else:
            self.r += 1
            self.choose()

    def finale(self):
        self.phase = "finale"
        average = round(sum(self.scores)/len(self.scores))
        star_baker = average >= 90
        self.frame("Star Baker!" if star_baker else "Cake Week complete", "FINAL SCORECARD")
        self.face(271, 244, True)
        self.face(689, 244, False)
        if star_baker:
            for x, y in ((391, 240), (480, 196), (569, 240)):
                points = []
                for i in range(10):
                    angle = i*math.tau/10-math.pi/2
                    radius = (24 if i%2 == 0 else 11) if x == 480 else (13 if i%2 == 0 else 6)
                    points.extend((x+radius*math.cos(angle), y+radius*math.sin(angle)))
                self.poly(points, GOLD, INK)
        self.cake(480, 321, .9)
        comment = ("Paul: Somewhere, a cake stand is feeling very smug." if star_baker else
                   "Nigella: The judging's over. Now we can have a proper slice.")
        self.label(480, 357, comment, 13, bold=True)
        for i, (name, score) in enumerate(zip(ROUNDS, self.scores)):
            x = 306+174*i
            self.pill(x-78, 382, 156, 63, (PINK, MINT, GOLD)[i], 14, INK)
            self.label(x, 400, name, 11, bold=True)
            self.label(x, 424, str(score), 15, bold=True)
        self.label(480, 467, f"Overall {average} / 100   •   Star Baker at 90", 14, bold=True)
        if self.handshakes:
            self.label(480, 497, f"Hollywood handshakes earned: {self.handshakes}", 12, bold=True)
        self.button(238, 555, 220, 49, "Back to title", self.home)
        self.button(502, 555, 220, 49, "Bake Cake Week again", self.start, PINK)

    def click(self, event):
        for x, y, right, bottom, action in self.buttons:
            if x <= event.x <= right and y <= event.y <= bottom:
                action()
                return
        if self.phase == "decorate":
            self.place(event.x, event.y)


def smoke_test(game):
    from types import SimpleNamespace

    for high_score in (True, False):
        game.start()
        for r in range(3):
            game.begin(r)
            if r == 0:
                for _ in range(2):
                    game.start_pour()
                    game.grams = game.grams_target if high_score else 250
                    game.release(None)
                    assert game.phase == "weighed"
                    game.next_weight()
            elif r == 1:
                game.cancel_timer()
                game.preview_end = time.monotonic()-1
                game.memo_tick()
                wrong = dict(zip(COLORS, list(COLORS)[1:]+list(COLORS)[:1]))
                picks = game.order if high_score else [wrong[name] for name in game.order]
                for name in picks:
                    game.recall(name)
            else:
                for _ in range(3):
                    game.layer_x = 480 if high_score else (655 if game.index % 2 == 0 else 305)
                    game.drop_layer()
            assert game.phase == "mix"
            if high_score:
                for i in range(310):
                    angle = i*math.tau/48
                    game.stir(SimpleNamespace(x=480+80*math.cos(angle), y=357+80*math.sin(angle)))
                    if game.phase == "oven":
                        break
                assert game.phase == "oven"
                game.started = time.monotonic()-game.target*game.oven_time
            else:
                game.cancel_timer()
                game.started = time.monotonic()-20
                game.mix_tick()
            game.finish_oven()
            if high_score:
                for x, y in game.targets.copy():
                    game.place(x, y)
            game.cancel_timer()
            game.decorate_end = time.monotonic()-1
            game.decor_tick()
            assert game.phase == "review"
            if high_score:
                assert game.steps == [100]*4, game.steps
            else:
                assert max(game.steps) <= 40, game.steps
            if high_score:
                assert game.buttons[-1][-1] == game.handshake
                game.buttons[-1][-1]()
                assert game.handshakes == r+1
            else:
                assert game.buttons[-1][-1] != game.handshake
            last_menu = set(game.flavor_menu)
            game.next_round()
            if r < 2:
                assert not last_menu.intersection(game.flavor_menu)
        assert game.phase == "finale"
        expected_title = "Star Baker!" if high_score else "Cake Week complete"
        assert any(game.c.itemcget(item, "text") == expected_title
                   for item in game.c.find_all() if game.c.type(item) == "text")
        game.buttons[-1][-1]()
        assert game.phase == "choose" and game.r == 0 and not game.scores and not game.handshakes
    game.flavor_deck = [i for i, flavor in enumerate(FLAVORS) if flavor[0].startswith("Strawberry")]
    game.choose()
    name_item, = [item for item in game.c.find_all() if game.c.type(item) == "text"
                  and game.c.itemcget(item, "text").startswith("Strawberry")]
    left, top, right, bottom = game.c.bbox(name_item)
    assert left > 249 and right < 467 and top > 296 and bottom < 351
    print("Verified both Cake Week endings, replay, handshakes, and Strawberry label spacing.")


if __name__ == "__main__":
    tcl = Path(__file__).resolve().parent / "tcl"
    if tcl.is_dir():
        os.environ.setdefault("TCL_LIBRARY", str(tcl / "tcl8.6"))
        os.environ.setdefault("TK_LIBRARY", str(tcl / "tk8.6"))
    root = tk.Tk()
    game = BakeOff(root)
    if "--smoke-test" in sys.argv:
        root.withdraw()
        smoke_test(game)
        root.destroy()
    else:
        root.mainloop()
