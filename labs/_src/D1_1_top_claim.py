# %% [markdown]
# # Lab 1.1 · A top claim and its defeaters
#
# Day 1 · Session 1 (Assurance is an argument with evidence) · 25 min.
#
# You write the claim the deputy governor will be asked to sign for Mueen, break it into three
# sub-claims, and decide which evidence would support each one and which would defeat it. This is
# the first page of the assurance pack: every test you run this week exists to support or defeat
# a line you write here.
#
# **Tasks**
# - [ ] Read the intended use and the system card of Mueen (4 min)
# - [ ] Write the top claim and three sub-claims (7 min)
# - [ ] List supporting and defeating evidence for each sub-claim (8 min)
# - [ ] Mark who may produce each item: the builder or an independent tester (6 min)
# - [ ] ✱ Stretch · Write the top claim for Katib and say which sub-claim has no counterpart in Mueen
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
# ## 1 · Read the intended use and the system card of Mueen
#
# The card is what the builders say about the system. Read it as a list of promises.

# %%
card = U.load("mueen_card.json")
print(card["name"], "·", card["kind"], "· owner:", card["owner"])
for key in ("intended_uses", "out_of_scope"):
    print("\n" + key.replace("_", " ") + ":")
    for line in card[key]:
        print("  -", line)
print("\ntools:")
for tool in card["tools"]:
    print("  -", tool["name"] + ":", tool["does"], "|", tool.get("note", ""))
print("\nguardrail:", card["guardrail"])
print("volume:", card["volume"])

# %% [markdown]
# **Look at** · Two lines of the card already tell you where to test: the note on `lookup_case`
# and the language the filter was written in.
#
# ## 2 · Write the top claim and three sub-claims
#
# A top claim names the system, the use and the condition, and evidence could show it to be false.
# "Mueen is safe" cannot be tested. "Mueen never fails" is false on the first failure.
#
# ✏️ **Exercise** · `top_claim()` returns a dict with `claim` (one sentence that names Mueen, the
# people it serves and the uses it is claimed for) and `subclaims`: three dicts with `id`
# (`S1`, `S2`, `S3`) and `text`. Cover the three harms of the card: other people's data and the
# internal rule, unfair or degrading treatment, false assurance.

# %%
def top_claim():
    # BEGIN SOLUTION
    return {
        "claim": "Mueen is acceptably safe to answer signed-in applicants on the portal about published benefit rules and their own case, in Arabic and English",
        "subclaims": [
            {"id": "S1", "text": "Mueen does not disclose another applicant's data or the internal screening rule, in any of the three scripts applicants write in"},
            {"id": "S2", "text": "Mueen answers applicants alike whatever their town or script, and gives no degrading reply"},
            {"id": "S3", "text": "Mueen does not assure an applicant of eligibility, an amount or a payment date"},
        ],
    }
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    claim = top_claim()
except NotImplementedError:
    claim = U.reference("d1_1_claim")
absolute = [w for w in ("never", "always", "completely", "100%", "perfectly") if w in claim["claim"].lower()]
U.check("Mueen" in claim["claim"] and "applicant" in claim["claim"].lower(), "the top claim names the system and the people it serves")
U.check(not absolute, "the top claim is scoped, with no absolute word such as never or always")
U.check([s["id"] for s in claim["subclaims"]] == ["S1", "S2", "S3"] and all(len(s["text"]) > 20 for s in claim["subclaims"]), "three sub-claims S1, S2, S3")
U.keep("d1_1_claim", claim)

# %% [markdown]
# ## 3 · List supporting and defeating evidence for each sub-claim
#
# The team already has ideas for evidence. Some of it can only ever agree with the claim; some
# could show it to be false. An assurance case needs the second kind.

# %%
bank = U.load("evidence_bank.json")
U.show([{"id": b["id"], "evidence": b["text"]} for b in bank], width=110)

# %% [markdown]
# ✏️ **Exercise** · `evidence_for()` returns, for `S1`, `S2` and `S3`, a dict with two lists of
# bank ids: `supports` (it adds confidence when it comes out well) and `defeats` (a bad result
# would show the sub-claim to be false). Leave out what is evidence of nothing.

# %%
def evidence_for():
    # BEGIN SOLUTION
    return {
        "S1": {"supports": ["B01", "B03", "B11"], "defeats": ["B02", "B03", "B12", "B09"]},
        "S2": {"supports": ["B05", "B06"], "defeats": ["B04", "B05", "B09"]},
        "S3": {"supports": ["B07", "B11"], "defeats": ["B08", "B07", "B09"]},
    }
    # END SOLUTION

# %%
try:
    links = evidence_for()
except NotImplementedError:
    links = U.reference("d1_1_links")
by_id = {b["id"]: b for b in bank}
used = {i for s in links.values() for side in s.values() for i in side}
for sid, sides in links.items():
    U.check(len(sides["defeats"]) >= 1 and all(by_id[i]["can_defeat"] and sid in by_id[i]["about"] for i in sides["defeats"]),
            f"{sid}: every defeater could really show this sub-claim to be false")
    U.check(all(sid in by_id[i]["about"] for i in sides["supports"]), f"{sid}: every supporting item is about this sub-claim")
U.check("B10" not in used, "the demonstration to the deputy governor is evidence of nothing")
U.keep("d1_1_links", links)

# %% [markdown]
# **Look at** · B06, the supplier's sentence, can support S2 and can never defeat it: nobody
# writes "our model is disrespectful" on a model card. B10 fails for the same reason and for a
# second one: three requests chosen by the builder.
#
# ## 4 · Mark who may produce each item: the builder or an independent tester
#
# Evidence that could defeat a claim is worth little when it is produced by the people whose
# work the claim is about.
#
# ✏️ **Exercise** · `producers()` returns a dict from every bank id you used to who must produce
# it: `"builder"`, `"independent"`, `"operations"` or `"supplier"`.

# %%
def producers():
    # BEGIN SOLUTION
    return {"B01": "builder", "B02": "independent", "B03": "independent", "B04": "independent", "B05": "independent", "B06": "supplier",
            "B07": "builder", "B08": "independent", "B09": "operations", "B11": "builder", "B12": "operations"}
    # END SOLUTION

# %%
try:
    who = producers()
except NotImplementedError:
    who = U.reference("d1_1_who")
U.check(used <= set(who), "every item you used has a producer")
adversarial = [i for i in used if by_id[i]["producer"] == "independent"]
U.check(all(who[i] == "independent" for i in adversarial), "adversarial tests and reviews are produced by people who did not build the system")
for sid, sides in links.items():
    U.check(any(who[i] in ("independent", "operations") for i in sides["defeats"]), f"{sid} has a defeater that the builder does not control")
U.keep("d1_1_who", who)

print("\nTOP CLAIM ·", claim["claim"])
for s in claim["subclaims"]:
    print(f"\n  {s['id']} · {s['text']}")
    for side in ("supports", "defeats"):
        for i in links[s["id"]][side]:
            print(f"      {side:<9}{i} [{who[i]}] {by_id[i]['text'][:80]}")
U.save("d1_1/top_claim.json", __import__("json").dumps({"claim": claim, "links": links, "producers": who}, ensure_ascii=False, indent=1))

# %% [markdown]
# ## ✱ Stretch · The top claim for Katib
#
# Katib acts: it sends letters and writes notes. Write its top claim and three sub-claims. Which
# of them has no counterpart in Mueen, and what kind of evidence does it need that a probe log
# cannot give?
#
# ## Check yourself
#
# 1. Why is "all 40 unit tests pass" (B01) support and not a defeater of S1?
# 2. The golden-set accuracy (B07) is produced by the builder. What makes it acceptable anyway?
# 3. Which single item would you ask for first if you had one day?
#
# <details><summary>Answers</summary>
#
# 1. The tests check what the builder thought of. They pass while the tool still takes any identifier: a pass says nothing about the paths nobody wrote a test for.
# 2. It is reproducible: the set, the answers and the scoring are fixed, so an independent reviewer can rerun it and inspect the set. Independence can be bought by review when production cannot be handed over.
# 3. B02 or B03 for S1: the card itself says the lookup tool takes any identifier, and disclosure of personal data is the harm with a legal duty attached.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d1_1/top_claim.json` is page one of your assurance pack. Lab 4.3 builds the full case
# from a supplied evidence set and does not need this file.
