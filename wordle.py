WORDS_FILE = "./all-wordle-words.txt"
DEBUG      = True
_ORD_A     = ord('a')


# ── precomputation ────────────────────────────────────────────────────────────

def _mask(word: str) -> int:
    """26-bit presence mask: bit i is set ↔ chr(97+i) appears in word."""
    m = 0
    for ch in word:
        m |= 1 << (ord(ch) - _ORD_A)
    return m

def load() -> list[tuple[str, int]]:
    """Load words and precompute their bitmasks once."""
    with open(WORDS_FILE) as f:
        return [(w, _mask(w)) for line in f if (w := line.strip())]


# ── filtering ─────────────────────────────────────────────────────────────────

def filter_pool(
    pool:     list[tuple[str, int]],
    inc_mask: int,
    exc_mask: int,
    exact:    dict[int, str],        # {position: char}  – green tiles
    wrong:    set[tuple[int, str]],  # {(position, char)} – yellow tiles
) -> list[tuple[str, int]]:
    out        = []
    ex_items   = list(exact.items())  # snapshot once; list is faster to iterate
    wrong_list = list(wrong)
    for word, mask in pool:
        if mask & exc_mask:                           continue  # has an excluded letter
        if (mask & inc_mask) != inc_mask:             continue  # missing an included letter
        if any(word[p] != c for p, c in ex_items):   continue  # exact-position mismatch
        if any(word[p] == c for p, c in wrong_list): continue  # letter at a forbidden spot
        out.append((word, mask))
    return out


# ── display ───────────────────────────────────────────────────────────────────

def _mask_to_chars(m: int) -> list[str]:
    return [chr(_ORD_A + i) for i in range(26) if m >> i & 1]

def show(pool: list[tuple[str, int]], no_dup: bool = False) -> None:
    words = [w for w, _ in pool]
    if no_dup:
        words = [w for w in words if len(set(w)) == len(w)]
    print(words, len(words))


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ALL: list[tuple[str, int]] = load()   # immutable master list

    # All state lives as locals → LOAD_FAST, not LOAD_GLOBAL
    pool:     list[tuple[str, int]] = list(ALL)
    inc_mask: int                   = 0
    exc_mask: int                   = 0
    exact:    dict[int, str]        = {}
    wrong:    set[tuple[int, str]]  = set()

    while True:
        a = input()
        changed = False

        if a.startswith("i"):                          # include letters
            for ch in a[1:]:
                inc_mask |= 1 << (ord(ch) - _ORD_A)
            changed = True

        elif a.startswith("n"):                        # exclude letters
            for ch in a[1:]:
                exc_mask |= 1 << (ord(ch) - _ORD_A)
            changed = True

        elif a.startswith("e") and len(a) == 3:       # exact position (green)
            ch, pos = a[1], int(a[2]) - 1
            inc_mask |= 1 << (ord(ch) - _ORD_A)
            exact[pos] = ch
            changed = True

        elif a.startswith("r") and len(a) == 3:       # wrong position (yellow)
            ch, pos = a[1], int(a[2]) - 1
            inc_mask |= 1 << (ord(ch) - _ORD_A)
            wrong.add((pos, ch))
            changed = True

        elif a.startswith("clear"):
            inc_mask = exc_mask = 0
            exact.clear()
            wrong.clear()
            pool = list(ALL)

        elif a.startswith("show"):
            show(pool, no_dup=a.endswith("1"))

        if changed:
            if DEBUG:
                print(_mask_to_chars(inc_mask), _mask_to_chars(exc_mask), exact, wrong)
            pool = filter_pool(pool, inc_mask, exc_mask, exact, wrong)


main()
