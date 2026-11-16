# kern-atlas

Where GPU kernels already exist: ours and upstream's, one file each, for an agent to find before it
writes another.

## Use

```sh
ls topk/                       # every kernel of one op class
grep -ril mxfp8 .              # any word; search with GLOSSARY.md's terms
```

An entry's `at` says where the kernel lives. `hf:` names a folder of
[Pegainfer/kern-kernels](https://huggingface.co/Pegainfer/kern-kernels) holding `kernel.cubin`,
`src/`, `build.sh` (rebuilds `kernel.cubin` byte for byte) and `LICENSE`; `https://github.com/`
names a source file at a commit, `#` the kernel's symbol. Read the source before using a kernel:
its constants, dtypes and launch geometry are there, not here.

## An entry

`<op class>/<source>-<name>.toml`. A kernel of several op classes sits in its main one and is
symlinked from the others.

| Field | | |
|---|---|---|
| `op` | required | what it computes, one sentence (below) |
| `at` | required | where it lives |
| `arch` | required | nvcc's spelling (`sm_90a`, `sm_100f`, `sm_103a`): the cubin's target, or the archs the source has a path for |
| `license` | upstream entries | SPDX id; ours carry `LICENSE` in their folder |
| `notes` | optional | facts the source does not show: measurements, what was tried and failed. Each with its date |

No other field. A new one names the tool that reads it and why the fact cannot stay in the source.

## Writing `op`

- One sentence, at most 160 characters, starting with what is computed.
- The common name first, the upstream's own in parentheses: `MoE routing top-16 of 896 experts (noaux_tc)`.
- Sizes as the kernel's numbers: `top-k 2048`, `3584-wide`.
- Fused stages joined by ` + `, in the order they run.
- Terms as `GLOSSARY.md` spells them.
- Not in it: speed or quality words, the arch, the repository, measurements.

`python3 check.py` checks every entry; CI runs it.
