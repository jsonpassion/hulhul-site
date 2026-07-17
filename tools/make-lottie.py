#!/usr/bin/env python3
"""훌훌 사이트 Lottie 생성기 — assets/lottie/*.json 재생성 (10종).
실행: 리포 루트에서 `python3 tools/make-lottie.py`
팔레트는 앱/아이콘과 동일: 산들바람 · 먹빛 · 아지랑이 · 솜구름.

1. how-register    ① 얼굴 등록: 원형 슬롯에 얼굴이 담기고 1~3장으로 늘어남
2. how-scan        ② 모두 찾기: 사진 그리드를 스캔 바가 훑고 매칭 셀이 켜짐
3. how-review      ③ 직접 고르기: 체크가 그려지고, 아닌 사진은 빠짐
4. how-sweep       ④ 훌훌 털기: 고른 사진들이 바람에 날아감
5. feature-seal    봉인하기: 사진 위로 자물쇠가 내려와 잠김
6. feature-privacy 온디바이스: 아이폰 안에서만 도는 얼굴 점
7. feature-shared  함께 쓰는 사진 보호: 두 사람 앞에 방패가 서고 체크
8. feature-multiface 여러 얼굴 선택: 셋 중 하나를 골라 체크
9. feature-period  기간 선택: 칩이 골라지고 예상 시간이 도는 시계
10. feature-live   실시간 발견: 진행 바가 차며 썸네일이 쌓임

히어로는 시네마틱 영상(assets/video/hero-feather.mp4)이 대신한다.
"""
import json
import os

W = H = 300
FR = 30

BREEZE = [0.239, 0.584, 0.780, 1]
SOFT = [0.435, 0.733, 0.902, 1]
INK = [0.133, 0.188, 0.231, 1]
HAZE = [0.486, 0.545, 0.588, 1]
CLOUD = [0.969, 0.980, 0.988, 1]
LINE = [0.890, 0.922, 0.945, 1]
WHITE = [1, 1, 1, 1]


def static(v):
    return {"a": 0, "k": v}


def kfs(frames):
    """frames: (t, value[, 'h']). value는 스칼라 또는 리스트."""
    keys = []
    for i, f in enumerate(frames):
        t, v = f[0], f[1]
        hold = len(f) > 2
        s = v if isinstance(v, list) else [v]
        k = {"t": t, "s": s}
        if hold:
            k["h"] = 1
        elif i < len(frames) - 1:
            dim = len(s)
            k["i"] = {"x": [0.42] * dim, "y": [1] * dim}
            k["o"] = {"x": [0.58] * dim, "y": [0] * dim}
        keys.append(k)
    return {"a": 1, "k": keys}


def transform():
    return {"ty": "tr", "p": static([0, 0]), "a": static([0, 0]),
            "s": static([100, 100]), "r": static(0), "o": static(100)}


def fill_group(shape, color, extras=None):
    items = [shape] + (extras or []) + [
        {"ty": "fl", "c": color if isinstance(color, dict) else static(color), "o": static(100)},
        transform()]
    return {"ty": "gr", "it": items}


def stroke_group(shape, color, width, extras=None):
    items = [shape] + (extras or []) + [
        {"ty": "st", "c": static(color), "o": static(100),
         "w": static(width), "lc": 2, "lj": 2},
        transform()]
    return {"ty": "gr", "it": items}


def ellipse(w, h, p=(0, 0)):
    return {"ty": "el", "d": 1, "s": static([w, h]), "p": static(list(p))}


def rect(w, h, r=0, p=(0, 0)):
    return {"ty": "rc", "d": 1, "s": static([w, h]), "p": static(list(p)), "r": static(r)}


def path(points, closed=False, i_tan=None, o_tan=None):
    n = len(points)
    return {"ty": "sh", "d": 1, "ks": static({
        "i": i_tan or [[0, 0]] * n,
        "o": o_tan or [[0, 0]] * n,
        "v": points, "c": closed})}


def layer(name, shapes, ind, op, pos=None, o=None, s=None, a=None, r=None):
    return {
        "ddd": 0, "ind": ind, "ty": 4, "nm": name, "sr": 1,
        "ks": {
            "o": o if isinstance(o, dict) else static(100 if o is None else o),
            "r": r if isinstance(r, dict) else static(r or 0),
            "p": pos if isinstance(pos, dict) else static((pos or [150, 150]) + [0]),
            "a": static((a or [0, 0]) + [0]),
            "s": s if isinstance(s, dict) else static((s or [100, 100]) + [100]),
        },
        "ao": 0, "shapes": shapes, "ip": 0, "op": op, "st": 0,
    }


def doc(name, layers, op):
    return {"v": "5.7.4", "fr": FR, "ip": 0, "op": op, "w": W, "h": H,
            "nm": name, "ddd": 0, "assets": [], "layers": layers}


def feather_shapes(scale=1.0):
    """깃털 마크 (아이콘과 동일 지오메트리): 잎꼴 + 밝은 깃대 + 깃촉."""
    s = scale
    body = path(
        [[0, -60 * s], [20 * s, 0], [0, 60 * s], [-20 * s, 0]], closed=True,
        i_tan=[[0, 0], [0, -33 * s], [0, 0], [0, 33 * s]],
        o_tan=[[0, 0], [0, 33 * s], [0, 0], [0, -33 * s]])
    # Lottie는 배열 앞 항목이 위에 그려진다 — 깃대가 몸통 위로
    return [
        stroke_group(path([[0, -45 * s], [0, 42 * s]]), CLOUD, 5 * s),
        stroke_group(path([[0, 56 * s], [0, 74 * s]]), BREEZE, 5 * s),
        fill_group(body, BREEZE),
    ]


def how_register():
    OP = 96
    ring = layer("ring", [stroke_group(ellipse(120, 120), BREEZE, 5)], 1, OP,
                 pos=[150, 138],
                 s=kfs([(0, [0, 0]), (14, [108, 108]), (22, [100, 100])]))
    face = layer("face", [
        fill_group(ellipse(34, 34, (0, -16)), BREEZE),
        fill_group(ellipse(64, 40, (0, 26)), BREEZE),
    ], 2, OP, pos=[150, 140],
        o=kfs([(10, 0), (24, 100)]),
        s=kfs([(10, [60, 60]), (24, [100, 100])]))
    slots = []
    for i, (x, delay) in enumerate([(64, 40), (236, 54)]):
        slots.append(layer(
            f"slot{i}", [stroke_group(ellipse(56, 56), HAZE, 3.5),
                         fill_group(ellipse(14, 14, (0, -7)), HAZE),
                         fill_group(ellipse(27, 17, (0, 11)), HAZE)], 3 + i, OP,
            pos=[x, 138],
            o=kfs([(delay, 0), (delay + 12, 70)]),
            s=kfs([(delay, [60, 60]), (delay + 12, [100, 100])])))
    caption = layer("count", [fill_group(rect(88, 10, 5, (0, 0)), LINE)], 5, OP,
                    pos=[150, 232], o=kfs([(20, 0), (32, 100)]))
    return doc("how-register", [ring, face] + slots + [caption], OP)


def how_scan():
    OP = 100
    cells = []
    idx = 1
    lit = {(0, 1), (2, 0), (1, 2)}  # 매칭되는 셀
    for row in range(3):
        for col in range(3):
            x, y = 82 + col * 68, 70 + row * 68
            when = 18 + row * 22
            if (row, col) in lit:
                color = kfs([(when, HAZE[:3] + [1]), (when + 8, BREEZE[:3] + [1])])
                cells.append(layer(f"c{row}{col}", [fill_group(rect(56, 56, 10), color)],
                                   idx, OP, pos=[x, y], o=90))
            else:
                cells.append(layer(f"c{row}{col}", [fill_group(rect(56, 56, 10), LINE)],
                                   idx, OP, pos=[x, y]))
            idx += 1
    bar = layer("scanbar", [fill_group(rect(224, 14, 7), SOFT)], idx, OP,
                pos=kfs([(6, [150, 52]), (72, [150, 224])]),
                o=kfs([(0, 0), (8, 60), (72, 60), (84, 0)]))
    return doc("how-scan", [bar] + cells, OP)


def how_review():
    OP = 100
    layers = []
    # 두 장은 체크(담김), 한 장은 빠짐
    for i, x in enumerate([70, 150, 230]):
        layers.append(layer(f"photo{i}", [fill_group(rect(64, 64, 10), LINE)], 1 + i, OP,
                            pos=[x, 130],
                            o=kfs([(58, 100), (74, 38)]) if i == 2 else 100))
    for i, (x, start) in enumerate([(70, 12), (150, 30)]):
        check = stroke_group(
            path([[-14, 1], [-4, 11], [15, -10]]), BREEZE, 7,
            extras=[{"ty": "tm", "s": static(0),
                     "e": kfs([(start, 0), (start + 12, 100)]),
                     "o": static(0), "m": 1}])
        layers.append(layer(f"check{i}", [check], 4 + i, OP, pos=[x, 130],
                            o=kfs([(start, 0), (start + 2, 100)])))
    minus = layer("minus", [stroke_group(path([[-12, 0], [12, 0]]), HAZE, 7)], 6, OP,
                  pos=[230, 130], o=kfs([(58, 0), (68, 100)]))
    photos = [l for l in layers if l["nm"].startswith("photo")]
    checks = [l for l in layers if l["nm"].startswith("check")]
    return doc("how-review", checks + [minus] + photos, OP)


def how_sweep():
    OP = 110
    layers = []
    # 사진 석 장이 차례로 위-오른쪽으로 훌훌 날아간다
    for i, (x, y, delay) in enumerate([(96, 180, 0), (150, 196, 12), (204, 182, 24)]):
        layers.append(layer(
            f"fly{i}", [fill_group(rect(52, 52, 9), SOFT if i == 1 else BREEZE)],
            1 + i, OP,
            pos=kfs([(delay, [x, y]), (delay + 46, [x + 96, y - 128])]),
            r=kfs([(delay, 0), (delay + 46, 34)]),
            o=kfs([(delay, 100), (delay + 30, 100), (delay + 46, 0)]),
            s=kfs([(delay, [100, 100]), (delay + 46, [64, 64])])))
    for i, (x, y, delay) in enumerate([(120, 210, 18), (176, 214, 34)]):
        layers.append(layer(
            f"dust{i}", [fill_group(ellipse(8, 8), SOFT)], 4 + i, OP,
            pos=kfs([(delay, [x, y]), (delay + 36, [x + 60, y - 76])]),
            o=kfs([(delay, 0), (delay + 8, 70), (delay + 36, 0)])))
    ground = layer("tray", [stroke_group(path([[-84, 0], [84, 0]]), LINE, 6)], 7, OP,
                   pos=[150, 232])
    return doc("how-sweep", layers + [ground], OP)


def feature_seal():
    OP = 96
    photo = layer("photo", [fill_group(rect(120, 120, 16), LINE)], 3, OP,
                  pos=[150, 168], o=kfs([(24, 100), (44, 55)]))
    body = layer("lockbody", [fill_group(rect(64, 48, 10), BREEZE)], 1, OP,
                 pos=kfs([(10, [150, 68]), (30, [150, 160]), (36, [150, 152])]),
                 o=kfs([(4, 0), (12, 100)]))
    shackle = layer("shackle", [stroke_group(
        path([[-17, 8], [-17, -12], [17, -12], [17, 8]],
             i_tan=[[0, 0], [0, 12], [-19, 0], [0, -12]],
             o_tan=[[0, 12], [19, 0], [0, 12], [0, 0]]), BREEZE, 8)], 2, OP,
        pos=kfs([(10, [150, 30]), (30, [150, 122]), (36, [150, 114])]),
        o=kfs([(4, 0), (12, 100)]))
    return doc("feature-seal", [shackle, body, photo], OP)


def feature_privacy():
    OP = 120
    phone = layer("phone", [stroke_group(rect(132, 232, 26), INK, 6),
                            stroke_group(path([[-20, 0], [20, 0]]), INK, 5)], 1, OP,
                  pos=[150, 150], a=[0, 0])
    # 화면 하단 홈바 위치 보정: 두 번째 스트로크를 아래로
    phone["shapes"][1]["it"][0] = path([[-20, 98], [20, 98]])
    # 얼굴 점: 폰 안에서 원을 그리며 돈다 (앵커 오프셋 + 회전)
    orbit = layer("orbit", [fill_group(ellipse(22, 22, (0, -52)), BREEZE)], 2, OP,
                  pos=[150, 150], r=kfs([(0, 0), (OP, 360)]))
    pulse = layer("pulse", [stroke_group(ellipse(80, 80), SOFT, 4)], 3, OP,
                  pos=[150, 150],
                  s=kfs([(0, [40, 40]), (54, [110, 110]), (55, [40, 40], 'h'), (109, [110, 110])]),
                  o=kfs([(0, 60), (54, 0), (55, 60, 'h'), (109, 0)]))
    return doc("feature-privacy", [orbit, pulse, phone], OP)


def feature_shared():
    OP = 110
    def person(x, tone):
        return layer(f"p{x}", [stroke_group(ellipse(52, 52), tone, 3.5),
                               fill_group(ellipse(13, 13, (0, -7)), tone),
                               fill_group(ellipse(25, 16, (0, 11)), tone)], 4, OP,
                     pos=[x, 108])
    a, b = person(118, HAZE), person(182, HAZE)
    b["ind"] = 5
    # 방패: 아래에서 올라와 두 사람 앞에 선다
    shield_shape = path([[0, -30], [26, -18], [26, 6], [0, 32], [-26, 6], [-26, -18]],
                        closed=True,
                        i_tan=[[0, 0], [-6, -4], [0, -6], [10, -4], [0, 8], [0, 0]],
                        o_tan=[[6, -4], [0, 6], [0, 8], [-10, -4], [0, -6], [0, 0]])
    shield = layer("shield", [fill_group(shield_shape, BREEZE)], 1, OP,
                   pos=kfs([(12, [150, 235]), (32, [150, 178]), (38, [150, 172])]),
                   o=kfs([(12, 0), (24, 100)]))
    check = layer("check", [stroke_group(
        path([[-11, 0], [-3, 8], [12, -8]]), WHITE, 6,
        extras=[{"ty": "tm", "s": static(0), "e": kfs([(42, 0), (56, 100)]),
                 "o": static(0), "m": 1}])], 0, OP,
        pos=kfs([(12, [150, 232]), (32, [150, 175]), (38, [150, 169])]),
        o=kfs([(42, 0), (44, 100)]))
    check["ind"] = 6
    return doc("feature-shared", [check, shield, a, b], OP)


def feature_multiface():
    OP = 120
    slots = []
    for i, x in enumerate([80, 150, 220]):
        dim = kfs([(58, 100), (72, 45)]) if x != 150 else 100
        slots.append(layer(f"s{i}", [stroke_group(ellipse(52, 52), HAZE, 3.5),
                                     fill_group(ellipse(13, 13, (0, -7)), HAZE),
                                     fill_group(ellipse(25, 16, (0, 11)), HAZE)],
                           4 + i, OP, pos=[x, 130], o=dim))
    # 선택 링: 훑다가 가운데에 멈춘다
    ring = layer("ring", [stroke_group(ellipse(64, 64), BREEZE, 5)], 1, OP,
                 pos=kfs([(8, [80, 130]), (26, [80, 130]), (40, [220, 130]),
                          (54, [220, 130]), (66, [150, 130])]),
                 o=kfs([(8, 0), (14, 100)]),
                 s=kfs([(60, [100, 100]), (70, [108, 108]), (76, [100, 100])]))
    check = layer("check", [stroke_group(
        path([[-10, 0], [-3, 7], [11, -7]]), BREEZE, 6,
        extras=[{"ty": "tm", "s": static(0), "e": kfs([(74, 0), (86, 100)]),
                 "o": static(0), "m": 1}])], 2, OP,
        pos=[150, 196], o=kfs([(74, 0), (76, 100)]))
    return doc("feature-multiface", [check, ring] + slots, OP)


def feature_period():
    OP = 130
    chips = []
    # 칩 3개: 훑고 가운데(최근 1년)가 선택돼 남는다
    for i, x in enumerate([83, 150, 217]):
        if i == 1:
            color = kfs([(30, LINE[:3] + [1]), (40, BREEZE[:3] + [1])])
        else:
            color = static(LINE)
        chips.append(layer(f"chip{i}", [fill_group(rect(58, 28, 14), color)],
                           3 + i, OP, pos=[x, 84]))
    # 시계: 예상 시간
    face = layer("clock", [stroke_group(ellipse(72, 72), BREEZE, 5)], 1, OP,
                 pos=[150, 182],
                 s=kfs([(44, [0, 0]), (58, [106, 106]), (66, [100, 100])]))
    hand = layer("hand", [stroke_group(path([[0, 0], [0, -24]]), BREEZE, 5)], 2, OP,
                 pos=[150, 182], r=kfs([(60, 0), (124, 360)]),
                 o=kfs([(44, 0), (58, 100)]))
    tick = layer("tick", [fill_group(ellipse(7, 7), BREEZE)], 0, OP,
                 pos=[150, 182], o=kfs([(44, 0), (58, 100)]))
    tick["ind"] = 6
    return doc("feature-period", [tick, hand, face] + chips, OP)


def feature_live():
    OP = 120
    track = layer("track", [fill_group(rect(200, 10, 5), LINE)], 3, OP, pos=[150, 74])
    # 채워지는 바: 왼쪽 끝 고정으로 늘어난다
    bar = layer("bar", [fill_group(rect(200, 10, 5), BREEZE)], 2, OP,
                pos=[50, 74], a=[-100, 0],
                s=kfs([(6, [0, 100]), (100, [96, 100])]))
    thumbs = []
    for i, (x, delay) in enumerate([(94, 26), (150, 52), (206, 78)]):
        thumbs.append(layer(
            f"t{i}", [fill_group(rect(50, 50, 9), SOFT if i == 1 else BREEZE)],
            4 + i, OP, pos=[x, 166],
            o=kfs([(delay, 0), (delay + 10, 100)]),
            s=kfs([(delay, [40, 40]), (delay + 10, [108, 108]), (delay + 16, [100, 100])])))
    return doc("feature-live", [bar, track] + thumbs, OP)


def main():
    out_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets", "lottie"))
    os.makedirs(out_dir, exist_ok=True)
    docs = {
        "how-register": how_register(),
        "how-scan": how_scan(),
        "how-review": how_review(),
        "how-sweep": how_sweep(),
        "feature-seal": feature_seal(),
        "feature-privacy": feature_privacy(),
        "feature-shared": feature_shared(),
        "feature-multiface": feature_multiface(),
        "feature-period": feature_period(),
        "feature-live": feature_live(),
    }
    for name, d in docs.items():
        p = os.path.join(out_dir, name + ".json")
        with open(p, "w") as f:
            json.dump(d, f, separators=(",", ":"))
        print(f"{name}.json  {os.path.getsize(p)} bytes")


if __name__ == "__main__":
    main()
