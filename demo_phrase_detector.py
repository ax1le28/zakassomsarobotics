import cv2
import numpy as np

from image_utils import normalize_bbox
from schemas import Detection

PHRASE_LABEL = "oi oi oi"

_TEMPLATES: list[tuple[np.ndarray, int, int]] | None = None


def _build_templates() -> list[tuple[np.ndarray, int, int]]:
    templates: list[tuple[np.ndarray, int, int]] = []
    phrases = ("Oi Oi Oi", "OI OI OI", "oi oi oi")
    fonts = (cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_DUPLEX)
    for phrase in phrases:
        for font in fonts:
            for scale in (0.7, 0.9, 1.15, 1.4, 1.75, 2.1, 2.5):
                thickness = max(2, int(round(scale * 2)))
                (tw, th), baseline = cv2.getTextSize(phrase, font, scale, thickness)
                canvas = np.zeros((th + baseline + 24, tw + 24), dtype=np.uint8)
                cv2.putText(
                    canvas,
                    phrase,
                    (12, th + 10),
                    font,
                    scale,
                    255,
                    thickness,
                    cv2.LINE_AA,
                )
                edges = cv2.Canny(canvas, 50, 150)
                if edges.sum() > 0:
                    templates.append((edges, canvas.shape[1], canvas.shape[0]))
    return templates


def _templates() -> list[tuple[np.ndarray, int, int]]:
    global _TEMPLATES
    if _TEMPLATES is None:
        _TEMPLATES = _build_templates()
    return _TEMPLATES


def _best_text_match(frame_bgr: np.ndarray) -> tuple[float, tuple[int, int, int, int] | None]:
    h, w = frame_bgr.shape[:2]
    max_width = 960
    scale_down = min(1.0, max_width / max(w, 1))
    if scale_down < 1.0:
        small = cv2.resize(frame_bgr, (int(w * scale_down), int(h * scale_down)))
    else:
        small = frame_bgr

    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    edge_frames = (
        cv2.Canny(gray, 50, 150),
        cv2.Canny(255 - gray, 50, 150),
    )

    best_score = 0.0
    best_box = None
    sh, sw = gray.shape[:2]

    for edges in edge_frames:
        for template, tw, th in _templates():
            if tw >= sw or th >= sh:
                continue
            result = cv2.matchTemplate(edges, template, cv2.TM_CCOEFF_NORMED)
            _, score, _, loc = cv2.minMaxLoc(result)
            if score > best_score:
                x1, y1 = loc
                best_score = float(score)
                best_box = (x1, y1, x1 + tw, y1 + th)

    if not best_box or scale_down == 0:
        return best_score, None

    inv = 1.0 / scale_down
    x1, y1, x2, y2 = best_box
    return best_score, (
        int(x1 * inv),
        int(y1 * inv),
        int(x2 * inv),
        int(y2 * inv),
    )


def detect_demo_phrases(frame_bgr: np.ndarray) -> list[Detection]:
    score, box = _best_text_match(frame_bgr)
    if box is None or score < 0.16:
        return []

    h, w = frame_bgr.shape[:2]
    return [
        Detection(
            label=PHRASE_LABEL,
            raw_label="Oi Oi Oi",
            category="demo",
            confidence=round(min(1.0, score), 3),
            distance=1.0,
            position="center",
            bbox=normalize_bbox(box, w, h),
            action="STOP",
            source="demo_text",
            priority=9.0,
            risk=0.0,
        )
    ]
