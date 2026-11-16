#!/usr/bin/env python3
"""Check every entry against README.md's rules; print every problem, exit 1 if any."""
import pathlib
import re
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent
FIELDS = {"op", "at", "arch", "license", "notes"}
REQUIRED = {"op", "at", "arch"}
OP_MAX = 160
ARCH = re.compile(r"sm_\d+[af]?")
HF = re.compile(r"hf:[\w.-]+/[\w.-]+/[\w.+=-]+-[0-9a-f]{8}#\w+")
GITHUB = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/blob/[0-9a-f]{7,40}/\S+#\w+")
NAME = re.compile(r"[\w.]+-[\w.+=-]+\.toml")
BANNED = re.compile(r"\b(fast|faster|fastest|optimized|efficient|high-performance|blackwell|hopper|sm_?\d+[af]?)\b", re.I)


def glossary():
    block = (ROOT / "GLOSSARY.md").read_text().split("```")[1]
    rows = (re.split(r"\s{2,}", line.strip(), maxsplit=1) for line in block.splitlines() if line.strip())
    return {alias.strip(): term for term, aliases in (r for r in rows if len(r) == 2) for alias in aliases.split(",")}


def op_problems(op, aliases):
    bare = re.sub(r"\([^)]*\)", "", op)
    return ([f"`op` is {len(op)} characters, over {OP_MAX}"] if len(op) > OP_MAX else []) + \
        (["`op` is one line"] if "\n" in op else []) + \
        [f"`op` says `{m.group(0)}`: no speed, quality or arch words" for m in BANNED.finditer(bare)] + \
        [f"`op` says `{alias}`: write `{term}`" for alias, term in aliases.items()
         if re.search(rf"(?<![\w-]){re.escape(alias)}(?![\w-])", bare, re.I)]


def entry_problems(path, aliases):
    if not NAME.fullmatch(path.name):
        return [f"name is not <source>-<name>.toml"]
    try:
        e = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as err:
        return [f"not TOML: {err}"]
    at = e.get("at", "")
    return [f"unknown field `{k}`" for k in sorted(e.keys() - FIELDS)] + \
        [f"missing `{k}`" for k in sorted(REQUIRED - e.keys())] + \
        [f"`{k}` is not a string" for k in ("op", "at", "license", "notes") if k in e and not isinstance(e[k], str)] + \
        (op_problems(e["op"], aliases) if isinstance(e.get("op"), str) else []) + \
        ([f"`at` is neither hf:<org>/<repo>/<name>-<sha8>#<symbol> nor a GitHub blob URL at a commit with #<symbol>"]
         if isinstance(at, str) and at and not (HF.fullmatch(at) or GITHUB.fullmatch(at)) else []) + \
        (["`arch` is a non-empty list of nvcc arch names like sm_103a"]
         if "arch" in e and not (isinstance(e["arch"], list) and e["arch"]
                                 and all(isinstance(a, str) and ARCH.fullmatch(a) for a in e["arch"])) else []) + \
        (["`arch` lists an arch twice"] if isinstance(e.get("arch"), list) and len(set(map(str, e["arch"]))) < len(e["arch"]) else []) + \
        ([f"upstream `arch` `{a}` carries a suffix: a and f are a build's choice" for a in e.get("arch", [])
          if isinstance(at, str) and at.startswith("https://") and isinstance(a, str) and a[-1:] in ("a", "f")]) + \
        (["upstream entry without `license`"] if isinstance(at, str) and at.startswith("https://") and "license" not in e else []) + \
        (["`license` belongs to upstream entries; ours carry LICENSE in their folder"]
         if isinstance(at, str) and at.startswith("hf:") and "license" in e else [])


def main():
    aliases = glossary()
    entries = sorted(p for p in ROOT.glob("*/*.toml") if not p.parent.name.startswith("."))
    problems = [f"{p.relative_to(ROOT)}: {msg}" for p in entries for msg in
                ((["symlink to nothing"] if not p.exists() else []) if p.is_symlink() else entry_problems(p, aliases))]
    print("\n".join(problems) or f"{len(entries)} entries, no problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
