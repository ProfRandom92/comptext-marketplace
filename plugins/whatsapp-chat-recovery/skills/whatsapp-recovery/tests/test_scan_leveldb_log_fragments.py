from __future__ import annotations

import struct
import tempfile
import unittest
from pathlib import Path

from scan_leveldb_log_fragments import (
    crc32c,
    masked_crc32c,
    scan_file,
)


def physical_record(record_type: int, payload: bytes) -> bytes:
    header_input = bytes([record_type]) + payload
    return struct.pack("<IHB", masked_crc32c(header_input), len(payload), record_type) + payload


class LevelDBFragmentScannerTests(unittest.TestCase):
    def scan_bytes(self, data: bytes, **kwargs) -> dict:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "fragment.bin"
            path.write_bytes(data)
            return scan_file(path, **kwargs)

    def test_crc32c_standard_check_value(self) -> None:
        self.assertEqual(crc32c(b"123456789"), 0xE3069283)

    def test_finds_valid_record_inside_unaligned_fragment(self) -> None:
        payload = b"writebatch WebEncKeySalt"
        fragment = b"prefix-bytes" + physical_record(1, payload) + b"trailer"
        result = self.scan_bytes(fragment, identifiers=["WebEncKeySalt"])
        self.assertTrue(result["read_only"])
        self.assertEqual(result["valid_physical_records"], 1)
        self.assertEqual(result["records"][0]["offset"], len(b"prefix-bytes"))
        self.assertEqual(result["identifier_hit_counts"]["WebEncKeySalt"], 1)
        self.assertNotIn(payload.decode(), str(result))

    def test_rejects_corrupt_checksum(self) -> None:
        record = bytearray(physical_record(1, b"synthetic"))
        record[0] ^= 0x01
        result = self.scan_bytes(bytes(record))
        self.assertEqual(result["valid_physical_records"], 0)

    def test_known_source_offset_rejects_cross_block_record(self) -> None:
        record = physical_record(1, b"x" * 32)
        unknown_alignment = self.scan_bytes(record)
        known_alignment = self.scan_bytes(record, source_offset=32760)
        self.assertEqual(unknown_alignment["valid_physical_records"], 1)
        self.assertEqual(known_alignment["valid_physical_records"], 0)

    def test_scan_limit_is_reported(self) -> None:
        record = physical_record(1, b"too-late")
        result = self.scan_bytes(b"x" * 20 + record, max_bytes=10)
        self.assertTrue(result["scan_truncated"])
        self.assertEqual(result["scanned_bytes"], 10)


if __name__ == "__main__":
    unittest.main()
