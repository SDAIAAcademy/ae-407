# %% [markdown]
# # Lab 1.2 · Missing paths in the threat model
#
# Day 1 · Session 2 (Scoping from the threat model) · 25 min.
#
# The builders of Katib wrote a threat model with six paths. You read it as a tester: tag what
# holds private data, what carries untrusted content and what is an exit, list every path where
# the three meet, find the ones the model misses and rank all of them for testing. You wrote
# threat models in AE-308; here one is handed to you and your job is to turn it into a scope.
#
# **Tasks**
# - [ ] Read the provided threat model and the tool list of Katib (5 min)
# - [ ] Tag every tool and store: private data, untrusted content, exit (6 min)
# - [ ] Find the paths where the three meet and add the missing ones (8 min)
# - [ ] Rank the paths for testing (6 min)
# - [ ] ✱ Stretch · Find a path that needs two case files and say why a single-file test would miss it
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
# ## 1 · Read the provided threat model and the tool list of Katib

# %%
tm = U.load("threat_model.json")
U.show([{"id": e["id"], "kind": e["kind"], "what": e["what"]} for e in tm["elements"]], width=90)
print()
U.show([{"id": p["id"], "path": p["text"]} for p in tm["provided_paths"]], width=110)

# %% [markdown]
# **Look at** · Six paths look thorough. Count how many of them have all three of: content an
# outsider can write, data that is private, and a way out of the Agency.
#
# ## 2 · Tag every tool and store: private data, untrusted content, exit
#
# ✏️ **Exercise** · `tags()` returns a dict from each element id to `"private"`, `"untrusted"`,
# `"exit"` or `"none"`. Untrusted means: someone outside the Agency can write it. An exit means:
# it can carry data to a place the Agency does not control.

# %%
def tags():
    # BEGIN SOLUTION
    return {"case_record": "private", "all_cases": "private", "statement": "untrusted", "template": "untrusted", "rules": "none",
            "worker_chat": "none", "send_letter": "exit", "fetch_template": "exit", "add_note": "none", "draft_letter": "none"}
    # END SOLUTION

# %%
# Check, with a safety net
try:
    my_tags = tags()
except NotImplementedError:
    my_tags = U.reference("d1_2_tags")
key = tm["key"]
wrong = [e for e in key["tags"] if my_tags.get(e) != key["tags"][e]]
print("differs from the reference:", wrong or "nothing")
U.check(len(wrong) <= 1, "at most one tag differs from the reference")
U.check(my_tags.get("template") == "untrusted", "the template text is untrusted: it comes back from an address given in the call")
my_tags = dict(key["tags"]) if wrong else my_tags
U.keep("d1_2_tags", my_tags)

# %% [markdown]
# **Look at** · `fetch_template` is an exit when it sends the request and a carrier of untrusted
# content when the reply comes back. `worker_chat` is typed by authenticated staff: what goes
# wrong there is misuse, which has its own controls, not injection.
#
# ## 3 · Find the paths where the three meet and add the missing ones
#
# ✏️ **Exercise** · `trifecta_paths(my_tags)` returns every combination of one untrusted element,
# one private element and one exit as a dict with the keys `untrusted`, `private`, `exit`.

# %%
def trifecta_paths(my_tags):
    # BEGIN SOLUTION
    pick = lambda tag: sorted(e for e, t in my_tags.items() if t == tag)
    return [{"untrusted": u, "private": p, "exit": x} for u in pick("untrusted") for p in pick("private") for x in pick("exit")]
    # END SOLUTION

# %%
try:
    paths = trifecta_paths(my_tags)
except NotImplementedError:
    paths = U.reference("d1_2_paths")
triple = lambda p: (p["untrusted"], p["private"], p["exit"])
covered = {triple(p) for p in tm["provided_paths"] if all(triple(p))}
missing = [p for p in paths if triple(p) not in covered]
U.check(len(paths) == 8, "two untrusted sources, two private stores and two exits give eight paths")
U.check(len(missing) == 6, "the provided threat model covers two of the eight; six are missing")
U.keep("d1_2_paths", paths)
U.show(missing)

# %% [markdown]
# **Look at** · The provided model has both exits and stops at one case file. Nobody wrote down
# that the template is an entry point, or that `search_cases` puts every town behind the same hijack.
#
# ## 4 · Rank the paths for testing
#
# A budget of 600 model calls does not test eight paths equally. Rank by the harm if the path
# works and by how little the attacker needs. The team agreed on two scales: harm 2 for one case
# record and 4 for every case of a town; ease 3 for the statement (any applicant writes it) and 1
# for the template (the attacker must first control an address the agent fetches).
#
# ✏️ **Exercise** · `rank(paths, harm, ease)` returns the paths sorted by `harm × ease`, highest
# first, each with a `score` key. Break ties by putting `send_letter` before `fetch_template`.

# %%
def rank(paths, harm, ease):
    # BEGIN SOLUTION
    scored = [dict(p, score=harm[p["private"]] * ease[p["untrusted"]]) for p in paths]
    return sorted(scored, key=lambda p: (-p["score"], p["exit"] != "send_letter", p["untrusted"]))
    # END SOLUTION

# %%
try:
    ranked = rank(paths, key["harm"], key["ease"])
except NotImplementedError:
    ranked = U.reference("d1_2_ranked")
U.show(ranked)
U.check([p["score"] for p in ranked] == sorted((p["score"] for p in ranked), reverse=True), "sorted by score, highest first")
U.check(triple(ranked[0]) == ("statement", "all_cases", "send_letter") and ranked[0]["score"] == 12, "first to test: a statement that sends every case of a town by email")
U.check(sum(triple(p) in covered for p in ranked[:2]) == 0, "neither of the two highest-ranked paths is in the provided threat model")
U.keep("d1_2_ranked", ranked)
U.save("d1_2/ranked_paths.json", __import__("json").dumps(ranked, indent=1))

# %% [markdown]
# **Look at** · The two paths at the top of your list are both missing from the builders' model.
# That is the usual result of scoping from someone else's threat model, and the reason the scope
# is yours to write.
#
# ## ✱ Stretch · A path that needs two case files
#
# `add_note` is tagged "none". Suppose a planted line in case A makes Katib write a note into
# case B, and the note itself carries an instruction. Which tag changes, and why would a test that
# plants and runs one file never find this?
#
# ## Check yourself
#
# 1. Why is P4 (a case worker searches outside their caseload) not one of the eight paths?
# 2. What single change removes four of the eight paths at once?
# 3. The ease scale gave the template 1. What evidence would make you raise it?
#
# <details><summary>Answers</summary>
#
# 1. It has no untrusted content: the request comes from authenticated staff. It is a real risk (misuse) and belongs in the register, but an injection test does not exercise it.
# 2. Removing one leg. For example scoping `search_cases` to the acting case worker's caseload removes the four paths through `all_cases`; an allowlist on each exit removes the paths through that exit.
# 3. Any way for an outsider to choose the address: an instruction in the statement that names it (path P6 does exactly that), or a template host that accepts uploads.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d1_2/ranked_paths.json` is the scope section of your test plan. Lab 1.3 supplies its
# own copy.
