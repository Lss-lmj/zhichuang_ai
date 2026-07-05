from __future__ import annotations

import os
import tempfile

TEST_DB_DIR = tempfile.mkdtemp(prefix="zhichuang-test-")

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    f"sqlite:///{TEST_DB_DIR}/test.db",
)
os.environ.setdefault("SCHOOL_IDENTITY_SHARED_SECRET", "dev-school-identity-secret")
