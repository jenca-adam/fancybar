import sys
import time
import json
import os
import cursor
import colored

GRADIENT_TEMPLATE = "\x1b[38;2;{};{};{};48;2;{};{};{}m\u258c\x1b[0m"

os.system("")  # MarchAgainstWindows
_SPINNERS_FILENAME = os.path.join(
    os.path.split(os.path.realpath(__file__))[0], "spinners.json"
)
_COLORS_FILENAME = os.path.join(
    os.path.split(os.path.realpath(__file__))[0], "colors.json"
)

END = "\x1b[0m"
SPINNERS = json.load(open(_SPINNERS_FILENAME))
COLORS = json.load(open(_COLORS_FILENAME))


def _rgb_color(foreground=None, background=None):
    if foreground is None and background is None:
        return ""
    string = "\x1b["
    if foreground is not None:
        string += "38;2;" + ";".join(str(i) for i in foreground)
    if background is not None:
        if string[-1] != "[":
            string += ";"
        string += "48;2;" + ";".join(str(i) for i in background)
    return string + "m"


def _force_rgb(col):
    if type(col) not in (str, tuple):
        raise TypeError("Invalid color type")
    if type(col) == str:
        col = parse_hex(COLORS[col])
    return col


def color_fg(col):
    if col is None:
        return ""
    if type(col) not in (str, tuple):
        raise TypeError("Invalid color type")
    if type(col) == str:
        return colored.fg(col)
    return _rgb_color(col)


def color_bg(col):
    if col is None:
        return ""
    if type(col) not in (str, tuple):
        raise TypeError("Invalid color type")
    if type(col) == str:
        return colored.bg(col)
    return _rgb_color(None, col)


def parse_hex(h):
    if h[0] == "#":
        h = h[1:]
    try:
        col = int(h, 16)
    except ValueError:
        raise ValueError("Invalid HEX string") from None

    l = len(h)
    if l == 6:  # long form , no alpha
        return (col & 0xFF0000) >> 16, (col & 0xFF00) >> 8, (col & 0xFF)
    elif l == 8:  # long form, alpha
        scol = col >> 8
        return (
            (scol & 0xFF0000) >> 16,
            (scol & 0xFF00) >> 8,
            (scol & 0xFF),
            (col & 0xFF) / 255,
            )
    elif l == 3:  # short form, no alpha
        return 17 * ((col & 0xF00) >> 8), 17 * ((col & 0xF0) >> 4), 17 * (col & 0xF)
    elif l == 4:  # short form, alpha
        print(hex(col))
        return (
            17 * ((col & 0xF000) >> 12),
            17 * ((col & 0xF00) >> 8),
            17 * ((col & 0xF0) >> 4),
            17 * (col & 0xF) / 255,
        )
    else:
        raise ValueError("Invalid HEX string")


def _range(start, end, length):
    step = (end - start) / length
    for _ in range(length):
        yield int(start)
        start += step


def _color_range(start_r, start_g, start_b, end_r, end_g, end_b, length):
    range_r = _range(start_r, end_r, length)
    range_g = _range(start_g, end_g, length)
    range_b = _range(start_b, end_b, length)
    for _ in range(length):
        yield next(range_r), next(range_g), next(range_b)


def _generate_gradient_colors(startcol, endcol, length):
    col_r = _color_range(*startcol, *endcol, length)
    cur=startcol
    prev = 0, 0, 0
    i = 0
    curr_frame = ""
    prev_frame = ""
    while True:
        try:
            cur = next(col_r)
        except StopIteration:
            break
        if i % 2 == 1:
            nxt = cur
            cur = prev
            prev_frame = curr_frame = prev_frame + GRADIENT_TEMPLATE.format(*cur,*nxt)

        else:
            nxt = 0, 0, 0
            prev= cur
            curr_frame += GRADIENT_TEMPLATE.format(*cur, *nxt)
        i += 1
        yield curr_frame


def closest_odd(number):
    if number % 2 == 1:
        return number
    return number + 1


def gradient(start, end, length):
    return [
        i + " " * ((length - j) // 2)
        for j, i in enumerate(_generate_gradient_colors(start, end, length + 1))
    ]


class GradientBarType:
    def __init__(self, length, start_color=(255, 0, 0), end_color=(0, 255, 0)):
        self.frames = gradient(
            _force_rgb(start_color), _force_rgb(end_color), closest_odd(length)
        )


def create_bar_type(
    char,
    filler,
    name="?",
    char_fg_color=None,
    char_bg_color=None,
    filler_fg_color=None,
    filler_bg_color=None,
):
    class BarType:
        __qualname__ = name

        def __init__(
            self,
            length,
            char_fg_color=char_fg_color,
            char_bg_color=char_bg_color,
            filler_fg_color=filler_fg_color,
            filler_bg_color=filler_bg_color,
        ):
            self.frames = [
                color_bg(char_bg_color)
                + color_fg(char_fg_color)
                + char * i
                + END
                + color_bg(filler_bg_color)
                + color_fg(filler_fg_color)
                + filler * (length - i)
                + END
                for i in range(length + 1)
            ]

    return BarType


NoBarType = create_bar_type("", "", "NoBar")
MinusBarType = create_bar_type("-", " ", "Default")
PlusMinusBarType = create_bar_type("+", "-", "PlusMinus", "green", None, "red")
ClassicBarType = create_bar_type("#", " ", "Classic")
TrianglesBarType = create_bar_type("\u25b6", "\u25b7", "Triangles")
DotsBarType = create_bar_type(".", " ", "Dots")
FullBarType = create_bar_type(" ", " ", "Full", None, "white")
BARTYPES = {
    "full": FullBarType,
    "plusMinus": PlusMinusBarType,
    "classic": ClassicBarType,
    "triangles": TrianglesBarType,
    "dots": DotsBarType,
    "gradient": GradientBarType,
    "nobar": NoBarType,
    "minus": MinusBarType,
}


class Spinner:
    def __init__(self, name, speed):
        self.speed = speed
        self.frames = SPINNERS[name]["frames"]
        self.frame_count = len(self.frames)
        self._index = -1

    @property
    def next_frame(self):
        self._index += self.speed
        return self.frames[int(self._index) % self.frame_count]


class ProgressBar:
    def __init__(
        self,
        items,
        *,
        length=50,
        item_name="it",
        spinner="line",
        spinner_speed=0.5,
        percentage_fg_color=None,
        percentage_bg_color=None,
        spinner_fg_color=None,
        spinner_bg_color=None,
        bartype="full",
        hide_cursor=False,
        **kwargs,
    ):
        if isinstance(bartype, str):
            bartype = BARTYPES[bartype]
        self.length = length
        self.items = items
        self.running = False
        self.items_done = 0
        self.hide_cursor = hide_cursor
        self.spinner_speed = spinner_speed
        self.start_time = None
        self.list = bartype(length, **kwargs).frames
        self.item_name = item_name
        self.spinner = Spinner(spinner, speed=spinner_speed)
        self.percentage_fg_color = percentage_fg_color
        self.spinner_fg_color = spinner_fg_color
        self.spinner_bg_color = spinner_bg_color
        self.percentage_bg_color = percentage_bg_color
        self.max_spinner_length = max(len(i) for i in self.spinner.frames)

    def stop(self):
        cursor.show()
        self.running = False
        print()

    def start(self):
        if self.hide_cursor:
            cursor.hide()

        self.start_time = time.time()
        self.items_done = 0
        self.running = True

    def __enter__(self):
        self.start()

    def __exit__(self, *foo):
        self.stop()

    def update(self):
        try:
            if not self.running:
                return
            if self.items_done == self.items:
                self.stop()
                return
            self.items_done += 1
            sf = self.spinner.next_frame
            sfpad = (self.max_spinner_length - len(sf)) * " "
            index = int(self.length * (self.items_done / self.items))
            if index < 0:
                index = 0
            image = self.list[index]
            self.percentage = (self.items_done / self.items) * 100
            iterations = self.items_done / (time.time() - self.start_time)
            self.eta = round((self.items - self.items_done) / iterations)
            string = f"\r  {color_fg(self.spinner_fg_color)}{color_bg(self.spinner_bg_color)}{sf}{sfpad}{END}"+\
            f"<{self.items_done}/{self.items}> {color_fg(self.percentage_fg_color)}{color_bg(self.percentage_bg_color)}{self.percentage:.1f}%{END}"+\
            f"|{image}| ({iterations:.2f} {self.item_name}/s) ({self.eta//60:0>2}:{self.eta%60:0>2}eta)     "

            sys.stdout.write(string)
            sys.stdout.flush()
        except:
            cursor.show()
            raise


class SequentialProgressBar(ProgressBar):
    def __init__(self, seq, *args, **kwargs):
        self.iterable = iter(seq)
        self.seq = seq
        super().__init__(len(seq), *args, **kwargs)

    def __iter__(self):
        self.start()
        return self

    def __next__(self):
        self.update()
        try:
            return next(self.iterable)
        except StopIteration:
            self.stop()
            raise


bar = SequentialProgressBar
