"""QF stdlib CLI.

Read-only by default. The only commands that write files are `build-canon`
and `validate-canon --write-report`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qf_stdlib.attest import attest
from qf_stdlib.adapters import adapter_convention
from qf_stdlib.canon import build_canon, check_root, load_canon, lookup, validate_canon, write_report
from qf_stdlib.errors import AdapterConventionError, NotFoundError, QFStdlibError, UnsupportedAdapter, ValidationError
from qf_stdlib.registry import json_dump_stable, load_snapshot
from qf_stdlib.templates import build_with_proof, load_template, validate_template


def _print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def cmd_build_canon(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(ROOT)
    canon = build_canon(snapshot)
    report = validate_canon(canon, snapshot)
    if not report.ok:
        _print_json(report.to_json())
        return 1
    out = Path(args.out) if args.out else ROOT / "registry" / "CANON.json"
    if not out.is_absolute():
        out = ROOT / out
    json_dump_stable(canon, out)
    if args.write_report:
        write_report(report, ROOT)
    print(f"CANON written: {out.relative_to(ROOT)} entries={report.entries} root={report.registry_root_hash[:16]}..")
    return 0


def cmd_validate_canon(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(ROOT)
    canon = load_canon(ROOT)
    report = validate_canon(canon, snapshot)
    if args.write_report:
        write_report(report, ROOT)
    _print_json(report.to_json())
    return 0 if report.ok else 1


def cmd_check_root(_args: argparse.Namespace) -> int:
    snapshot = load_snapshot(ROOT)
    canon = load_canon(ROOT)
    report = check_root(canon, snapshot)
    _print_json(report.to_json())
    return 0 if report.ok else 1


def cmd_list(_args: argparse.Namespace) -> int:
    canon = load_canon(ROOT)
    for key in sorted(canon.get("canon", {})):
        entry = canon["canon"][key]
        print(f"{key}\t{entry['kind']}:{entry['id']}\t{entry['semantic_guarantee']}")
    return 0


def cmd_lookup(args: argparse.Namespace) -> int:
    entry = lookup(args.query, root=ROOT)
    if entry is None:
        return 3
    _print_json(entry)
    return 0


def cmd_attest(args: argparse.Namespace) -> int:
    if args.adapter:
        if args.adapter.lower() == "cirq":
            raise UnsupportedAdapter("cirq adapter requires Python API circuit input; CLI attest remains lookup-only")
        raise UnsupportedAdapter(args.adapter)
    data = attest(args.query, root=ROOT)
    if data is None:
        return 3
    _print_json(data)
    return 0


def cmd_validate_template(args: argparse.Namespace) -> int:
    canon = load_canon(ROOT)
    template = load_template(args.template_id, root=ROOT)
    errors = validate_template(template, canon=canon, root=ROOT)
    result = {"ok": not errors, "errors": errors, "template_id": args.template_id}
    _print_json(result)
    return 0 if not errors else 1


def cmd_build_template(args: argparse.Namespace) -> int:
    cert = build_with_proof(args.template_id, root=ROOT)
    _print_json(cert)
    return 0


def cmd_adapter_info(args: argparse.Namespace) -> int:
    _print_json(adapter_convention(args.adapter))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="QF stdlib sidecar/lookup CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("build-canon", help="generate registry/CANON.json from the live registry")
    p.add_argument("--out", default="registry/CANON.json")
    p.add_argument("--write-report", action="store_true")
    p.set_defaults(func=cmd_build_canon)

    p = sub.add_parser("validate-canon", help="validate registry/CANON.json against live registry state")
    p.add_argument("--write-report", action="store_true")
    p.set_defaults(func=cmd_validate_canon)

    p = sub.add_parser("check-root", help="fail if CANON.json root differs from the live registry manifest root")
    p.set_defaults(func=cmd_check_root)

    p = sub.add_parser("list", help="list canonical stdlib keys")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("lookup", help="lookup by key, alias, id, or exact u_hash")
    p.add_argument("query")
    p.set_defaults(func=cmd_lookup)

    p = sub.add_parser("attest", help="emit lookup attestation for a canonical entry")
    p.add_argument("query")
    p.add_argument("--adapter", default=None, help="reserved for future exact circuit adapters")
    p.set_defaults(func=cmd_attest)

    p = sub.add_parser("validate-template", help="validate a proof-carrying template")
    p.add_argument("template_id")
    p.set_defaults(func=cmd_validate_template)

    p = sub.add_parser("build-template", help="emit a derived template certificate")
    p.add_argument("template_id")
    p.set_defaults(func=cmd_build_template)

    p = sub.add_parser("adapter-info", help="show a pinned adapter convention")
    p.add_argument("adapter")
    p.set_defaults(func=cmd_adapter_info)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except UnsupportedAdapter as exc:
        print(f"unsupported_adapter: {exc}", file=sys.stderr)
        return 2
    except AdapterConventionError as exc:
        print(f"adapter_convention_error: {exc}", file=sys.stderr)
        return 2
    except NotFoundError as exc:
        print(f"not_found: {exc}", file=sys.stderr)
        return 3
    except ValidationError as exc:
        print(f"validation_error: {exc}", file=sys.stderr)
        return 1
    except QFStdlibError as exc:
        print(f"qf_stdlib_error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
