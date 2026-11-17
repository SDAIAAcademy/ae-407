# %% [markdown]
# # Lab 1.3 · A test plan a reviewer approves
#
# Day 1 · Session 3 (Objectives, scope and rules of engagement) · 25 min.
#
# You write the test plan of the exercise as data: objectives tied to harms, scope, a budget, rules
# of engagement, stop conditions and what happens to a harmful output. Then the planning checklist
# that Sulafa Al-Nashmi, head of AI assurance, applies to every plan runs against yours. The plan
# is approved when all ten items pass.
#
# **Tasks**
# - [ ] Write four objectives, each tied to a harm and a success check (7 min)
# - [ ] Set the scope, what is out of scope and the call budget (5 min)
# - [ ] Write the stop conditions and the harmful-output procedure (7 min)
# - [ ] Run the planning checklist and fix what it rejects (6 min)
# - [ ] ✱ Stretch · Add the rules for an attacker model: what it may generate, where its outputs are kept and who reads them
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
# ## 1 · Write four objectives, each tied to a harm and a success check
#
# An objective is not "try prompt injection". It names who is harmed and how, and it says what
# you will look at to decide that the harm happened. The two targets are `mueen` and `katib`.
# The ranked paths of Lab 1.2 are supplied below.

# %%
ranked = U.reference("d1_2_ranked")
U.show(ranked[:4])
print("\nMueen is not to do:", *U.load("mueen_card.json")["out_of_scope"], sep="\n  - ")

# %% [markdown]
# ✏️ **Exercise** · `objectives()` returns four dicts with `id` (`O1` to `O4`), `target`, `harm`,
# `success_check` and `decided_by` (what you read to decide: the reply text, the tool log, the
# exit log, the case record). One objective must be about unfair or degrading treatment of
# applicants: at this Agency that is a red-team objective beside data leakage.

# %%
def objectives():
    # BEGIN SOLUTION
    return U.load("objectives.json")
    # END SOLUTION

# %%
# Check, with a safety net
try:
    objs = objectives()
except NotImplementedError:
    objs = U.reference("d1_3_plan")["objectives"]
U.show([{"id": o["id"], "target": o["target"], "harm": o["harm"]} for o in objs], width=100)

# %% [markdown]
# ## 2 · Set the scope, what is out of scope and the call budget
#
# ✏️ **Exercise** · `scope()` returns a dict with `targets`, `scripts` (from `en`, `ar`,
# `arabizi`), `out_of_scope` (a list of sentences) and `budget_calls`. The exercise has a fixed
# budget of 600 model calls for both targets.

# %%
def scope():
    # BEGIN SOLUTION
    return {
        "targets": ["mueen", "katib"],
        "scripts": ["en", "ar", "arabizi"],
        "out_of_scope": ["The production portal and the production case database", "Real applicants, real staff accounts and real addresses",
                         "Denial of service and anything that only spends the budget", "The supplier's own infrastructure"],
        "budget_calls": 600,
    }
    # END SOLUTION

# %% [markdown]
# ## 3 · Write the stop conditions and the harmful-output procedure
#
# A stop condition is an event after which testing halts and someone is told. A red team that
# tries to draw degrading text will sometimes succeed: decide now where that text is kept, who
# may read it and when it is deleted.
#
# ✏️ **Exercise** · `rules()` returns a dict with `stop_conditions` (a list of sentences),
# `harmful_outputs` (a dict with `stored`, `access`, `deleted`), `roles` (`lead`, `tester`,
# `builder`) and `data_handling` (one sentence that names the classification level of case data
# and where it may go).

# %%
def rules():
    # BEGIN SOLUTION
    return {
        "stop_conditions": [
            "Anything that looks like real personal data appears in a reply or a file: stop, tell the lead and the data protection officer",
            "A request or an email leaves the sandbox for a real host: stop and tell the security architect",
            "The call budget is spent, or a target stops answering",
            "A tester is distressed by an output: stop that line of probing and tell the lead",
        ],
        "harmful_outputs": {"stored": "In the attack log inside the exercise repository, marked as harmful, never pasted into chat or slides",
                            "access": "The testers, the lead and the internal auditor", "deleted": "Ninety days after the findings report is signed, except the excerpts the report quotes"},
        "roles": {"lead": "Sulafa Al-Nashmi", "tester": "the assurance team", "builder": "the case-work systems team"},
        "data_handling": "Case data is synthetic but handled as Restricted: it stays in the sandbox and in the exercise repository",
    }
    # END SOLUTION

# %% [markdown]
# ## 4 · Run the planning checklist and fix what it rejects

# %%
try:
    plan = {"objectives": objs, "scope": scope(), **rules()}
    plan["budget_calls"] = plan["scope"]["budget_calls"]
except NotImplementedError:
    plan = U.reference("d1_3_plan")
failed = U.checklist(U.review_plan(plan))
U.check(failed == 0, "the plan passes the planning checklist: approved")
U.keep("d1_3_plan", plan)
U.save("d1_3/test_plan.json", __import__("json").dumps(plan, ensure_ascii=False, indent=1))

# %% [markdown]
# **Look at** · Now break it on purpose, to see what the reviewer is protecting. Each of these is
# a plan real teams have submitted.

# %%
import copy

weak = copy.deepcopy(plan)
weak["objectives"][0]["decided_by"] = "the model says it complied"
weak["scope"]["scripts"] = ["en"]
weak["stop_conditions"] = weak["stop_conditions"][2:]
weak["roles"]["tester"] = weak["roles"]["builder"]
rejected = [text for text, ok in U.review_plan(weak) if not ok]
print(*rejected, sep="\n")
U.check(len(rejected) == 4, "the weakened plan is rejected on four items")

# %% [markdown]
# ## ✱ Stretch · Rules for an attacker model
#
# In the capstone you may use a model to write attacks. Add a section `attacker_model` to the
# plan: what it may generate, where its outputs are kept, who reads them before they are sent to
# a target, and what you do when it produces something you would not have written yourself.
#
# ## Check yourself
#
# 1. Why does the checklist refuse "the model says it complied" as a way to decide success?
# 2. The budget is 600 calls. Name two decisions it forces before the first probe.
# 3. Who should be able to stop the exercise, and how do they learn that a stop condition was met?
#
# <details><summary>Answers</summary>
#
# 1. A hijacked or confused model does not report accurately what it did. Success is read from what happened: the reply text, the tool log, the exit log, the case record.
# 2. How many trials each attack gets (which sets how wide the intervals are), and which paths are not tested at all. Both belong in the plan, not in the report's excuses.
# 3. Any tester and the lead. The plan names who is told for each condition; a stop that depends on one person noticing is not a stop condition.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d1_3/test_plan.json` is the plan section of your pack. Lab 1.4 loads the reference
# objectives from `data/objectives.json`.
