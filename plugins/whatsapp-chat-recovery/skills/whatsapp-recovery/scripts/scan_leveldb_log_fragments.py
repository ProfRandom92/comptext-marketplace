#!/usr/bin/env python3
"""Read-only scan for CRC32C-valid LevelDB log physical records in a file fragment.

The scanner reports offsets, record types, lengths, and exact identifier hit counts.
It never prints payload bytes, writes recovered data, or modifies the input.
"""
from __future__ import annotations

import argparse
import json
import mmap
from pathlib import Path

HEADER_SIZE = 7
LEVELDB_BLOCK_SIZE = 32 * 1024
MAX_RECORD_SIZE = LEVELDB_BLOCK_SIZE - HEADER_SIZE
MAX_SCAN_BYTES = 64 * 1024 * 1024
MAX_REPORTED_RECORDS = 100
TYPE_NAMES = {1: "FULL", 2: "FIRST", 3: "MIDDLE", 4: "LAST"}
MASK_DELTA = 0xA282EAD8


def _crc_table() -> tuple[int, ...]:
    values = []
    for value in range(256):
        crc = value
        for _ in range(8):
            crc = (crc >> 1) ^ (0x82F63B78 if crc & 1 else 0)
        values.append(crc)
    return tuple(values)


CRC_TABLE = _crc_table()


def crc32c(data: bytes | memoryview) -> int:
    crc = 0xFFFFFFFF
    for byte in data:
        crc = CRC_TABLE[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF


def masked_crc32c(data: bytes | memoryview) -> int:
    crc = crc32c(data)
    return (((crc >> 15) | (crc << 17)) + MASK_DELTA) & 0xFFFFFFFF


def scan_file(
    path: Path,
    identifiers: list[str] | None = None,
    source_offset: int | None = None,
    max_bytes: int = MAX_SCAN_BYTES,
) -> dict:
    identifiers = identifiers or []
    needles = {value: value.encode("utf-8") for value in identifiers if value}
    size = path.stat().st_size
    limit = min(size, max_bytes)
    records = []
    record_count = 0
    identifier_totals = {value: 0 for value in needles}

    if limit == 0:
        return {
            "read_only": True,
            "path": str(path),
            "file_size_bytes": size,
            "scanned_bytes": 0,
            "scan_truncated": size > 0,
            "source_offset_known": source_offset is not None,
            "valid_physical_records": 0,
            "identifier_hit_counts": identifier_totals,
            "records": records,
        }

    with path.open("rb") as stream:
        with mmap.mmap(stream.fileno(), length=limit, access=mmap.ACCESS_READ) as data:
            for offset in range(max(0, limit - HEADER_SIZE + 1)):
                record_type = data[offset + 6]
                if record_type not in TYPE_NAMES:
                    continue
                length = data[offset + 4] | (data[offset + 5] << 8)
                end = offset + HEADER_SIZE + length
                if length > MAX_RECORD_SIZE or end > limit:
                    continue
                if source_offset is not None:
                    block_offset = (source_offset + offset) % LEVELDB_BLOCK_SIZE
                    if block_offset + HEADER_SIZE + length > LEVELDB_BLOCK_SIZE:
                        continue
                stored_crc = int.from_bytes(data[offset : offset + 4], "little")
                if masked_crc32c(memoryview(data)[offset + 6 : end]) != stored_crc:
                    continue

                record_count += 1
                payload = data[offset + HEADER_SIZE : end]
                hits = {}
                for identifier, needle in needles.items():
                    count = payload.count(needle)
                    if count:
                        identifier_totals[identifier] += count
                        hits[identifier] = count
                if len(records) < MAX_REPORTED_RECORDS:
                    records.append(
                        {
                            "offset": offset,
                            "type": TYPE_NAMES[record_type],
                            "length": length,
                            "identifier_hits": hits,
                        }
                    )

    return {
        "read_only": True,
        "path": str(path),
        "file_size_bytes": size,
        "scanned_bytes": limit,
        "scan_truncated": limit < size,
        "source_offset_known": source_offset is not None,
        "valid_physical_records": record_count,
        "records_reported": len(records),
        "records_report_limit": MAX_REPORTED_RECORDS,
        "identifier_hit_counts": identifier_totals,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="One candidate binary file or fragment")
    parser.add_argument("--identifier", action="append", default=[], help="Exact UTF-8 byte string to count in valid record payloads; repeatable")
    parser.add_argument("--source-offset", type=int, help="Known byte offset of this fragment in its original LevelDB log; enables 32-KB boundary validation")
    parser.add_argument("--max-bytes", type=int, default=MAX_SCAN_BYTES, help="Maximum bytes to scan (default: 64 MiB)")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()
    if args.max_bytes <= 0:
        parser.error("--max-bytes must be greater than zero")
    if args.source_offset is not None and args.source_offset < 0:
        parser.error("--source-offset cannot be negative")
    if not args.path.is_file():
        parser.error(f"not a regular file: {args.path}")
    result = scan_file(args.path, args.identifier, args.source_offset, args.max_bytes)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            f"read_only=True valid_physical_records={result['valid_physical_records']} "
            f"scanned_bytes={result['scanned_bytes']} scan_truncated={result['scan_truncated']}"
        )
        for record in result["records"]:
            print(
                f"  offset={record['offset']} type={record['type']} length={record['length']} "
                f"identifier_hits={record['identifier_hits']}"
            )
        for identifier, count in result["identifier_hit_counts"].items():
            print(f"  exact_identifier_hit_count {identifier!r}: {count}")
        if result["scan_truncated"]:
            print("  scan limit reached; increase --max-bytes to examine the remaining file")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
