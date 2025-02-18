# AutoDoc Tool

Build an MCP tool that automatically creates documentation by:

1. Watching for triggers:
   - Task completion ("done", "completed", etc.)
   - Break indicators ("let's take a break", "pause here", etc.)
   - Manual command ("/document")

2. When triggered:
   - Look at recent conversation
   - Check project files (code, docs, README)
   - See what changed since last doc

3. Create a simple markdown doc:
   ```md
   ---
   date: [timestamp]
   status: needs_review
   ---

   # Progress Update

   ## What's Done
   [list completed tasks]

   ## Current State
   [describe where we are]

   ## Next Steps
   [list what's next]
   ```

4. Ask for review:
   - Show the doc
   - "Does this look good? (yes/no)"
   - If no, ask what to change
   - Mark as "reviewed" or "not_reviewed"

5. Save in:
   ```
   docs/
   └── progress/
       ├── YYYY-MM-DD_HH-MM.md  (new updates)
       └── current.md           (latest state)
   ```

That's it! Keep it simple but useful. Let users refine docs if needed, but focus on capturing progress automatically so nothing gets lost.
