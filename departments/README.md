# departments/ — each function as a set of workflow loops

A department OS is not a folder of documents; it's a set of **installed workflow loops**, one canvas per workflow. A workflow without a canvas is a one-off, not part of the OS.

Every loop has the same five-part anatomy:

**sensor** (what triggers it) → **policy** (the rules) → **tools** (what it may call) → **quality gate** (what blocks shipping) → **learning** (what gets written back to the brain)

Rules:
- Copy `_canvas-template.md` to create a new workflow. Fill every field — especially the gate and the DRI.
- Each department folder holds its canvases plus an `outputs/` subfolder for the finished artifacts its loops produce.
- Install order: **pain × frequency × data access.** Don't install a loop you can't feed with real data.
- Start with ONE loop in the company's focus department. Add the next when the first runs boringly well.

`marketing/user-signal-to-content.md` is a fully worked example — read it before writing your first canvas.
