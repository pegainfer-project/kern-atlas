# kern-atlas

Only judgment lives in this file. `python3 check.py` enforces the rest; run it before every commit.

## Before writing a kernel

- Search here first: `ls <class>/`, then grep the `GLOSSARY.md` terms, then the upstream names you
  know, then the computation in other words (a top-k is also a select; MoE routing is also gating).
  A symlink is an entry listed under a second class.
- No match here does not mean no kernel exists. Search the upstream sources (FlashInfer, vLLM,
  SGLang, TensorRT-LLM, DeepGEMM, ...) for the same computation. Whatever you find goes in as an
  entry, whether you use it or not: the next agent searches here.
- Judge fit from the source, never from `op`: the constants compiled in, dtypes, layouts, launch
  geometry, the arch guards.
- The commit that adds a kernel to a model repository says `prior-art: <entry paths>`, or
  `prior-art: none, searched <terms>`.

## Adding an entry

- One kernel entry point per file. A cubin with two entry points is two files naming one folder.
- File it under what it mainly computes and symlink it from the classes of the stages it fuses. A
  new class directory only when none fits; its name becomes a glossary term.
- `op`, one sentence of at most 160 characters:
  - starts with what is computed;
  - the common name first, the upstream's own in parentheses: `MoE routing top-16 of 896 experts (noaux_tc)`;
  - sizes as the kernel's numbers: `top-k 2048`, `3584-wide`;
  - fused stages joined by ` + `, in the order they run;
  - terms as `GLOSSARY.md` spells them; a new term goes there with the spellings it replaces;
  - no speed or quality words, no arch, no repository, no measurements.
- `at` for an upstream kernel names a commit hash, never a branch, and the symbol after `#`.
- `arch` lists every arch, one by one, never a range. For ours, the cubin's target as `cuobjdump`
  reports it, suffix included. For upstream, each arch the upstream build compiles the source for
  whose guards and dispatch admit the kernel's whole path, without a suffix (`a` or `f` is the
  build's choice, not the source's).
- `notes` holds only what the source does not show: measurements and attempts that failed, each
  dated, with where it was measured (GPU, shapes, commit) and why it failed. A note that stops
  being true is corrected or removed.

## Publishing our kernel

A folder `<module>-<sha8>/` in [Pegainfer/kern-kernels](https://huggingface.co/Pegainfer/kern-kernels),
never changed after upload: new bytes are a new folder. `k31_topk-5eff1799/` is the template.

- `kernel.cubin`; `src/`, everything the build reads beyond the CUDA toolkit; `LICENSE`.
- `build.sh [OUT]` checks the nvcc version, builds in the fixed directory `/tmp/kern-build` (nvcc
  names anonymous-namespace symbols after the source's absolute path, so another directory gives
  another sha256), checks the sha256 and copies the cubin to `OUT`.
- Before uploading, run `build.sh` from two copies of the folder in different places; both print
  the sha256. After uploading, download `kernel.cubin` and check its sha256.
- Upload only source we may redistribute: ours, or upstream's under a license that allows it,
  with that license.

## This repository is public

No hostnames, user names, internal paths or cluster names in anything committed or uploaded.
Every commit is signed off (`git commit -s`) by the identity that authored it.
