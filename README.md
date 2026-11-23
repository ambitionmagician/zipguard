# ZipGuard

by Dr. Brent Allen Jensen

Inspect ZIP archives — and extract them safely. ZipGuard refuses any
member whose path would escape the destination directory (absolute
paths and `..` traversal, the classic "zip slip"), so a hostile
archive cannot write outside the folder you chose.

## Quickstart

```bash
python3 zipguard.py list archive.zip
python3 zipguard.py verify archive.zip     # integrity check, exit 1 on corruption
python3 zipguard.py info archive.zip
python3 zipguard.py extract archive.zip -o out/
```

## Commands

| Command | What it does |
|---|---|
| `list` | Every member with uncompressed size, compressed size, and compression ratio |
| `verify` | CRC integrity check of every member; names the first corrupt one |
| `info` | Member count, total sizes, overall ratio, largest member |
| `extract -o DIR` | Safe extraction: creates nested directories, refuses escaping members, exits nonzero if any were refused |

Refused members are named on stderr, and the safe members are still
extracted — you get the good files and a clear report of the bad ones.

## Requirements

- Python 3.10+, standard library only

## Notes

- ZipGuard checks *paths*, not content: it does not scan for malware,
  and it does not guard against decompression bombs (a small archive
  expanding to terabytes). Extract archives from untrusted sources in
  a space you can afford to lose.

## Support this work

If this tool saved you time or taught you something, donations keep the work going:

- BTC: 15McijPo79Zx58NGyEf2PvaPtGqGmpztWn
- ETH: 0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B

## License

MIT — see [LICENSE](LICENSE).
