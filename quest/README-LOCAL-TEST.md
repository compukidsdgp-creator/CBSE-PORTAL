# CBSEMOCK Quest – JSON-driven local test build

## Start the app
1. Extract the complete ZIP folder.
2. Keep `index.html`, `assets`, and `data` together exactly as supplied.
3. Double-click `RUN-LOCAL.bat`. It starts a local web server and opens http://localhost:8000.
4. Keep the command window open while testing. Press Ctrl+C to stop the server.

**Important:** Do not double-click `index.html` directly. The app fetches JSON files from `data/`, and browsers block those requests from a `file://` page. Python 3 is required for local testing; GitHub Pages does not need Python.

## Add a new monthly release manually
1. Generate the release ZIP with Quest Publisher and extract it to a temporary folder.
2. Copy all new class question-bank JSON files and group manifest JSON files into the application's `data/questions/` folder.
3. Open the release's `catalogue-entry.json`. Copy its `quests` entries into the existing application's `data/catalogue-entry.json` `quests` array. Append; do not replace old entries, so the archive remains available.
4. Confirm every catalogue `manifest` path exists under `data/`. Each manifest's `class_sets[].file` path is also relative to `data/` (normally `questions/<filename>.json`).
5. Update the catalogue top-level `month` field to the newest release month (for example, `December 2026`). Keep the `quests` array containing all previous and new entries.
6. Save and refresh the app. The new month appears automatically.

## Important rules
- Each catalogue quest needs a unique `id` and `manifest` path.
- Keep one catalogue entry per combined subject/group/month release. One AI Group 9–10 entry points to separate Class 9 and Class 10 banks.
- Use unique file names each month; never overwrite older question files.
- The app validates catalogue IDs, paths, class numbers, question IDs, options and answer keys.
- Draft status is allowed in this local testing build. Review content and approve it before student publication.

## GitHub Pages
Upload the complete folder, including `data/`. GitHub Pages serves JSON over HTTPS and loads the catalogue and banks directly. No Python server is needed online.

## Student progress
Progress remains in that browser's local storage. It does not sync across devices. Use the built-in backup export/import. The leaderboard remains a local demonstration, not a shared live leaderboard.
