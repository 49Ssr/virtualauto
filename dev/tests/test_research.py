from __future__ import annotations

import unittest

from virtualauto.research import find_sections, get_section


class ResearchRetrievalTests(unittest.TestCase):
    def test_resolves_exact_canonical_key_with_provenance(self) -> None:
        result = get_section("ABR-COMP-010")
        self.assertEqual(result["section"]["canonical_key"], "ABR-COMP-010")
        self.assertIn("Node architecture", result["content"])
        self.assertRegex(result["source_sha256"], "^[a-f0-9]{64}$")

    def test_find_defaults_to_canonical_sections(self) -> None:
        results = find_sections("weave", prefix="ABR-COMP")
        self.assertTrue(results)
        self.assertTrue(
            all(result["canonical_key"].startswith("ABR-COMP") for result in results)
        )


if __name__ == "__main__":
    unittest.main()
