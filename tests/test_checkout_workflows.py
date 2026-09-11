"""Regression tests for the actions/checkout v7 workflow update.

Run with: python3 -m unittest tests/test_checkout_workflows.py
"""

from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHANGED_WORKFLOWS = (
    REPOSITORY_ROOT / ".github/workflows/ci.yml",
    REPOSITORY_ROOT / ".github/workflows/openrabbitai.yml",
)
CHECKOUT_REFERENCE = "actions/checkout@"
CHECKOUT_STEP = re.compile(
    r"^(?P<indent> +)-\s+uses:\s+"
    r"(?P<quote>['\"]?)actions/checkout@(?P<version>[^\s'\"#]+)"
    r"(?P=quote)(?:\s+#.*)?$"
)


def active_checkout_lines(workflow: Path):
    """Return line-numbered, non-comment checkout references from a workflow."""
    references = []
    for line_number, line in enumerate(workflow.read_text().splitlines(), start=1):
        if CHECKOUT_REFERENCE in line and not line.lstrip().startswith("#"):
            references.append((line_number, line))
    return references


class CheckoutWorkflowTests(unittest.TestCase):
    def test_changed_workflows_still_contain_a_checkout_step(self):
        """Prevent a missing action from making the version assertions vacuous."""
        for workflow in CHANGED_WORKFLOWS:
            with self.subTest(workflow=workflow.name):
                self.assertTrue(
                    active_checkout_lines(workflow),
                    f"{workflow} no longer contains an active checkout step",
                )

    def test_checkout_references_are_well_formed_steps(self):
        for workflow in CHANGED_WORKFLOWS:
            for line_number, line in active_checkout_lines(workflow):
                with self.subTest(workflow=workflow.name, line=line_number):
                    self.assertIsNotNone(
                        CHECKOUT_STEP.fullmatch(line),
                        f"{workflow}:{line_number} is not a valid checkout step: {line!r}",
                    )

    def test_all_checkout_steps_use_v7(self):
        """Catch partial upgrades when a workflow contains multiple jobs."""
        for workflow in CHANGED_WORKFLOWS:
            for line_number, line in active_checkout_lines(workflow):
                match = CHECKOUT_STEP.fullmatch(line)
                with self.subTest(workflow=workflow.name, line=line_number):
                    self.assertIsNotNone(match, f"Malformed checkout step: {line!r}")
                    self.assertEqual(
                        match.group("version"),
                        "v7",
                        f"{workflow}:{line_number} still uses {match.group('version')}",
                    )

    def test_checkout_steps_are_nested_under_steps(self):
        """Reject merge residue that detaches an upgraded action from its job."""
        for workflow in CHANGED_WORKFLOWS:
            lines = workflow.read_text().splitlines()
            for line_number, line in active_checkout_lines(workflow):
                match = CHECKOUT_STEP.fullmatch(line)
                with self.subTest(workflow=workflow.name, line=line_number):
                    self.assertIsNotNone(match, f"Malformed checkout step: {line!r}")
                    step_indent = len(match.group("indent"))
                    parent = next(
                        (
                            candidate.strip()
                            for candidate in reversed(lines[: line_number - 1])
                            if candidate.strip()
                            and len(candidate) - len(candidate.lstrip()) < step_indent
                        ),
                        None,
                    )
                    self.assertEqual(
                        parent,
                        "steps:",
                        f"{workflow}:{line_number} is not nested directly under steps",
                    )


if __name__ == "__main__":
    unittest.main()
