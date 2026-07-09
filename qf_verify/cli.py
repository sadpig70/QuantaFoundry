# -*- coding: utf-8 -*-
"""cli — python -m qf_verify {run,list-steps,explain,write-claim-map}."""
import sys
import argparse


def main(argv=None):
    p = argparse.ArgumentParser(prog="qf_verify",
                                description="manifest-driven verification runner")
    sub = p.add_subparsers(dest="cmd", required=True)
    runp = sub.add_parser("run", help="run a verification profile")
    runp.add_argument("--profile", required=True, choices=["full", "changed"])
    sub.add_parser("list-steps", help="list all steps across profiles")
    exp = sub.add_parser("explain", help="explain a claim")
    exp.add_argument("--claim", required=True)
    sub.add_parser("write-claim-map", help="generate reports/CLAIM-EVIDENCE-MAP.md")
    args = p.parse_args(argv)

    if args.cmd == "run":
        from . import runner
        _, _, code = runner.run_profile(args.profile)
        return code
    if args.cmd == "list-steps":
        from . import manifest as mf
        steps, changed = mf.load_profile("full")
        for st in steps:
            kind = f"special:{st['special']}" if "special" in st else " ".join(st["argv"][:2])
            print(f"{st['id']:38s} [{st.get('_group','?'):9s}] {kind}")
        print(f"-- {len(steps)} steps (profile=full)")
        return 0
    if args.cmd == "explain":
        from . import claims
        print(claims.explain(args.claim))
        return 0
    if args.cmd == "write-claim-map":
        from . import claims
        print("→", claims.write_claim_map())
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
