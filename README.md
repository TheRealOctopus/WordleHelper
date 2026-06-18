# WordleHelper 

A lightweight command-line tool that narrows down your Wordle candidates in real time. Feed it the clues from each guess — green, yellow, and grey tiles — and it filters a word list down to only the words still possible.

---

## Requirements

- Python 3.x
- A `words.txt` file in the same directory — one word per line (5-letter words recommended)

---

## Setup

```bash
git clone ttps://github.com/TheRealOctopus/WordleHelper.git
cd WordleHelper
# You can change the words.txt file, then:
python wordle.py
```

---

## Commands

Commands are entered one at a time. The word list is filtered immediately after each command.

| Command | Meaning | Example |
|--------|---------|---------|
| `i<char>` | **Include** — keep only words containing this letter (yellow or green tile) | `iae` → keep words with `a` and `e` |
| `n<char>` | **Not include** — remove words containing this letter (grey tile) | `nz` → remove words with `z` |
| `e<char><pos>` | **Exact** — keep only words with this letter at this position (green tile) | `ea2` → `a` must be at position 2 |
| `r<char><pos>` | **Remove position** — remove words with this letter at this position (yellow tile — letter exists but not here) | `ra2` → remove words where `a` is at position 2 |
| `show` | Print the current list of remaining candidates | `show` |
| `clear` | Reset the word list back to the full original list | `clear` |

> Positions are **1-indexed** (position 1 is the first letter).

---

## Example Workaround

Say your target word is **CRANE** and your first guess is **AUDIO**:

```
Guess: AUDIO
Result: A=grey, U=grey, D=grey, I=grey, O=grey
```

```
na
nu
nd
ni
no
show
```

Next guess: **STERN**

```
Guess: STERN
Result: S=grey, T=grey, E=🟡, R=🟡, N=🟢
```

```
nster
en5
re2
show
```

The list now contains only words where `e` and `r` are present, `n` is the last letter, `e` is not at position 2, and `r` is not at position 3.

---

## Notes

- The `i` (include) command keeps words that contain the letter **anywhere** — pair it with `r` to express "letter is in the word but not at this spot" (yellow tile).
- `clear` reloads the word list from `words.txt` so you can start a fresh puzzle without restarting the script.
- Each command resets internal state after filtering, so commands don't stack — enter one clue at a time.
- The "words.txt" file may not include the name of a compound for something the same.
- Original words list file [https://gist.github.com/daemondevin/df09befaf533c380743bc2c378863f0c]
- Wordle words list file [https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93]
