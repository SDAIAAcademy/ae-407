# %% [markdown]
# # Lab 4.3 · Evidence, controls and gaps
#
# Day 4 · Session 3 (Assurance evidence packs) · 25 min.
#
# Fourteen pieces of evidence have come out of four days of work, some of them yours and some
# the builders'. You map each to the controls of a framework it supports, find the controls with
# no evidence or with evidence too weak to carry a claim, link the evidence to the claims of the
# assurance case, and write the gap list an auditor would raise, before the auditor does.
#
# **Tasks**
# - [ ] Read the evidence set and the framework extract (5 min)
# - [ ] Map each evidence item to the controls it supports (8 min)
# - [ ] List the controls with no evidence or weak evidence (6 min)
# - [ ] Link evidence to claims and write the gap list (6 min)
# - [ ] ✱ Stretch · Map the same evidence to the control library of the Agency and compare the two gap lists
# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ae-407.git"
    if not Path("/content/ae-407").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ae-407"], check=True)
    os.chdir("/content/ae-407/labs")
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import nrba as U
import targets as T

# %% [markdown]
# ## 1 · Read the evidence set and the framework extract
#
# The framework here is an extract of fourteen subcategories of the NIST AI Risk Management
# Framework, paraphrased for the lab. The method is the same for any control framework your
# organisation answers to.

# %%
doc = U.load("evidence.json")
controls, evidence, claims = doc["framework"]["controls"], doc["evidence"], doc["claims"]
print(doc["framework"]["name"], "\n")
U.show(controls, width=100)
print()
U.show(evidence, columns=["id", "text", "by", "strength"], width=92)

# %% [markdown]
# **Look at** · Two columns matter before any mapping. `by` says who produced the item: the
# builders, or someone independent of them. `strength` is the reviewers' judgment of what the
# item can carry: a log with rates and intervals is strong; a summary with no log is weak; a
# screenshot of one refusal is evidence of nothing.
#
# ## 2 · Map each evidence item to the controls it supports
#
# ✏️ **Exercise** · `my_map()` returns a dict from each evidence id to the list of control ids
# it supports (one or two; an empty list when it supports none).

# %%
def my_map():
    # BEGIN SOLUTION
    return {
        "E01": ["MEASURE 1.3", "MAP 1.1"], "E02": ["MEASURE 2.7"], "E03": ["MEASURE 2.7", "MANAGE 1.3"], "E04": ["MANAGE 1.3", "MEASURE 2.6"],
        "E05": ["MAP 1.1", "MAP 3.5"], "E06": ["MEASURE 2.7"], "E07": ["MEASURE 2.7"], "E08": ["GOVERN 6.1", "MANAGE 3.1"], "E09": ["MEASURE 2.10"],
        "E10": ["GOVERN 2.1"], "E11": ["MEASURE 2.7"], "E12": ["MEASURE 2.11"], "E13": ["MANAGE 4.1"], "E14": [],
    }
    # END SOLUTION

# %%
# Check, with a safety net
try:
    mapping = my_map()
except NotImplementedError:
    mapping = U.reference("d4_3_map")
ids = {c["id"] for c in controls}
key_map = {e["id"]: e["key"] for e in evidence}
U.check(set(mapping) == set(key_map) and all(set(v) <= ids for v in mapping.values()), "every item is mapped, to controls of the extract only")
agree = sum(bool(set(mapping[e]) & set(key_map[e])) or (not mapping[e] and not key_map[e]) for e in key_map)
print("items on which you and the reviewers share at least one control:", agree, "of", len(key_map))
U.check(agree >= 11, "at least eleven of fourteen items share a control with the reviewers' mapping")
U.check(mapping["E14"] == [], "a screenshot of one refusal supports no control")
U.keep("d4_3_map", mapping)

# %% [markdown]
# ## 3 · List the controls with no evidence or weak evidence
#
# ✏️ **Exercise** · `gaps(mapping, evidence)` returns a dict with `none` (the control ids no item
# maps to) and `weak` (the control ids whose items are all of strength `weak` or `none`), each in
# the order of the framework extract.

# %%
def gaps(mapping, evidence):
    # BEGIN SOLUTION
    strength = {e["id"]: e["strength"] for e in evidence}
    out = {"none": [], "weak": []}
    for c in controls:
        items = [e for e, cs in mapping.items() if c["id"] in cs]
        if not items:
            out["none"].append(c["id"])
        elif all(strength[e] != "strong" for e in items):
            out["weak"].append(c["id"])
    return out
    # END SOLUTION

# %%
try:
    holes = gaps(key_map, evidence)
except NotImplementedError:
    holes = U.reference("d4_3_gaps")
print("on the reviewers' mapping:", holes)
U.check(holes["none"] == ["MANAGE 2.4", "MANAGE 4.3"], "nothing supports switching the system off, or handling incidents")
U.check(holes["weak"] == ["MEASURE 2.11", "MANAGE 4.1"], "fairness and monitoring rest on weak evidence only")
U.keep("d4_3_gaps", holes)
counts = {c["id"]: sum(c["id"] in key_map[e["id"]] for e in evidence) for c in controls}
U.show([{"control": c, "items": n, "bar": "#" * n} for c, n in counts.items()])

# %% [markdown]
# **Look at** · Five items support MEASURE 2.7 and none supports MANAGE 2.4. Evidence piles up
# where the team likes to work: testing security. The gaps are all on the right-hand side of the
# life cycle, after release, where nobody has had to work yet.
#
# ## 4 · Link evidence to claims and write the gap list

# %%
print("top claim:", claims["top"], "\n")
U.show(claims["sub"], width=110)

# %% [markdown]
# ✏️ **Exercise** · `case()` returns a dict with `links` (from each sub-claim id to the evidence
# ids that support it), `weakest` (the sub-claim that rests on weak evidence only) and `gaps` (a
# list of dicts with `control`, `kind` (`"none"` or `"weak"`) and `ask`: what you ask for, from
# whom, to close it).

# %%
def case():
    # BEGIN SOLUTION
    return {
        "links": {"C1": ["E01", "E02", "E03", "E09", "E12"], "C2": ["E04", "E05", "E08", "E10"], "C3": ["E06", "E07"], "C4": ["E13"]},
        "weakest": "C4",
        "gaps": [
            {"control": "MANAGE 2.4", "kind": "none", "ask": "Sumayya Al-Shaalan names who may stop Katib and within how many minutes, and shows one drill"},
            {"control": "MANAGE 4.3", "kind": "none", "ask": "Sulafa Al-Nashmi extends the Agency's incident process to the agent, with a record of one exercise"},
            {"control": "MEASURE 2.11", "kind": "weak", "ask": "The red team reruns the degrading-reply probes in all three scripts, 30 trials each"},
            {"control": "MANAGE 4.1", "kind": "weak", "ask": "Younis Al-Wabel gets the monitoring plan approved with alert thresholds and a per-case-worker action log"},
        ],
    }
    # END SOLUTION

# %%
try:
    built = case()
except NotImplementedError:
    built = U.reference("d4_3_case")
strength = {e["id"]: e["strength"] for e in evidence}
claim_key = {e["id"]: e["claim"] for e in evidence}
used = [(c, e) for c, es in built["links"].items() for e in es]
U.check(set(built["links"]) == {"C1", "C2", "C3", "C4"} and all(es for es in built["links"].values()), "every sub-claim has at least one item")
U.check(all(strength[e] != "none" for _, e in used), "nothing of strength 'none' holds up a claim")
U.check(sum(claim_key[e] == c for c, e in used) >= 10, "at least ten links agree with the reviewers")
U.check(built["weakest"] == "C4", "the claim about what happens after release rests on a draft plan")
U.check({g["control"] for g in built["gaps"]} >= set(holes["none"]) | set(holes["weak"]) and all(len(g["ask"]) > 25 for g in built["gaps"]), "all four gaps are listed, each with an ask")
U.keep("d4_3_case", built)
for c in claims["sub"]:
    es = built["links"][c["id"]]
    print(f"{c['id']} · {c['text']}\n     " + ", ".join(f"{e} ({strength[e]})" for e in es))
U.save("d4_3/assurance_case.json", __import__("json").dumps({"top": claims["top"], **built}, ensure_ascii=False, indent=1))

# %% [markdown]
# **Look at** · E11, the builders' summary that "all security tests passed", is not in the
# reference links although it maps to a control. An assurance case is as strong as the evidence
# an outsider can check; a summary with no log is a claim, not evidence. And the top claim from
# Lab 1.1 now has an honest shape: three sub-claims hold, one does not yet.
#
# ## ✱ Stretch · A second framework
#
# Map the same fourteen items to the Agency's control library (`data/register.json`, controls
# C01 to C14) and compare the two gap lists. Which gaps appear in both? Which appear only when
# you look through the Agency's own controls?
#
# ## Check yourself
#
# 1. Why list the gaps yourself, in the pack?
# 2. E10, the role chart, comes from the builders and is rated strong. When is builder evidence acceptable?
# 3. The crosswalk shows a control with five items. Is it well covered?
#
# <details><summary>Answers</summary>
#
# 1. An auditor finds them anyway. A pack that names its gaps, with an ask and an owner for each, shows that the claim was tested by its authors; a pack with none shows that nobody looked.
# 2. When it is a record of fact that an outsider can verify (who holds which role) and not a judgment of the builders' own work. "Our tests passed" is the second kind.
# 3. Not necessarily: count the strong, independent items and ask whether they cover the control's whole text. Five items on security testing say nothing about resilience after release.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d4_3/assurance_case.json` is the assurance case with its gap list. Lab 4.4 starts
# from a supplied summary of the whole pack.
