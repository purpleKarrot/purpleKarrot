"""Patch pinned Metrics and layer the fix onto its official runtime image."""

from pathlib import Path
import sys


def patch(source: str) -> str:
    replacements = {
        "        do {\n": "        while (data.user[type].nodes.length < repositories) {\n",
        "          if (pushed < repositories) {": "          if (!cursor || pushed < Math.min(repositories, account === \"organization\" ? Math.min(25, _batch) : _batch)) {",
        "        while ((pushed) && (cursor) && ((data.user.repositories?.nodes?.length ?? 0) + (data.user.repositoriesContributedTo?.nodes?.length ?? 0) < repositories))": "",
    }
    for old, new in replacements.items():
        if source.count(old) != 1:
            raise RuntimeError(f"Pinned Metrics source changed; expected one match for {old!r}")
        source = source.replace(old, new)
    return source


if __name__ == "__main__":
    checkout = Path(sys.argv[1])
    target = checkout / "source/plugins/base/index.mjs"
    target.write_text(patch(target.read_text()))
    # Reuse the working dependencies instead of rebuilding the old Dockerfile.
    # The image version matches the pinned Metrics 3.34.0 source in metric.yml.
    (checkout / "Dockerfile").write_text(
        "FROM ghcr.io/lowlighter/metrics:v3.34\n"
        "COPY source/plugins/base/index.mjs /metrics/source/plugins/base/index.mjs\n"
    )
