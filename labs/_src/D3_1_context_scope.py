# %% [markdown]
# # Lab 3.1 · Context and scope for Katib
#
# Day 3 · Session 1 (The national framework as method) · 25 min.
#
# The National AI Risk Management Framework starts before any risk is named: with a record of
# what the system is, what it touches, who decides and how it will change. You write that record
# for Katib in four parts, one for each activity of the framework's first step, and a checklist
# tells you what a reader would still have to ask.
#
# **Tasks**
# - [ ] Describe the system, its intended uses and the uses out of scope (6 min)
# - [ ] List the data, the entry and exit points and the parties (7 min)
# - [ ] State the level of automation and the human decision points (6 min)
# - [ ] State the life-cycle stage and the change plan (6 min)
# - [ ] ✱ Stretch · Name the reference pillar that each of your out-of-scope uses rests on
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
# ## 1 · Describe the system, its intended uses and the uses out of scope
#
# Everything you need is in the brief below. Nothing in it is a secret, and nothing is yet a
# context record: it is a list of facts in the order the builders remembered them.

# %%
brief = U.load("katib_brief.json")
print(brief["name"], "·", brief["kind"])
for fact in brief["facts"]:
    print("  -", fact)

# %% [markdown]
# ✏️ **Exercise** · `system()` returns a dict with `description` (what kind of system, for what
# purpose), `output_use` (what happens to what it produces), `intended_uses` (at least three),
# `out_of_scope` (at least three uses that are not allowed), `users` (who operates it) and
# `affected` (who is affected without using it).

# %%
def system():
    # BEGIN SOLUTION
    return {
        "description": "Katib is an agent built on a hosted language model. It reads one case file and drafts the status or decision letter for it.",
        "output_use": "A signed-in case worker sees the draft; in the pilot the letter is emailed to the applicant when the case worker presses Send.",
        "intended_uses": ["Draft the letter for the case file a case worker opened", "Look up the published rules of the benefit concerned", "Send the approved letter to the applicant's registered address"],
        "out_of_scope": ["Deciding eligibility or changing a payment", "Contacting anyone other than the applicant of the case", "Searching cases for any purpose other than the open file"],
        "users": "Twelve case workers of the case-work department; two in the pilot",
        "affected": "Benefit applicants: they receive the letters and their records are read, and they never use the agent",
    }
    # END SOLUTION

# %% [markdown]
# ## 2 · List the data, the entry and exit points and the parties
#
# ✏️ **Exercise** · `data_and_parties()` returns a dict with `data` (a list of dicts with `what`
# and `level`, the classification level), `entry_points` (where content comes in), `exit_points`
# (where output goes) and `parties` (everyone in the value chain, each with a role).

# %%
def data_and_parties():
    # BEGIN SOLUTION
    return {
        "data": [{"what": "Case records: identifier, bank number, amounts, health notes on disability cases", "level": "Restricted"},
                 {"what": "The applicant's own statement", "level": "Restricted"},
                 {"what": "Published benefit rules and letter templates", "level": "Public"}],
        "entry_points": ["The case worker's request", "The case file, including the applicant statement", "The template text returned by fetch_template"],
        "exit_points": ["send_letter: email to an address", "fetch_template: a request to a host", "add_note: a note in the case record", "The draft on the case worker's screen"],
        "parties": ["Case-work department: owner and operator", "IT department: runs the agent runtime", "Lisan Language Systems: supplier of the hosted model",
                    "Applicants: affected, and authors of the statement"],
    }
    # END SOLUTION

# %% [markdown]
# ## 3 · State the level of automation and the human decision points
#
# The framework asks whether the system recommends, decides or acts, and where a person approves,
# reviews, objects or stops it.
#
# ✏️ **Exercise** · `automation()` returns a dict with `level` (`"recommends"`, `"decides"` or
# `"acts"`), `decision_points` (a list), `mandatory` (the point where a person must act) and
# `responsibilities` (a dict with `developer`, `operator`, `decision_owner`, `escalation`).

# %%
def automation():
    # BEGIN SOLUTION
    return {
        "level": "acts",
        "decision_points": ["A case worker starts every run", "The case worker reads the draft and presses Send", "The case-work supervisor may stop the pilot"],
        "mandatory": "No letter may leave without the case worker pressing Send on the draft they were shown",
        "responsibilities": {"developer": "The case-work systems team", "operator": "The case-work department under Sumayya Al-Shaalan",
                             "decision_owner": "Zuhair Al-Zaidi, deputy governor for benefits", "escalation": "Case worker to supervisor to the head of AI assurance, the same day"},
    }
    # END SOLUTION

# %% [markdown]
# **Look at** · The brief says a case worker "sees the draft" and presses Send. Lab 2.2 showed a
# second email leaving before the draft existed. Which is the truth about the level of
# automation: what the design says, or what the tools allow?
#
# ## 4 · State the life-cycle stage and the change plan
#
# ✏️ **Exercise** · `lifecycle()` returns a dict with `stage`, `changes` (a list of dicts with
# `what`, `how_often` and `approver`) and `reassess_when` (what triggers a new risk assessment).

# %%
def lifecycle():
    # BEGIN SOLUTION
    return {
        "stage": "Pilot with two case workers; full operation after sign-off",
        "changes": [{"what": "The supplier updates the hosted model", "how_often": "about twice a year", "approver": "Sumayya Al-Shaalan after a staging retest"},
                    {"what": "Letter templates change", "how_often": "monthly", "approver": "The case-work supervisor"},
                    {"what": "A tool is added or its permissions change", "how_often": "rarely", "approver": "Younis Al-Wabel, security architect"}],
        "reassess_when": "A model update, a new tool or permission, a new kind of data in the case file, or an incident",
    }
    # END SOLUTION

# %%
# Check, with a safety net: the reviewer's checklist for context and scope
try:
    ctx = {"system": system(), "data": data_and_parties(), "automation": automation(), "lifecycle": lifecycle()}
except NotImplementedError:
    ctx = U.reference("d3_1_context")
failed = U.checklist(U.review_context(ctx))
U.check(failed == 0, "the context and scope record passes the checklist")
U.check(ctx["automation"]["level"] == "acts", "Katib acts: it sends email and writes notes through tools")
U.check(any("template" in e.lower() for e in ctx["data"]["entry_points"]), "the template text is listed as an entry point")
U.keep("d3_1_context", ctx)
U.save("d3_1/context_and_scope.json", __import__("json").dumps(ctx, ensure_ascii=False, indent=1))

# %% [markdown]
# **Look at** · Two lines of this record will carry weight later. "Acts" is why Katib's risks
# score higher than Mueen's for the same weakness. And the change plan is where Lab 3.4 starts:
# the supplier updates the model about twice a year, and somebody must approve that.
#
# ## ✱ Stretch · The reference pillars
#
# The framework rests every step on four reference pillars: general principles and values,
# AI regulations, data regulations and sector regulations. For each of your three out-of-scope
# uses, name the pillar it rests on and the document you would cite.
#
# ## Check yourself
#
# 1. Why are applicants listed as affected and also as a party?
# 2. The design says "the case worker approves every letter". Why is the level of automation still "acts"?
# 3. Which line of the record would you update first after the findings of Day 2?
#
# <details><summary>Answers</summary>
#
# 1. They are affected by the letters and by what happens to their records, and they author the statement, which is an entry point. One group, two roles, and the second is the one builders forget.
# 2. Because the tools let the agent send and write without that approval: the approval is a screen, not a gate. The record describes what the system can do, and notes the gap.
# 3. The mandatory human point: today it is a statement of intent. Either the approval becomes a gate on send_letter, or the record says that it is not one.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d3_1/context_and_scope.json` opens the risk section of your pack. Lab 3.2 starts
# from a supplied list of twelve risks.
