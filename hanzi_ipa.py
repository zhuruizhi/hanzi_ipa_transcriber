# -*- coding: utf-8 -*-
"""Pinyin_IPA.ipynb

!pip -q install pypinyin ToJyutping

import re
from pypinyin import lazy_pinyin, Style
import ToJyutping

# ----------------------------
# 1) Mandarin tones: pinyin 1/2/3/4 -> Chao tone numerals
# ----------------------------
TONE_TO_CHAO = {
    "1": "55",
    "2": "35",
    "3": "214",
    "4": "51",
    "5": "0",
    "0": "0",
}

# ----------------------------
# 2) List of Mandarin Pinyin initials (longest first)
# ----------------------------
PINYIN_INITIALS = [
    "zh","ch","sh",
    "b","p","m","f",
    "d","t","n","l",
    "g","k","h",
    "j","q","x",
    "r","z","c","s",
]

# ----------------------------
# 3) Mandarin initials: Pinyin -> IPA
# ----------------------------
INITIAL_TO_IPA = {
    "": "",
    "b": "p",    "p": "pʰ",   "m": "m",  "f": "f",
    "d": "t",    "t": "tʰ",   "n": "n",  "l": "l",
    "g": "k",    "k": "kʰ",   "h": "x",
    "j": "tɕ",   "q": "tɕʰ",  "x": "ɕ",
    "zh": "ʈʂ",  "ch": "ʈʂʰ", "sh": "ʂ",
    "r": "ʐ",
    "z": "ts",   "c": "tsʰ",  "s": "s",
}

# ----------------------------
# 4) Mandarin finals: (normalized) Pinyin final -> IPA
#    Preferred version: glides are written only when the original Pinyin begins with y/w
# ----------------------------
FINAL_TO_IPA = {
    # a group
    "a": "a", "ai": "aɪ", "ao": "aʊ", "ei": "eɪ", "ou": "oʊ",
    "an": "an", "en": "ən", "ang": "ɑŋ", "eng": "əŋ", "er": "ɚ",
    "e": "ɤ", "o": "o",

    # u group (do not transcribe medial u as w)
    "u": "u", "ong": "ʊŋ",
    "ua": "ua", "uo": "uo", "uai": "uaɪ",
    "ui": "ueɪ", "uei": "ueɪ",
    "uan": "uan", "un": "uən", "uen": "uən",
    "uang": "uɑŋ", "ueng": "uəŋ",

    # i group (do not transcribe medial i as j)
    "i": "i",
    "ia": "ia", "ie": "iɛ", "iao": "iaʊ",
    "iu": "ioʊ", "iou": "ioʊ",
    "ian": "iɛn", "in": "in",
    "iang": "iɑŋ", "ing": "iŋ", "iong": "iʊŋ",

    # ü group: v is used internally to represent ü
    "v": "y",
    "ve": "ɥe",
    "van": "ɥɛn",
    "vn": "yn",
}

# ----------------------------
# 5) Cantonese: Jyutping -> IPA  (following Help:IPA/Cantonese)
# ----------------------------
SYLLABIC = "\u0329"   # ̩
NO_RELEASE = "\u031A" # ̚
LABIALIZED = "\u02B7" # ʷ

CANTO_INITIALS = [
    "gw","kw","ng",
    "b","p","m","f",
    "d","t","n","l",
    "g","k","h",
    "z","c","s",
    "j","w",
]

CANTO_INITIAL_TO_IPA = {
    "": "",
    "b": "p",
    "p": "pʰ",
    "m": "m",
    "f": "f",
    "d": "t",
    "t": "tʰ",
    "n": "n",
    "l": "l",
    "g": "k",
    "k": "kʰ",
    "ng": "ŋ",
    "h": "h",
    "gw": "k" + LABIALIZED,
    "kw": "k" + LABIALIZED + "ʰ",
    "z": "ts",
    "c": "tsʰ",
    "s": "s",
    "j": "j",
    "w": "w",
}

CANTO_FINAL_TO_IPA = {
    # vocalic finals
    "aa": "a",
    "aai": "aj",
    "aau": "aw",
    "e": "ɛ",
    "ei": "ej",
    "ai": "ɐj",
    "au": "ɐw",
    "i": "i",
    "iu": "iw",
    "o": "ɔ",
    "oe": "œ",
    "oi": "ɔj",
    "ou": "ɔw",
    "eoi": "ɵɥ",
    "u": "u",
    "ui": "uj",
    "yu": "y",

    # nasal finals
    "m": "m" + SYLLABIC,
    "aam": "am",
    "am": "ɐm",
    "im": "im",
    "aan": "an",
    "an": "ɐn",
    "in": "in",
    "eon": "ɵn",
    "eun": "ɵn",
    "on": "ɔn",
    "un": "un",
    "yun": "yn",
    "ng": "ŋ" + SYLLABIC,
    "aang": "aŋ",
    "ang": "ɐŋ",
    "eng": "ɛŋ",
    "ing": "ɪŋ",
    "ong": "ɔŋ",
    "oeng": "œŋ",
    "eung": "œŋ",
    "ung": "ʊŋ",

    # checked finals (unreleased stops)
    "aap": "a" + "p" + NO_RELEASE,
    "ap":  "ɐ" + "p" + NO_RELEASE,
    "ip":  "i" + "p" + NO_RELEASE,
    "aat": "a" + "t" + NO_RELEASE,
    "at":  "ɐ" + "t" + NO_RELEASE,
    "it":  "i" + "t" + NO_RELEASE,
    "eot": "ɵ" + "t" + NO_RELEASE,
    "eut": "ɵ" + "t" + NO_RELEASE,
    "ot":  "ɔ" + "t" + NO_RELEASE,
    "ut":  "u" + "t" + NO_RELEASE,
    "yut": "y" + "t" + NO_RELEASE,
    "aak": "a" + "k" + NO_RELEASE,
    "ak":  "ɐ" + "k" + NO_RELEASE,
    "ek":  "ɛ" + "k" + NO_RELEASE,
    "ik":  "ɪ" + "k" + NO_RELEASE,
    "oek": "œ" + "k" + NO_RELEASE,
    "euk": "œ" + "k" + NO_RELEASE,
    "ok":  "ɔ" + "k" + NO_RELEASE,
    "uk":  "ʊ" + "k" + NO_RELEASE,
}

# Cantonese tones: Jyutping 1–6 -> numeric contours (Wikipedia key)
CANTO_TONE_TO_CONTOUR = {
    "1": "55",
    "2": "25",
    "3": "33",
    "4": "21",
    "5": "23",
    "6": "22",
    # If 7/8/9 occur, treat them as the checked-tone variants of 1/3/6 according to the key
    "7": "55",
    "8": "33",
    "9": "22",
}

# ----------------------------
# 6) IPA -> TIPA LaTeX macros (extended with symbols commonly used for Cantonese)
# ----------------------------
IPA_TO_TIPA = {
    # Existing mappings
    "ɕ": r"\textctc",
    "ʂ": r"\textrtails",
    "ʐ": r"\textrtailz",
    "ʈ": r"\textrtailt",
    "ŋ": r"\ng",

    "ɑ": r"\textscripta",
    "ɛ": r"\textepsilon",
    "ə": r"\textschwa",
    "ɚ": r"\textrhookschwa",
    "ɤ": r"\textramshorns",
    "ʊ": r"\textupsilon",
    "ɪ": r"\textsci",

    "ɻ": r"\textturnrrtail",
    "ɹ": r"\textturnr",

    "ʰ": r"\super h",
    "ʷ": r"\super w",

    # Additional symbols commonly used for Cantonese
    "ɐ": r"\textturna",
    "ɔ": r"\textopeno",
    "ɵ": r"\textbaro",
    "œ": r"\oe",
    "ɥ": r"\textturnh",

    # "No audible release" diacritic: approximated with corner
    NO_RELEASE: r"\textcorner",
}

CONTROL_WORD = re.compile(r"^\\[A-Za-z]+$")

def _is_hanzi(ch: str) -> bool:
    return bool(re.match(r"[\u4e00-\u9fff]", ch))

def split_tone(py: str):
    py = py.lower()
    m = re.match(r"^([a-züv:]+)([0-5])$", py)
    if not m:
        return py, "0"
    base, tone = m.group(1), m.group(2)
    base = base.replace("u:", "v").replace("ü", "v")
    return base, tone

def normalize_zero_initial(base: str):
    """
    Mandarin: output the j-/w- glide only when the original Pinyin begins with y-/w-
    """
    if base.startswith("y"):
        if base.startswith("yu"):
            return "v" + base[2:], ""
        rest = base[1:]
        if rest.startswith("i"):
            return rest, ""
        return "i" + rest, "j"

    if base.startswith("w"):
        if base == "wu":
            return "u", ""
        return "u" + base[1:], "w"

    return base, ""

def split_initial_final(base: str):
    for ini in PINYIN_INITIALS:
        if base.startswith(ini):
            return ini, base[len(ini):]
    return "", base

def pinyin_base_to_ipa(base: str) -> str:
    base, glide = normalize_zero_initial(base)
    ini, fin = split_initial_final(base)

    if ini in {"j", "q", "x"} and fin.startswith("u"):
        fin = "v" + fin[1:]
    if ini in {"b", "p", "m", "f"} and fin == "o":
        fin = "uo"

    ini_ipa = INITIAL_TO_IPA.get(ini)
    if ini_ipa is None:
        raise ValueError(f"Unrecognized initial: {ini} (from {base})")

    # apical vowels
    if fin == "i" and ini in {"zh", "ch", "sh", "r"}:
        fin_ipa = "ɻ" + SYLLABIC
    elif fin == "i" and ini in {"z", "c", "s"}:
        fin_ipa = "ɹ" + SYLLABIC
    else:
        fin_ipa = FINAL_TO_IPA.get(fin)
        if fin_ipa is None:
            raise ValueError(f"Unrecognized final: {fin} (from {base})")

    if ini_ipa == "" and glide == "j":
        return ("j" + fin_ipa[1:]) if fin_ipa.startswith("i") else ("j" + fin_ipa)
    if ini_ipa == "" and glide == "w":
        return ("w" + fin_ipa[1:]) if fin_ipa.startswith("u") else ("w" + fin_ipa)

    return ini_ipa + fin_ipa

def split_canto_initial_final(base: str):
    for ini in CANTO_INITIALS:
        if base.startswith(ini):
            return ini, base[len(ini):]
    return "", base

def split_jyutping_syllable(jp: str):
    """
    e.g. 'toi4' -> ('toi', '4')
    """
    m = re.match(r"^([a-z]+)([1-9])$", jp)
    if not m:
        return jp, "0"
    return m.group(1), m.group(2)

def jyutping_to_ipa(jp: str) -> tuple[str, str]:
    """
    return (ipa, contour_digits)
    """
    base, tone = split_jyutping_syllable(jp)
    ini, fin = split_canto_initial_final(base)

    ini_ipa = CANTO_INITIAL_TO_IPA.get(ini)
    if ini_ipa is None:
        raise ValueError(f"Unrecognized Cantonese initial: {ini} (from {jp})")

    fin_ipa = CANTO_FINAL_TO_IPA.get(fin)
    if fin_ipa is None:
        raise ValueError(f"Unrecognized Cantonese final: {fin} (from {jp})")

    contour = CANTO_TONE_TO_CONTOUR.get(tone, "0")
    return ini_ipa + fin_ipa, contour

def ipa_to_tipa(ipa: str) -> str:
    """
    IPA Unicode -> TIPA LaTeX (for use inside \textipa{...})
    Supports any "consonant + syllabic diacritic" sequence (◌̩)
    """
    out = []
    i = 0
    while i < len(ipa):
        ch = ipa[i]

        # General syllabic handling: X + ̩  -> \textsyllabic{X}
        if i + 1 < len(ipa) and ipa[i+1] == SYLLABIC:
            base = IPA_TO_TIPA.get(ch, ch)
            out.append(r"\textsyllabic{" + base + "}")
            i += 2
            continue

        mapped = IPA_TO_TIPA.get(ch, ch)
        out.append(mapped)

        # Add a space after a control-word macro
        if CONTROL_WORD.match(mapped):
            out.append(" ")

        i += 1

    return "".join(out).strip()

def tone_digit_to_chao(tone_digit: str) -> str:
    return TONE_TO_CHAO.get(tone_digit, "0")

def canto_char_to_jyutping(ch: str) -> str | None:
    """
    Single character: use ToJyutping to obtain Jyutping with a tone digit (e.g. 'toi4').
    """
    s = ToJyutping.get_jyutping_text(ch).strip()
    if not s or "…" in s or "[" in s:
        return None
    # A single character normally returns only one syllable; take the first token as a safeguard
    return s.split()[0]

def transcribe(text: str, dialect: str = "mandarin") -> str:
    """
    dialect:
      - 'mandarin' / 'cmn'
      - 'cantonese' / 'yue'
    """
    dialect = dialect.lower().strip()
    tokens = []

    for ch in text:
        if _is_hanzi(ch):
            if dialect in {"mandarin", "cmn"}:
                py = lazy_pinyin(ch, style=Style.TONE3, neutral_tone_with_five=True)[0]
                base, tone_digit = split_tone(py)
                ipa = pinyin_base_to_ipa(base)
                tipa = ipa_to_tipa(ipa)
                tone = tone_digit_to_chao(tone_digit)
                tokens.append(f"{ch} [\\textipa{{{tipa}}}{tone}]")

            elif dialect in {"cantonese", "yue"}:
                jp = canto_char_to_jyutping(ch)
                if jp is None:
                    tokens.append(f"{ch} [\\textipa{{?}}0]")
                else:
                    ipa, contour = jyutping_to_ipa(jp)
                    tipa = ipa_to_tipa(ipa)
                    tokens.append(f"{ch} [\\textipa{{{tipa}}}{contour}]")
            else:
                raise ValueError("dialect must be 'mandarin/cmn' or 'cantonese/yue'")

        else:
            if ch.strip():
                tokens.append(ch)

    return " ".join(tokens)

# ---- Demo ----
print(transcribe("睿", dialect="mandarin"))
print(transcribe("喺", dialect="cantonese"))