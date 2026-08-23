from __future__ import annotations

import unittest

from engine.semantic_assurance import formal_method_recommendations


def recommendation_kinds(assurance: dict[str, object]) -> set[str]:
    return {
        item["kind"]
        for item in formal_method_recommendations(assurance)
    }


class FormalRecommendationTests(unittest.TestCase):
    def test_generic_validation_policy_does_not_recommend_policy_engine(self) -> None:
        assurance = {
            "depth": "domain",
            "requirements": [
                {
                    "id": "REQ-001",
                    "pattern": "policy",
                    "component": "Backup restore",
                    "scope": ["local repository"],
                    "preconditions": ["a backup file was selected"],
                    "trigger": "the user requests restore",
                    "response": ["reject an invalid backup without replacing current data"],
                }
            ],
            "constraints": [],
            "relations": [],
            "transitions": [],
        }

        self.assertNotIn("opa-or-cedar", recommendation_kinds(assurance))

    def test_authorization_policy_can_recommend_policy_engine(self) -> None:
        assurance = {
            "depth": "domain",
            "requirements": [
                {
                    "id": "REQ-001",
                    "pattern": "policy",
                    "component": "Authorization policy",
                    "scope": ["protected administrative actions"],
                    "preconditions": ["the user has an authenticated role"],
                    "trigger": "a role without permission attempts the action",
                    "response": ["deny access according to authorization policy"],
                }
            ],
            "constraints": [],
            "relations": [],
            "transitions": [],
        }

        self.assertIn("opa-or-cedar", recommendation_kinds(assurance))


if __name__ == "__main__":
    unittest.main()
