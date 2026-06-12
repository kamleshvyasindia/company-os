# Skill: skillify

**Trigger:** a human says "skillify it," or session-review notices the same work done twice. **Goal:** know-how leaves heads and enters the system.

1. From the session transcript, extract: trigger, steps actually taken, tools touched, what good output looked like, what was corrected.
2. Write `skills/<name>.md` in the house format (Trigger / Goal / numbered steps / Gate). Steps describe OUTCOMES per step, not keystrokes.
3. Add the row to `RESOLVER.md`.
4. Run the hygiene check: does this overlap an existing skill? If yes, merge into one parameterized skill instead. Does the resolver table still cover all recurring work with no overlaps (MECE)? Note exceptions.
5. Tell the human: skill name, when it will fire, and the one thing to correct next time it runs.
