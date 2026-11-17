# %% [markdown]
# # Lab 4.4 · A one-page residual-risk statement
#
# Day 4 · Session 4 (Briefing the accountable executive) · 25 min.
#
# Zuhair Al-Zaidi, the deputy governor, is asked to release Katib from the pilot to all twelve
# case workers. He has ten minutes and will read one page. You write that page from the summary
# of the assurance pack: the risks that remain in words he can act on, a recommendation, and
# conditions with owners and dates. A checklist plays the part of his chief of staff.
#
# **Tasks**
# - [ ] Read the summary of the assurance pack (5 min)
# - [ ] State the residual risks in plain words with their levels (6 min)
# - [ ] Write the recommendation with conditions, owners and dates (8 min)
# - [ ] Check the page against the briefing checklist (6 min)
# - [ ] ✱ Stretch · Revise the page after the supplier model change of Lab 3.4 and mark what changed
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
# ## 1 · Read the summary of the assurance pack

# %%
pack = U.load("pack.json")
print("systems:", pack["systems"])
print("decision requested:", pack["requested_decision"])
print("accountable executive:", pack["accountable_executive"], "\n")
U.show([{"risk": r["risk"], "inherent": r["inherent"], "residual": r["residual"], "band": U.band(r["residual"]), "depends on": " ".join(r["depends_on"]) or "-",
         "status": r["status"], "title": r["title"]} for r in pack["residual"]], width=62)
for name in ("open_findings", "gaps", "not_tested"):
    print(f"\n{name.replace('_', ' ')}:")
    for line in pack[name]:
        print("  -", line)
print("\npeople who can own a condition:", pack["people"])

# %% [markdown]
# ✏️ **Exercise** · Some residual scores are true today and some are promises. `on_paper(pack)`
# returns the ids of the risks whose residual score depends on at least one control that is not
# live yet. Read the `status` column; there is no field to filter on, which is how packs arrive.

# %%
def on_paper(pack):
    # BEGIN SOLUTION
    return ["R01", "R02"]
    # END SOLUTION

# %%
# Check, with a safety net
try:
    promised = on_paper(pack)
except NotImplementedError:
    promised = U.reference("d4_4_promised")
U.check(sorted(promised) == ["R01", "R02"], "R01 and R02 are medium only once controls that are due or not built are live")
U.keep("d4_4_promised", promised)

# %% [markdown]
# **Look at** · Until C03 is built, R02 stands at 12, not at 4. A page that prints "4, medium"
# with no condition beside it tells the deputy governor something that is not yet true.
#
# ## 2 · State the residual risks in plain words with their levels
#
# Plain words: what could happen, to whom, how likely, and what it depends on. No term that
# needs this course to understand. The checklist refuses a list of them.
#
# ✏️ **Exercise** · `risks_in_plain_words()` returns a list of dicts with `risk` (the id),
# `plain_words` and `level` (the residual level in the pack). Include the three highest residual
# risks, and the risks whose score is a promise.

# %%
def risks_in_plain_words():
    # BEGIN SOLUTION
    return [
        {"risk": "R09", "level": 6, "plain_words": "The supplier replaces the model in ten days. Our results were measured on the old one"},
        {"risk": "R07", "level": 6, "plain_words": "Case workers send drafts unread, so a wrong letter can reach an applicant. Untreated"},
        {"risk": "R05", "level": 6, "plain_words": "People who write Arabic in Latin letters are less well protected. Untreated"},
        {"risk": "R02", "level": 4, "plain_words": "One misled run could read a whole town's cases. Medium only once access is limited to the worker's own cases; today high"},
        {"risk": "R01", "level": 4, "plain_words": "Hidden text in a statement could make Katib send a record outside. Email is closed; two safeguards are due"},
    ]
    # END SOLUTION

# %% [markdown]
# ## 3 · Write the recommendation with conditions, owners and dates
#
# Three answers are possible: **go**, **go with conditions**, **hold**. A condition is something
# that must be true, owned by a named person at the Agency, due in a number of days.
#
# ✏️ **Exercise** · `recommendation()` returns a dict with `decision_requested`,
# `recommendation`, `conditions` (a list of dicts with `condition`, `owner`, `due_days`) and
# `not_tested` (at least two lines).

# %%
def recommendation():
    # BEGIN SOLUTION
    return {
        "decision_requested": "Release Katib from two case workers to all twelve",
        "recommendation": "go with conditions",
        "conditions": [
            {"condition": "Before release: Katib can open only the cases of the worker it acts for, proven by test", "owner": "Younis Al-Wabel", "due_days": 30},
            {"condition": "Before release: a named person can stop Katib within minutes, and each action is logged per case worker", "owner": "Sumayya Al-Shaalan", "due_days": 21},
            {"condition": "Before the new model serves applicants: our tests are rerun on it and none is worse", "owner": "Sulafa Al-Nashmi", "due_days": 14},
            {"condition": "The supplier confirms in writing where data is processed", "owner": "Tuqa Al-Mishaal", "due_days": 10},
        ],
        "not_tested": ["Attachments other than text", "Gulf dialect beyond a few attempts", "The new model version"],
    }
    # END SOLUTION

# %% [markdown]
# ## 4 · Check the page against the briefing checklist
#
# The page is the two parts together, with the signatory and the date of the next review.

# %%
try:
    page = {"to": pack["accountable_executive"], "residual_risks": risks_in_plain_words(), **recommendation(),
            "signatory": pack["accountable_executive"], "review_days": 90}
except NotImplementedError:
    page = U.reference("d4_4_page")
print("words on the page:", U.words(page), "\n")
failed = U.checklist(U.review_statement(page, pack))
U.check(failed == 0, "the page passes the briefing checklist")
U.check(all(any(r["risk"] == p for r in page["residual_risks"]) for p in promised), "the risks whose score is a promise are on the page")
U.check(page["recommendation"] != "go", "not a plain go: controls are not built and the model is about to change")
U.keep("d4_4_page", page)

# %%
# The page as the deputy governor sees it
lines = [f"To: {page['to']}", f"Decision requested: {page['decision_requested']}", f"Recommendation: {page['recommendation'].upper()}", "", "What remains:"]
lines += [f"  {r['risk']} · level {r['level']} ({U.band(r['level'])}) · {r['plain_words']}" for r in page["residual_risks"]]
lines += ["", "Conditions:"] + [f"  {i}. {c['condition']} ({c['owner']}, {c['due_days']} days)" for i, c in enumerate(page["conditions"], 1)]
lines += ["", "Not tested: " + "; ".join(page["not_tested"]), "", f"Signed: {page['signatory']} · reviewed again within {page['review_days']} days"]
print("\n".join(lines))
U.save("d4_4/residual_risk_statement.md", "\n".join(lines))

# %% [markdown]
# **Look at** · Read your page as someone who was in none of the labs. Is there one sentence he
# could not repeat to the governor? The checklist counts words and catches jargon; it cannot tell
# whether the page is true. That is what the panel on the capstone day is for: every line must
# lead back to a file in the pack.
#
# ## ✱ Stretch · After the model change
#
# The stretch of Lab 3.4 showed four tests worse on Lisan-2.1, one of them not in the retest.
# Revise the page: which levels change, which condition is added, does the recommendation still
# stand? Mark every line you changed, so that the reader of the second version sees the
# difference at once.
#
# ## Check yourself
#
# 1. Why does the page say what was not tested?
# 2. The owner of a condition is "the security team". What is wrong?
# 3. The deputy governor asks: "Is it safe?" What do you answer?
#
# <details><summary>Answers</summary>
#
# 1. Because the signature covers the whole system and the evidence does not. The executive must know where the tested ground ends, or he signs for more than anyone checked.
# 2. Nobody can be asked on the due date. A condition has one named person; the checklist accepts only people of the Agency.
# 3. Not with yes or no. "For the stated uses, these are the risks that remain and their levels; on these conditions I recommend release; this is what we did not test." Then the page.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d4_4/residual_risk_statement.md` is the last page of the pack and the first one
# read. On the capstone day you write the same page for Insaf and defend it.
