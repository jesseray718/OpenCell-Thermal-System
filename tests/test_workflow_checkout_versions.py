"""Regression tests for the actions/checkout v7 workflow upgrade."""

from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_UNDER_TEST = (
    REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml",
    REPOSITORY_ROOT / ".github" / "workflows" / "openrabbitai.yml",
)

CHECKOUT_REFERENCE = re.compile(r"actions/checkout@(?P<version>[^\s#'\"]+)")
CHECKOUT_STEP = re.compile(
    r"^\s*-\s+uses:\s+actions/checkout@[A-Za-z0-9._/-]+(?:\s+#.*)?$"
)
MERGE_DEBRIS = re.compile(
    r"^\s*(?:<{7}.*|={7}|>{7}.*|main|master|"
    r"(?:dependabot|chore|feature|fix|hotfix|release)/\S+)\s*$"
)


def workflow_lines(path):
    """Return numbered lines so failures identify the exact workflow entry."""
    return tuple(enumerate(path.read_text(encoding="utf-8").splitlines(), start=1))


class CheckoutWorkflowTests(unittest.TestCase):
    def test_changed_workflows_contain_checkout_steps(self):
        """Prevent an absent checkout step from making version checks vacuous."""
        for workflow in WORKFLOWS_UNDER_TEST:
            with self.subTest(workflow=workflow.name):
                references = [
                    (line_number, line)
                    for line_number, line in workflow_lines(workflow)
                    if "actions/checkout@" in line
                ]
                self.assertTrue(
                    references,
                    f"{workflow.name} must contain an actions/checkout step",
                )

    def test_all_checkout_references_use_v7(self):
        """Reject stale or accidentally reintroduced checkout action versions."""
        for workflow in WORKFLOWS_UNDER_TEST:
            unexpected_versions = []
            for line_number, line in workflow_lines(workflow):
                for match in CHECKOUT_REFERENCE.finditer(line):
                    if match.group("version") != "v7":
                        unexpected_versions.append(
                            (line_number, match.group("version"))
                        )

            with self.subTest(workflow=workflow.name):
                self.assertEqual([], unexpected_versions)

    def test_checkout_references_are_valid_step_entries(self):
        """Catch malformed upgrade lines that mention v7 but cannot run as a step."""
        for workflow in WORKFLOWS_UNDER_TEST:
            malformed_references = [
                (line_number, line)
                for line_number, line in workflow_lines(workflow)
                if "actions/checkout@" in line and not CHECKOUT_STEP.fullmatch(line)
            ]

            with self.subTest(workflow=workflow.name):
                self.assertEqual([], malformed_references)

    def test_changed_workflows_have_no_merge_debris(self):
        """Guard against branch labels or conflict markers corrupting workflow YAML."""
        for workflow in WORKFLOWS_UNDER_TEST:
            debris = [
                (line_number, line)
                for line_number, line in workflow_lines(workflow)
                if MERGE_DEBRIS.fullmatch(line)
            ]

            with self.subTest(workflow=workflow.name):
                self.assertEqual([], debris)


if __name__ == "__main__":
    unittest.main()
