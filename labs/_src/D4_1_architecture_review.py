# %% [markdown]
# # Lab 4.1 · Three findings on the agent's design
#
# Day 4 · Session 1 (Security architecture review) · 25 min.
#
# Katib's pilot design is on your desk for review. You read it the way an attacker would: what
# may the agent's own account do, where does the runtime sit, and which ways out does it have.
# Ten tests turn those questions into results, and you write three findings and a decision for
# each proposed fix. Nothing here calls a model: a design review holds whatever the model does.
#
# **Tasks**
# - [ ] Read the design and its data classification (5 min)
# - [ ] Run the least-privilege, isolation and egress tests (7 min)
# - [ ] Write three findings with severity (8 min)
# - [ ] Record a decision for each proposed fix (5 min)
# - [ ] ✱ Stretch · Write the policy rule that closes one finding and run the tests again
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
# ## 1 · Read the design and its data classification

# %%
import copy

doc = U.load("design.json")
design, review_key = doc["design"], doc["key"]
print(design["system"], "·", design["version"], "\n")
print("data and its classification:")
for what, level in design["classification"].items():
    print(f"  {what}: {level}")
print("\ntiers:", design["tiers"])
print("placement:", design["placement"])
print("\nroutes:")
U.show(design["routes"])
print("\npolicy of the service accounts:")
U.show(design["policy"])
print("\nmonitoring:", design["monitoring"])

# %% [markdown]
# ✏️ **Exercise** · Least privilege starts from the data. `needs()` returns the permissions
# Katib needs for its intended uses, as a list of dicts with `action` and `resource`, written as
# narrowly as the intended uses allow. Use the patterns of the policy above; for a case, the
# narrow resource is `case:own-caseload`, for mail `addr:registered`, for the web
# `host:templates.nrba.example`.

# %%
def needs():
    # BEGIN SOLUTION
    return [
        {"action": "case:read", "resource": "case:own-caseload"},
        {"action": "case:note", "resource": "case:own-caseload"},
        {"action": "mail:send", "resource": "addr:registered"},
        {"action": "net:fetch", "resource": "host:templates.nrba.example"},
        {"action": "rules:read", "resource": "rules:*"},
    ]
    # END SOLUTION

# %%
# Check, with a safety net
try:
    wanted = needs()
except NotImplementedError:
    wanted = U.reference("d4_1_needs")
granted = [(r["action"], r["resource"]) for r in design["policy"] if r["principal"] == "svc-katib"]
U.check(not any(w["action"] == "case:search" for w in wanted), "no intended use needs a search across cases")
U.check(not any(w["resource"] in ("case:*", "addr:*", "host:*") for w in wanted), "nothing Restricted and no way out is granted with a wildcard")
U.check({"case:read", "mail:send", "net:fetch", "rules:read"} <= {w["action"] for w in wanted}, "the intended uses are still possible")
print("granted today:", len(granted), "rules, of which with a wildcard on Restricted data or a way out:",
      sum(res in ("case:*", "addr:*", "host:*") for _, res in granted))
U.keep("d4_1_needs", wanted)

# %% [markdown]
# **Look at** · The gap between what you wrote and what is granted is the review. Every wildcard
# was convenient for the builders on the day they wrote it.
#
# ## 2 · Run the least-privilege, isolation and egress tests
#
# `T.review_tests(design)` asks ten questions of the design. Each has an expected answer:
# `deny` for what must not be possible, `allow` for what must still work.

# %%
results = T.review_tests(design)
U.show(results, columns=["test", "criterion", "question", "expected", "got", "passes"], width=70)

# %% [markdown]
# ✏️ **Exercise** · `failing(results)` returns a dict from each criterion to the list of its
# failed test ids, for the criteria that have at least one failure.

# %%
def failing(results):
    # BEGIN SOLUTION
    out = {}
    for r in results:
        if not r["passes"]:
            out.setdefault(r["criterion"], []).append(r["test"])
    return out
    # END SOLUTION

# %%
try:
    failed = failing(results)
except NotImplementedError:
    failed = U.reference("d4_1_failed")
print(failed)
U.check(failed == {c: v["tests"] for c, v in review_key.items()}, "seven tests fail, under four criteria")
U.check(all(r["passes"] for r in results if r["expected"] == "allow"), "the two things that must work still work")
U.keep("d4_1_failed", failed)

# %% [markdown]
# **Look at** · IS-2 passes: Mueen cannot use Katib's tools. A review also records what holds,
# so that the next change does not break it unnoticed.
#
# ## 3 · Write three findings with severity
#
# ✏️ **Exercise** · `findings()` returns three findings, one each for `least_privilege`,
# `isolation` and `egress`. Each is a dict with `criterion`, `title` (what is wrong, in one
# sentence), `evidence` (the failed test ids), `consequence` (what an attacker gains, tied to a
# risk of the register) and `severity` (1 to 4, on the impact scale of Day 3).

# %%
def findings():
    # BEGIN SOLUTION
    return [
        {"criterion": "least_privilege", "title": "The agent's account may read and search every case, not the caseload of the acting case worker",
         "evidence": ["LP-1", "LP-2"], "consequence": "One hijacked run reaches the cases of a whole town (R02)", "severity": 3},
        {"criterion": "egress", "title": "The agent may email any address and request any host",
         "evidence": ["EG-1", "EG-2"], "consequence": "A record can leave by email or inside a web address (R01)", "severity": 3},
        {"criterion": "isolation", "title": "The runtime sits in the case-database tier and has a route to the internet",
         "evidence": ["IS-1"], "consequence": "Whatever the policy says, Restricted data and the internet meet in one process", "severity": 3},
    ]
    # END SOLUTION

# %%
try:
    found = findings()
except NotImplementedError:
    found = U.reference("d4_1_findings")
U.check(sorted(f["criterion"] for f in found) == ["egress", "isolation", "least_privilege"], "one finding for each of the three criteria")
for f in found:
    U.check(set(f["evidence"]) and set(f["evidence"]) <= set(failed.get(f["criterion"], [])), f"{f['criterion']}: the evidence is failed tests of that criterion")
    U.check(abs(f["severity"] - review_key[f["criterion"]]["severity"]) <= 1, f"{f['criterion']}: severity within one step of the reviewers'")
    U.check(len(f["title"]) > 25 and len(f["consequence"]) > 25, f"{f['criterion']}: the finding says what is wrong and what it lets an attacker do")
U.keep("d4_1_findings", found)

# %% [markdown]
# **Look at** · Monitoring failed two tests and is not among your three findings. It goes to the
# pack as an open item: nobody can stop the agent, and no action can be traced to a case worker.
# You will meet it again in Labs 4.3 and 4.4.
#
# ## 4 · Record a decision for each proposed fix
#
# The builders answered the draft review with a fix for each finding:

# %%
proposed = {
    "least_privilege": "Keep case:* for the service account and add a line to the agent's instructions: only open the case you were given",
    "egress": "Replace addr:* with addr:registered and host:* with the template host",
    "isolation": "Move the runtime to tier B and reach the case database through a case service; remove the default gateway",
}
for c, text in proposed.items():
    print(f"{c}: {text}")

# %% [markdown]
# ✏️ **Exercise** · `decisions()` returns a dict from each criterion to a dict with `decision`
# (`"accept"`, `"reject"` or `"accept with conditions"`), `reason`, `owner` and `retest` (the
# test ids that must pass before the finding is closed).

# %%
def decisions():
    # BEGIN SOLUTION
    return {
        "least_privilege": {"decision": "reject", "reason": "An instruction is not a control: Day 2 showed the agent follows planted text. The permission itself must be scoped to the caseload",
                            "owner": "Younis Al-Wabel", "retest": ["LP-1", "LP-2"]},
        "egress": {"decision": "accept", "reason": "The rule removes both ways out and the template host still works",
                   "owner": "Younis Al-Wabel", "retest": ["EG-1", "EG-2", "EG-3"]},
        "isolation": {"decision": "accept with conditions", "reason": "Right design; until the case service exists the pilot stays at two case workers",
                      "owner": "Younis Al-Wabel", "retest": ["IS-1", "IS-2"]},
    }
    # END SOLUTION

# %%
try:
    decided = decisions()
except NotImplementedError:
    decided = U.reference("d4_1_decisions")
for c, d in decided.items():
    U.check(d["decision"] in ("accept", "reject", "accept with conditions") and len(d["reason"]) > 25 and d["owner"], f"{c}: a decision with a reason and an owner")
    U.check(set(review_key[c]["tests"]) <= set(d["retest"]), f"{c}: the failed tests are named as the retest")
U.check(decided["least_privilege"]["decision"] == "reject", "an instruction to the model is not accepted as a fix for a permission")
U.keep("d4_1_decisions", decided)
U.save("d4_1/architecture_review.json", __import__("json").dumps({"failed": failed, "findings": found, "decisions": decided}, ensure_ascii=False, indent=1))

# %% [markdown]
# **Look at** · A decision record is short: what was proposed, what was decided, why, who, and
# which test closes it. In a year nobody will remember the meeting, and the record is what an
# auditor reads.
#
# ## ✱ Stretch · Close one finding
#
# Change the policy of a copy of the design so that the egress finding closes, and run the tests
# again. The cell below makes the copy; write the two rules.

# %%
fixed = copy.deepcopy(design)
# fixed["policy"] = [r for r in fixed["policy"] if r["action"] not in ("mail:send", "net:fetch")] + [ ...your two rules... ]
again = T.review_tests(fixed)
print("failed tests on the copy:", [r["test"] for r in again if not r["passes"]])

# %% [markdown]
# ## Check yourself
#
# 1. Why is "tell the agent to open only the case it was given" rejected as a fix?
# 2. The policy is fixed and IS-1 still fails. Why does that matter?
# 3. Which of the ten tests must be rerun after the supplier's model update?
#
# <details><summary>Answers</summary>
#
# 1. Because the weakness is what the account may do, and the proposed fix changes only what the model is asked to do. A planted instruction asks it for something else.
# 2. Policy and placement are two layers. A policy rule can be changed by mistake in one line; a runtime with no route out cannot send anything whatever the policy says.
# 3. None. They test the design, not the model's behaviour. That is why the pack should rest on them where it can.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d4_1/architecture_review.json` joins the pack. Lab 4.2 starts from supplied
# delegation chains.
