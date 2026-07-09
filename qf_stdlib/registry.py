"""Read-only access to QuantaFoundry registry state."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def json_load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def json_dump_stable(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


@dataclass(frozen=True)
class RegistrySnapshot:
    root: Path
    manifest: dict[str, Any]
    semantic: dict[str, Any]
    dependency_graph: dict[str, Any]
    sealed: dict[str, dict[str, Any]]

    @property
    def registry_root_hash(self) -> str:
        return self.manifest["registry_root_hash"]

    @property
    def unique_apps(self) -> set[str]:
        return set(self.manifest["apps"]["unique"])

    @property
    def cached_leaf_modules(self) -> set[str]:
        return set(self.manifest["apps"].get("cached_leaf_modules", []))

    def ref(self, kind: str, ident: str) -> str:
        return f"{kind}:{ident}"

    def resolve(self, kind: str, ident: str) -> dict[str, Any] | None:
        return self.sealed.get(self.ref(kind, ident))

    def registry_path(self, kind: str, ident: str) -> Path:
        folder = "modules" if kind == "module" else "apps"
        return self.root / "registry" / folder / f"{ident}.sealed.json"

    def semantic_entry(self, kind: str, ident: str) -> dict[str, Any] | None:
        return self.semantic.get("guarantees", {}).get(self.ref(kind, ident))

    def dependencies(self, kind: str, ident: str) -> list[dict[str, Any]]:
        if kind != "app":
            return []
        graph_entry = self.dependency_graph.get(ident, {})
        return list(graph_entry.get("depends_on", []))


def _load_sealed_dir(root: Path, kind: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    folder = root / "registry" / ("modules" if kind == "module" else "apps")
    for path in sorted(folder.glob("*.sealed.json")):
        data = json_load(path)
        out[f"{kind}:{data['id']}"] = data
    return out


def load_snapshot(root: Path | None = None) -> RegistrySnapshot:
    repo = (root or ROOT).resolve()
    manifest = json_load(repo / "registry" / "REGISTRY-MANIFEST.json")
    semantic = json_load(repo / "registry" / "SEMANTIC-GUARANTEES.json")
    dependency_graph = json_load(repo / "registry" / "DEPENDENCY-GRAPH.json")
    sealed: dict[str, dict[str, Any]] = {}
    sealed.update(_load_sealed_dir(repo, "module"))
    sealed.update(_load_sealed_dir(repo, "app"))
    return RegistrySnapshot(
        root=repo,
        manifest=manifest,
        semantic=semantic,
        dependency_graph=dependency_graph,
        sealed=sealed,
    )

