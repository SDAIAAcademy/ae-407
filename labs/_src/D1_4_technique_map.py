# %% [markdown]
# # Lab 1.4 · Ten attacks, mapped and pruned
#
# Day 1 · Session 4 (Choosing techniques from catalogues) · 25 min.
#
# The team brainstormed ten attacks. You map each one to an entry of the OWASP lists and to a MITRE
# ATLAS technique, tie it to an objective of the plan, drop the two that serve none, and read the
# coverage table to see which objective is thin. Catalogues give you names other teams recognise
# and ideas you did not have; the objectives decide what is worth a call.
#
# **Tasks**
# - [ ] Read the ten planned attacks and the catalogue extract (4 min)
# - [ ] Map each attack to an OWASP entry and an ATLAS technique (9 min)
# - [ ] Tie each attack to an objective and drop the two that serve none (7 min)
# - [ ] Read the coverage table: which objective has too few attacks (5 min)
# - [ ] ✱ Stretch · Write one new attack for an agentic entry that no planned attack covers
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
# ## 1 · Read the ten planned attacks and the catalogue extract

# %%
data = U.load("planned_attacks.json")
attacks, key = data["attacks"], data["key"]
cat = U.load("catalogue.json")
objectives = U.load("objectives.json")
U.show(attacks, width=115)
print()
for part in ("owasp_llm", "owasp_agentic", "atlas"):
    print(part + ":", "; ".join(f"{e['id']} {e['name']}" for e in cat[part]), "\n")
U.show([{"id": o["id"], "target": o["target"], "harm": o["harm"]} for o in objectives], width=110)

# %% [markdown]
# ## 2 · Map each attack to an OWASP entry and an ATLAS technique
#
# ✏️ **Exercise** · `mapping()` returns a dict from each attack id to a dict with `owasp` (an id
# such as `LLM01` or `ASI02`, or `"none"` when no entry of either list fits) and `atlas` (an id
# such as `AML.T0054`). Choose the entry that names what the attack does, not what it hopes to get.

# %%
def mapping():
    # BEGIN SOLUTION
    return {
        "A01": {"owasp": "LLM01", "atlas": "AML.T0051.000"}, "A02": {"owasp": "LLM02", "atlas": "AML.T0054"},
        "A03": {"owasp": "LLM01", "atlas": "AML.T0068"}, "A04": {"owasp": "none", "atlas": "AML.T0048.003"},
        "A05": {"owasp": "LLM07", "atlas": "AML.T0048.003"}, "A06": {"owasp": "ASI01", "atlas": "AML.T0051.001"},
        "A07": {"owasp": "ASI02", "atlas": "AML.T0086"}, "A08": {"owasp": "ASI01", "atlas": "AML.T0053"},
        "A09": {"owasp": "LLM06", "atlas": "AML.T0034"}, "A10": {"owasp": "LLM08", "atlas": "AML.T0069"},
    }
    # END SOLUTION

# %%
# Check, with a safety net. More than one entry can be defended; the key lists those the reviewers accepted.
try:
    my_map = mapping()
except NotImplementedError:
    my_map = U.reference("d1_4_map")
known = {e["id"] for part in ("owasp_llm", "owasp_agentic", "atlas") for e in cat[part]} | {"none"}
U.check(all(m["owasp"] in known and m["atlas"] in known for m in my_map.values()), "every id you used is in the catalogue extract")
agree = {a: (my_map[a]["owasp"] in key[a]["owasp"], my_map[a]["atlas"] in key[a]["atlas"]) for a in key}
U.show([{"attack": a, "owasp": my_map[a]["owasp"], "accepted": "yes" if o else "discuss", "atlas": my_map[a]["atlas"], "accepted ": "yes" if t else "discuss"} for a, (o, t) in agree.items()])
U.check(sum(o and t for o, t in agree.values()) >= 8, "at least eight of ten mappings are among those the reviewers accepted")
U.keep("d1_4_map", my_map)

# %% [markdown]
# **Look at** · A04, the degrading reply, has no entry in either OWASP list: they are security
# lists. If you had built the plan from the catalogues, the objective the Agency cares about most
# in public would have no test at all. ATLAS at least names the harm to the user.
#
# ## 3 · Tie each attack to an objective and drop the two that serve none
#
# ✏️ **Exercise** · `serves()` returns a dict from each attack id to the objective it serves
# (`"O1"` to `"O4"`) or `None`. An attack serves an objective when its success would be the harm
# that objective names.

# %%
def serves():
    # BEGIN SOLUTION
    return {"A01": "O1", "A02": "O1", "A03": "O1", "A04": "O2", "A05": "O3", "A06": "O4", "A07": "O4", "A08": "O4", "A09": None, "A10": None}
    # END SOLUTION

# %%
try:
    link = serves()
except NotImplementedError:
    link = U.reference("d1_4_serves")
dropped = sorted(a for a, o in link.items() if o is None)
print("dropped:", dropped)
U.check(dropped == ["A09", "A10"], "the two attacks that serve no objective are dropped")
U.check(all(link[a] == key[a]["objective"] for a in key), "every kept attack is tied to the objective whose harm it would cause")
U.keep("d1_4_serves", link)

# %% [markdown]
# **Look at** · A09 is a real technique with an OWASP entry, and the plan put it out of scope: in
# a sandbox it only spends the budget. A10 is a step an attacker takes, not a harm. Neither is
# forbidden knowledge; neither earns calls. If you believe one of them is a harm, the fix is a
# fifth objective with a harm and a success check, not a stray attack.
#
# ## 4 · Read the coverage table: which objective has too few attacks
#
# ✏️ **Exercise** · `coverage(link, my_map)` returns one row per objective with `objective`,
# `attacks` (how many kept attacks serve it) and `entries` (the sorted list of distinct OWASP
# entries among them, without `"none"`).

# %%
def coverage(link, my_map):
    # BEGIN SOLUTION
    rows = []
    for o in ("O1", "O2", "O3", "O4"):
        mine = [a for a, target in link.items() if target == o]
        rows.append({"objective": o, "attacks": len(mine), "entries": sorted({my_map[a]["owasp"] for a in mine} - {"none"})})
    return rows
    # END SOLUTION

# %%
try:
    table = coverage(link, my_map)
except NotImplementedError:
    table = U.reference("d1_4_coverage")
U.show(table)
U.check([r["attacks"] for r in table] == [3, 1, 1, 3], "O1 and O4 have three attacks each, O2 and O3 one each")
thin = [r["objective"] for r in table if r["attacks"] < 2]
print("thin objectives:", thin)
untested = sorted({e["id"] for e in cat["owasp_agentic"]} - {m["owasp"] for m in my_map.values()})
print("agentic entries with no planned attack:", untested)
U.keep("d1_4_coverage", table)
U.save("d1_4/attack_plan.json", __import__("json").dumps({"map": my_map, "serves": link, "coverage": table}, indent=1))

# %% [markdown]
# **Look at** · Read coverage both ways. By objective: O2 and O3 rest on one attack each, in one
# wording. By catalogue: most agentic entries have no attack. Some of those are rightly empty
# (Katib runs no generated code and talks to no other agent); for each of the others, write down
# why not, or add an attack.
#
# ## ✱ Stretch · One new attack for an uncovered agentic entry
#
# Pick an entry from the list printed above that does apply to Katib (identity and privilege, or
# trust between the case worker and the agent). Write the attack in one sentence, name its
# objective and say how you would decide success.
#
# ## Check yourself
#
# 1. A06 can be mapped to LLM01 or to ASI01. What does each name tell the reader?
# 2. Why is "it is in the OWASP list" not a reason to keep A09?
# 3. O2 has one attack. What would a second and third look like?
#
# <details><summary>Answers</summary>
#
# 1. LLM01 names the mechanism (text read as instruction); ASI01 names what was taken over (the agent's goal). A finding report usually gives both: one tells the builder what to fix, the other tells the owner what was at stake.
# 2. A catalogue lists what can be done to systems in general. The plan lists the harms this Agency decided to look for with this budget. An attack is kept when its success is one of those harms.
# 3. The same question asked in transliterated Arabic and in dialect; a comparison of answers to the same question from two towns; a role-play that invites contempt for applicants in debt.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d1_4/attack_plan.json` completes the plan. Day 2 starts from the supplied probe set
# in `data/probes.jsonl`, which covers the same four objectives.
