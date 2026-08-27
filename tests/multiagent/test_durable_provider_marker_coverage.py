from __future__ import annotations

import unittest
from unittest.mock import patch

from engine.durable_provider_agent import decode_marker


class DurableProviderMarkerCoverageTests(unittest.TestCase):
    def test_marker_decoder_rejects_a_non_object_json_value(self) -> None:
        marker = '<!-- FACTORY_PROVIDER_RESULT {"status":"success"} -->'
        with patch("engine.durable_provider_agent.json.loads", return_value=[]):
            with self.assertRaisesRegex(ValueError, "payload must be an object"):
                decode_marker(marker, "result")


if __name__ == "__main__":
    unittest.main()
