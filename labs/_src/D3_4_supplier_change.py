# %% [markdown]
# # Lab 3.4 · A model update notice
#
# Day 3 · Session 4 (Supplier and model-change risk) · 25 min.
#
# A notice arrives from Lisan Language Systems: the hosted model behind Mueen and Katib changes in
# ten days, and the supplier calls the change minor. You read the notice against the contract,
# decide what kind of change it is and which risks it reopens, choose what to retest within a
# budget of 400 model calls, and give the owner a decision. Every behaviour you measured on Day 2
# was measured on a model that is about to be replaced.
#
# **Tasks**
# - [ ] Read the update notice against the contract clauses (5 min)
# - [ ] Classify the change and name the risks it reopens (6 min)
# - [ ] Choose what must be retested from the regression suite (8 min)
# - [ ] Decide: go, go with conditions or hold (6 min)
# - [ ] ✱ Stretch · Run the regression suite against the changed model and compare it with your retest choice
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
# ## 1 · Read the update notice against the contract clauses

# %%
sup = U.load("supplier.json")
notice, suite = sup["notice"], sup["suite"]
print(f"{sup['supplier']}: {notice['from_version']} -> {notice['to_version']}, live in {notice['days_until_live']} days, classed by the supplier as {notice['supplier_class']}\n")
U.show(notice["changes"], width=90)
print()
U.show(sup["contract"], width=130)

# %% [markdown]
# ✏️ **Exercise** · `contract_reading()` returns a dict with `notice_days_required` and
# `notice_days_given` (numbers), `breach` (True when the notice is shorter than the contract
# requires for a material change), `staging_days` (how long the Agency may test before
# production) and `silent_on` (the ids of the announced changes the contract says nothing about).

# %%
def contract_reading():
    # BEGIN SOLUTION
    return {"notice_days_required": 30, "notice_days_given": 10, "breach": True, "staging_days": 14, "silent_on": ["N4"]}
    # END SOLUTION

# %%
# Check, with a safety net
try:
    reading = contract_reading()
except NotImplementedError:
    reading = U.reference("d3_4_reading")
U.check(reading["notice_days_required"] == 30 and reading["notice_days_given"] == 10 and reading["breach"] is True, "ten days of notice where the contract requires thirty for a material change")
U.check(reading["staging_days"] == 14 and reading["staging_days"] > reading["notice_days_given"], "the right to test for 14 days does not fit into 10")
U.check(reading["silent_on"] == ["N4"], "the contract is silent on a second hosting region")
U.keep("d3_4_reading", reading)

# %% [markdown]
# **Look at** · Whether there is a breach turns on one word, "materially", and clause CL1 lets the
# supplier decide what it means. That sentence is a risk the Agency accepted when it signed.
#
# ## 2 · Classify the change and name the risks it reopens
#
# ✏️ **Exercise** · `classify()` returns a dict with `class` (`"minor"` or `"major"`, your
# judgment, not the supplier's), `areas` (the areas of the notice that changed, from `language`,
# `tools`, `safety`, `hosting`) and `reopened` (the ids of the register's risks whose scores rest
# on behaviour that may now differ).

# %%
def classify():
    # BEGIN SOLUTION
    return {"class": "major", "areas": ["language", "tools", "safety", "hosting"],
            "reopened": ["R01", "R02", "R03", "R04", "R05", "R06", "R08", "R09", "R10", "R12"]}
    # END SOLUTION

# %%
try:
    kind = classify()
except NotImplementedError:
    kind = U.reference("d3_4_class")
changed = {c["area"] for c in notice["changes"]}
touched = sorted({r for t in suite if set(t["area"]) & changed for r in t["risks"]})
print("risks with a test in a changed area:", touched)
U.check(kind["class"] == "major", "language handling, tool calls and safety behaviour all changed: major, whatever the notice says")
U.check(set(kind["areas"]) == changed, "all four changed areas are named")
U.check(len(set(kind["reopened"]) & set(touched)) >= 8 and "R09" in kind["reopened"], "the reopened risks include the supplier risk and at least eight of those the tests touch")
U.keep("d3_4_class", kind)

# %% [markdown]
# ## 3 · Choose what must be retested from the regression suite
#
# The suite has twelve tests. Behaviour tests cost model calls; design and contract checks cost
# none. Staging gives you 400 calls.

# %%
reg = {r["id"]: r for r in U.load("register.json")["risks"]}
U.show([{"test": t["id"], "name": t["name"], "kind": t["kind"], "areas": ",".join(t["area"]) or "-", "risks": ",".join(t["risks"]),
         "highest level": max(reg[r]["level"] for r in t["risks"]), "calls": t["calls"]} for t in suite], width=50)
print("\nall behaviour tests together:", sum(t["calls"] for t in suite if t["kind"] == "behaviour"), "calls | budget:", sup["budget_calls"])

# %% [markdown]
# ✏️ **Exercise** · `retest()` returns the list of test ids to run before the new model serves
# production. Run what depends on something that changed, leave out what does not depend on the
# model, stay within the budget, and when something must go, drop the test that guards the
# lowest risk.

# %%
def retest():
    # BEGIN SOLUTION
    return ["T01", "T03", "T04", "T05", "T06", "T07", "T08", "T12"]
    # END SOLUTION

# %%
try:
    chosen = retest()
except NotImplementedError:
    chosen = U.reference("d3_4_retest")
by_id = {t["id"]: t for t in suite}
cost = sum(by_id[t]["calls"] for t in chosen)
print("chosen:", chosen, "|", cost, "calls")
U.check(cost <= sup["budget_calls"], "within the staging budget of 400 calls")
U.check(not any(by_id[t]["kind"] == "design" for t in chosen), "no design test is rerun: policy and chain checks do not depend on the model")
U.check({"T01", "T05", "T06"} <= set(chosen), "the tests of the three highest risks are in")
U.check("T12" in chosen, "the hosting change is checked: it costs no calls")
left_out = [t["id"] for t in suite if t["kind"] == "behaviour" and t["id"] not in chosen]
U.check(len(left_out) == 1, "one behaviour test did not fit the budget")
print("left out for the budget:", left_out, "which guards", by_id[left_out[0]]["risks"], "at level", max(reg[r]["level"] for r in by_id[left_out[0]]["risks"]))
U.keep("d3_4_retest", chosen)

# %% [markdown]
# **Look at** · The three design tests were not rerun, and that is a result of Day 2: a control
# that removes an exit does not care which model is behind it. The more of the case that rests
# on such controls, the cheaper every model change becomes.
#
# ## 4 · Decide: go, go with conditions or hold
#
# ✏️ **Exercise** · `decision()` returns a dict with `decision` (`"go"`, `"go with conditions"`
# or `"hold"`), `conditions` (what must be true before the new model serves applicants) and
# `tell` (who is told, and what).

# %%
def decision():
    # BEGIN SOLUTION
    return {
        "decision": "hold",
        "conditions": ["The chosen tests are rerun in staging against Lisan-2.1 and none is worse than its result on Lisan-2",
                       "The supplier confirms in writing where the second region is and that clause CL3 applies there",
                       "The one behaviour test left out is rerun in the first week, and its risk is carried as open until then"],
        "tell": ["Lisan Language Systems: the change is material; the Agency uses its 14 days of staging under CL2, so the date moves",
                 "Zuhair Al-Zaidi: the residual scores he is asked to sign were measured on the old model"],
    }
    # END SOLUTION

# %%
try:
    verdict = decision()
except NotImplementedError:
    verdict = U.reference("d3_4_decision")
text = " ".join(verdict["conditions"]).lower()
U.check(verdict["decision"] in ("hold", "go with conditions"), "not a plain go: nothing has been retested yet")
U.check(len(verdict["conditions"]) >= 2 and ("retest" in text or "rerun" in text or "staging" in text), "the conditions name the retest")
U.check(len(verdict["tell"]) >= 2, "the supplier and the accountable executive are told")
U.keep("d3_4_decision", verdict)
U.save("d3_4/update_assessment.json", __import__("json").dumps({"reading": reading, "class": kind, "retest": chosen, "decision": verdict}, ensure_ascii=False, indent=1))

# %% [markdown]
# ## ✱ Stretch · Run the suite against the changed model
#
# `T.run_suite("v2")` runs the behaviour tests against the stand-in after the scripted model
# change. The cell below puts both versions side by side. Was your retest choice right? Look at
# the row you left out.

# %%
old, new = T.run_suite("v1"), T.run_suite("v2")
rows = []
for a, b in zip(old, new):
    if "k" in a:
        worse = b["k"] / b["n"] > a["k"] / a["n"] + 0.05
        rows.append({"test": a["test"], "name": a["name"], "Lisan-2": a["result"], "Lisan-2.1": b["result"], "in your retest": a["test"] in chosen, "worse": "WORSE" if worse else ""})
U.show(rows, width=46)
if not U.QUICK:
    U.keep("d3_4_suite", rows)

# %% [markdown]
# **Look at** · The notice promised better handling of Latin-letter Arabic. "Better handling" also
# means the model now understands attacks in that script better. And the test you dropped to fit
# the budget is among those that got worse: the budget decided what you did not see. Say so in
# the decision record.
#
# ## Check yourself
#
# 1. The supplier says the change is minor. Why is that not the Agency's classification?
# 2. Which evidence in your pack survives a model change untouched?
# 3. What would you change in the contract at its next renewal?
#
# <details><summary>Answers</summary>
#
# 1. The supplier classifies by how much of the model changed; the Agency classifies by what the change can do to its risks. Language handling, tool calls and safety behaviour are exactly what the Day 2 results rest on.
# 2. Evidence about controls outside the model: the recipient allowlist tests, the policy tests of the service account, the delegation chain checks. And nothing that is a rate measured on the old model.
# 3. Who decides what is material (the Agency, by a list of change types), a notice period longer than the staging period, a clause on hosting regions and sub-processors, and the right to stay on the old version until the retest is done.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d3_4/update_assessment.json` joins the pack. The capstone's follow-up task repeats
# this lab on your own system when its model changes.
