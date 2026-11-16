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
| `arch` | required | every arch it runs on, listed one by one in nvcc's spelling (`sm_100`, `sm_103a`): the cubin's target, or the archs an upstream build compiles the source for |
| `license` | upstream entries | SPDX id; ours carry `LICENSE` in their folder |
| `notes` | optional | facts the source does not show: measurements, what was tried and failed. Each with its date |

No other field. A new one names the tool that reads it and why the fact cannot stay in the source.

How to search, write an entry and publish a kernel: [AGENTS.md](AGENTS.md). `python3 check.py`
checks every entry; CI runs it.
