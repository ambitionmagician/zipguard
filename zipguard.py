#!/usr/bin/env python3
import argparse
import os
import sys
import zipfile
from pathlib import Path


def cmd_list(args):
    try:
        with zipfile.ZipFile(args.archive, 'r') as zf:
            for info in zf.infolist():
                ratio = (1 - info.compress_size / info.file_size) * 100 if info.file_size > 0 else 0
                print(f"{info.filename}\t{info.file_size}\t{info.compress_size}\t{ratio:.1f}%")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_verify(args):
    try:
        with zipfile.ZipFile(args.archive, 'r') as zf:
            bad = zf.testzip()
            if bad is None:
                print("OK")
            else:
                print(f"Corrupt member: {bad}", file=sys.stderr)
                sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_extract(args):
    try:
        with zipfile.ZipFile(args.archive, 'r') as zf:
            base = Path(args.output).resolve()
            base.mkdir(parents=True, exist_ok=True)
            refused = []
            for info in zf.infolist():
                target = (base / info.filename).resolve()
                try:
                    target.relative_to(base)
                except ValueError:
                    refused.append(info.filename)
                    continue
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(info) as src, open(target, 'wb') as dst:
                    dst.write(src.read())
            if refused:
                for name in refused:
                    print(f"Refused: {name}", file=sys.stderr)
                sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_info(args):
    try:
        with zipfile.ZipFile(args.archive, 'r') as zf:
            infos = zf.infolist()
            count = len(infos)
            total_uncompressed = sum(i.file_size for i in infos)
            total_compressed = sum(i.compress_size for i in infos)
            ratio = (1 - total_compressed / total_uncompressed) * 100 if total_uncompressed > 0 else 0
            largest = max(infos, key=lambda x: x.file_size) if infos else None
            print(f"Member count: {count}")
            print(f"Total uncompressed: {total_uncompressed}")
            print(f"Total compressed: {total_compressed}")
            print(f"Overall ratio: {ratio:.1f}%")
            if largest:
                print(f"Largest member: {largest.filename} ({largest.file_size} bytes)")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="ZIP archive utility")
    subparsers = parser.add_subparsers(dest='command', required=True)

    sp_list = subparsers.add_parser('list', help='List archive contents')
    sp_list.add_argument('archive', help='ZIP archive file')
    sp_list.set_defaults(func=cmd_list)

    sp_verify = subparsers.add_parser('verify', help='Verify archive integrity')
    sp_verify.add_argument('archive', help='ZIP archive file')
    sp_verify.set_defaults(func=cmd_verify)

    sp_extract = subparsers.add_parser('extract', help='Extract archive safely')
    sp_extract.add_argument('archive', help='ZIP archive file')
    sp_extract.add_argument('-o', '--output', required=True, help='Output directory')
    sp_extract.set_defaults(func=cmd_extract)

    sp_info = subparsers.add_parser('info', help='Show archive summary')
    sp_info.add_argument('archive', help='ZIP archive file')
    sp_info.set_defaults(func=cmd_info)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
