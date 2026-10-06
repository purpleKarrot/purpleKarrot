"""Fix repository pagination in the pinned Metrics action before building it."""

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
    target = Path(sys.argv[1]) / "source/plugins/base/index.mjs"
    target.write_text(patch(target.read_text()))
