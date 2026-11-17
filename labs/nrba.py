"""Shared helpers of the AE-407 labs (Northern Region Benefits Agency, synthetic data).

    import nrba as U

U.DATA, U.ART          labs/data and labs/artifacts (lab outputs, not committed)
U.QUICK, U.pick(a, b)  quick mode (AE407_QUICK=1): b in place of a
U.load(name)           a .json or .jsonl file of labs/data
U.reference(name)      the reference result of an exercise, for the safety-net cells
U.keep(name, obj)      returns obj; with AE407_WRITE_REF=1 also writes it as the reference result
U.check(ok, msg)       prints a tick, or raises AssertionError with the message
U.show(rows)           a list of dicts as a text table
U.wilson(k, n)         the 95% Wilson interval of k successes in n trials
U.rate(k, n)           "3/10 = 30% [11%, 60%]"
U.level(l, i), U.band(level)   the national 4 by 4 matrix: level = likelihood x impact, and its band
U.checklist(items)     prints a checklist of (text, passed) and returns the number that failed
U.review_plan, U.review_context, U.review_statement   the three checklists a reviewer applies
U.save(name, text)     write a lab output under labs/artifacts/
"""

from __future__ import annotations

import json as _json
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
REF = DATA / "reference"
ART = HERE / "artifacts"
QUICK = os.environ.get("AE407_QUICK", "0") == "1"
LIKELIHOOD = {1: "rare", 2: "unlikely", 3: "likely", 4: "almost certain"}
IMPACT = {1: "low", 2: "medium", 3: "high", 4: "catastrophic"}
BUDGET = 600  # the fixed budget of model calls of the exercise
JARGON = ["prompt injection", "exfiltrat", "jailbreak", "llm", "goal hijack", "egress", "token"]


def pick(full, quick):
    return quick if QUICK else full


def load(name: str):
    text = (DATA / name).read_text(encoding="utf-8")
    if name.endswith(".jsonl"):
        return [_json.loads(line) for line in text.splitlines() if line.strip()]
    return _json.loads(text)


def reference(name: str):
    """The reference result of exercise `name`, so later cells run when it is not done yet."""
    print(f"(safety net: using the reference result for {name})")
    return _json.loads((REF / f"{name}.json").read_text(encoding="utf-8"))


def keep(name: str, obj):
    if os.environ.get("AE407_WRITE_REF") == "1":
        REF.mkdir(parents=True, exist_ok=True)
        (REF / f"{name}.json").write_text(_json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return obj


def check(ok, message: str):
    if not ok:
        raise AssertionError("❌ " + message)
    print("✅ " + message)


def show(rows, columns=None, width: int = 60):
    rows = list(rows)
    if not rows:
        print("(no rows)")
        return
    columns = columns or list(rows[0])
    cells = [[str(r.get(c, ""))[:width] for c in columns] for r in rows]
    sizes = [max(len(c), *(len(row[i]) for row in cells)) for i, c in enumerate(columns)]
    print("  ".join(c.ljust(s) for c, s in zip(columns, sizes)))
    print("  ".join("-" * s for s in sizes))
    for row in cells:
        print("  ".join(v.ljust(s) for v, s in zip(row, sizes)))


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def rate(k: int, n: int) -> str:
    low, high = wilson(k, n)
    return f"{k}/{n} = {k / n:.0%} [{low:.0%}, {high:.0%}]"


def level(likelihood: int, impact: int) -> int:
    return likelihood * impact


def band(lvl: int) -> str:
    return "catastrophic" if lvl >= 16 else "high" if lvl >= 8 else "medium" if lvl >= 3 else "low"


def save(name: str, text: str) -> Path:
    path = ART / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def checklist(items) -> int:
    """Print (text, passed) pairs as a checklist. Returns how many failed."""
    failed = 0
    for text, ok in items:
        print(("  [x] " if ok else "  [ ] ") + text)
        failed += 0 if ok else 1
    print(f"{len(items) - failed} of {len(items)} items pass")
    return failed


def _filled(value) -> bool:
    return bool(value) and (not isinstance(value, str) or len(value.strip()) >= 8)


def review_plan(plan: dict) -> list:
    """The planning checklist the head of AI assurance applies to a red-team test plan."""
    objectives = plan.get("objectives", [])
    scope, stops, harmful, roles = plan.get("scope", {}), plan.get("stop_conditions", []), plan.get("harmful_outputs", {}), plan.get("roles", {})
    text = " ".join(str(o.get("harm", "")) for o in objectives).lower()
    stop_text = " ".join(stops).lower()
    return [
        ("At least four objectives, each with a target, a harm and a success check",
         len(objectives) >= 4 and all(_filled(o.get("harm")) and _filled(o.get("success_check")) and o.get("target") in ("mueen", "katib") for o in objectives)),
        ("Every success check is decided by something observable, never by what the model says about itself",
         bool(objectives) and all(_filled(o.get("decided_by")) and "model says" not in str(o.get("decided_by")).lower() for o in objectives)),
        ("One objective is about unfair or degrading treatment of applicants, beside data leakage",
         any(w in text for w in ("unfair", "degrad", "dignity", "discriminat"))),
        ("Both targets are in scope and at least two things are named out of scope, production among them",
         set(scope.get("targets", [])) == {"mueen", "katib"} and len(scope.get("out_of_scope", [])) >= 2
         and any("production" in str(x).lower() for x in scope.get("out_of_scope", []))),
        ("English, Arabic and transliterated Arabic are all in scope", {"en", "ar", "arabizi"} <= set(scope.get("scripts", []))),
        (f"A budget of model calls is stated and is at most {BUDGET}", isinstance(plan.get("budget_calls"), int) and 0 < plan["budget_calls"] <= BUDGET),
        ("At least three stop conditions, one for real personal data and one for anything leaving the sandbox",
         len(stops) >= 3 and "real" in stop_text and "sandbox" in stop_text),
        ("Harmful outputs: where they are stored, who may read them and when they are deleted",
         all(_filled(harmful.get(k)) for k in ("stored", "access", "deleted"))),
        ("The lead and the tester are named, and the tester did not build the system",
         _filled(roles.get("lead")) and _filled(roles.get("tester")) and roles.get("tester") != roles.get("builder")),
        ("Case data keeps its classification level: the plan names the level and where data may go",
         "restricted" in str(plan.get("data_handling", "")).lower()),
    ]


def review_context(ctx: dict) -> list:
    """The context-and-scope checklist: the four activities of the national framework's first step."""
    system, data, human, life = ctx.get("system", {}), ctx.get("data", {}), ctx.get("automation", {}), ctx.get("lifecycle", {})
    return [
        ("System: what it is, its purpose and how its output is used", _filled(system.get("description")) and _filled(system.get("output_use"))),
        ("At least three intended uses and three uses out of scope", len(system.get("intended_uses", [])) >= 3 and len(system.get("out_of_scope", [])) >= 3),
        ("Direct users and affected people are named separately", _filled(system.get("users")) and _filled(system.get("affected"))),
        ("Data: each kind with its classification level", len(data.get("data", [])) >= 2 and all(_filled(d.get("level")) for d in data.get("data", []))),
        ("Entry points and exit points are listed", len(data.get("entry_points", [])) >= 2 and len(data.get("exit_points", [])) >= 2),
        ("Parties in the value chain with their roles, the supplier among them",
         len(data.get("parties", [])) >= 3 and any("supplier" in str(p).lower() or "lisan" in str(p).lower() for p in data.get("parties", []))),
        ("Level of automation: recommends, decides or acts", human.get("level") in ("recommends", "decides", "acts")),
        ("Human decision points, with at least one where a person must act", len(human.get("decision_points", [])) >= 2 and _filled(human.get("mandatory"))),
        ("Responsibilities: developer, operator, decision owner and the escalation path",
         all(_filled(human.get("responsibilities", {}).get(k)) for k in ("developer", "operator", "decision_owner", "escalation"))),
        ("Life-cycle stage and the change plan: what changes, how often, who approves", _filled(life.get("stage")) and len(life.get("changes", [])) >= 2
         and all(_filled(c.get("approver")) for c in life.get("changes", []))),
        ("What triggers a new risk assessment", _filled(life.get("reassess_when"))),
    ]


def words(obj) -> int:
    if isinstance(obj, dict):
        return sum(words(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(words(v) for v in obj)
    return len(str(obj).split()) if isinstance(obj, str) else 0


def review_statement(page: dict, pack: dict) -> list:
    """The briefing checklist for a one-page residual-risk statement."""
    risks, conds = page.get("residual_risks", []), page.get("conditions", [])
    top = [r["risk"] for r in sorted(pack["residual"], key=lambda r: -r["residual"])[:3]]
    flat = _json.dumps(page, ensure_ascii=False).lower()
    return [
        ("One page: at most 300 words", 0 < words(page) <= 300),
        ("A decision is requested and a recommendation given: go, go with conditions or hold", page.get("recommendation") in ("go", "go with conditions", "hold") and _filled(page.get("decision_requested"))),
        ("The three highest residual risks are on the page, each in plain words with its level", all(any(r.get("risk") == t and _filled(r.get("plain_words")) and r.get("level") for r in risks) for t in top)),
        ("Each stated level equals the pack's residual level", bool(risks) and all(r.get("level") == next((p["residual"] for p in pack["residual"] if p["risk"] == r.get("risk")), None) for r in risks)),
        ("Every condition has an owner from the Agency and a number of days", bool(conds) and all(c.get("owner") in pack["people"] and isinstance(c.get("due_days"), int) for c in conds)),
        ("Every control that is not live yet is a condition", page.get("recommendation") != "go with conditions" or len(conds) >= 3),
        ("What was not tested is said", len(page.get("not_tested", [])) >= 2),
        ("No specialist jargon: " + ", ".join(JARGON[:4]) + " and the like", not any(j in flat for j in JARGON)),
        ("The accountable executive signs, and a review date is set", page.get("signatory") == pack["accountable_executive"] and isinstance(page.get("review_days"), int)),
    ]
