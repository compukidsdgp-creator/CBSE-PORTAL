# CBSEMOCK Quest – JSON-driven local test build

This build loads published quest content from JSON rather than embedding question banks in `assets/quest.js`.

## Main files
- `index.html` – app interface.
- `assets/quest.css` – design and responsive styling.
- `assets/quest.js` – app logic, catalogue loader, validation, progress and certificates.
- `data/catalogue-entry.json` – central catalogue of monthly releases.
- `data/questions/` – group manifests and class-specific question banks.
- `RUN-LOCAL.bat` – starts the local test server on Windows.

## Current included release
The November 2026 test release contains:
- Artificial Intelligence (417): Class 9 and Class 10, 15 questions each.
- Computer Science (083): Class 11 and Class 12, 15 questions each.

The application creates class-specific quest cards from the combined group manifests. The student sees the relevant class bank after selecting their class.

## Local testing
See `README-LOCAL-TEST.md`. Start the app with `RUN-LOCAL.bat`; do not open `index.html` directly because JSON loading requires HTTP.

## Monthly publishing
Generate a release package with Quest Publisher, copy its question and manifest JSON files into `data/questions/`, then append the release's `quests` entries to `data/catalogue-entry.json`. Keep previous entries and files to preserve the archive. Update the catalogue's top-level `month` field to the newest release month. Detailed instructions are in `README-LOCAL-TEST.md`.

## Student data and current limitations
- Student names, attempts, XP and certificates are stored in that browser's local storage.
- Progress does not sync across devices. Use the built-in JSON backup export/import.
- The leaderboard remains a local demonstration, not a shared live leaderboard.
- Certificate IDs are locally generated and are not centrally verifiable. Add a secure backend before issuing certificates as official credentials or relying on tamper-resistant scores.
- Review all question content and approve it before public student release.

## GitHub Pages
Upload the complete folder, including `data/`. GitHub Pages serves the JSON files over HTTPS; Python is only needed for local testing.
