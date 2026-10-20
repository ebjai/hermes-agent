"""Resolve promoted source releases, never infer publication from a Git tag."""
from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
import json
import logging
import re
import subprocess
import urllib.error
import urllib.request

from hermes_cli.update_channel import STABLE_TAG_RE, is_canary_tag

logger = logging.getLogger(__name__)
_PUBLIC_BASE = "https://hermes-assets.nousresearch.com"
# This checkout is the active repository for release metadata and canary publication.
# Keep the official repository identity aligned with the repo that owns the
# published stable/canary channel records.
OFFICIAL_REPOSITORY = "ebjai/hermes-agent"
_GITHUB_ORIGIN = re.compile(
    r"^(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)"
    r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?$", re.IGNORECASE,
)
_SHA = re.compile(r"[0-9a-f]{40}")
