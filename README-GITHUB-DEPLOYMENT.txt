CBSEMOCK — FRESH GITHUB REPOSITORY PACKAGE
==========================================

This package is built from the latest CBSEMOCK-main(1).zip supplied by the user.
The existing homepage content, banner, subject portals, resource pages, news,
theme switch, sharing controls, analytics placeholders, and automation files
have been retained. Four new 3D-style launch cards were added to the homepage.

FOUR ZONES
1. study-zone/       Class-group selector and subject-wise notes landing pages
2. mock-zone/        Class-group selector and subject-wise mock-paper landing pages
3. virtual-labs/     Six subject virtual-lab collections
4. quest/            Existing 3D Quest app, assets, and data folder

NAVIGATION AND ADS
- Every HTML page except the main index has a Back and Main Home navigation bar.
- Ad leaderboards are present on all pages. Existing ad configuration is in ads.js.
- All ad image URLs are resolved relative to ads.js, so nested pages can use the
  same ad configuration.
- Ad slots are placeholders by default because the existing ads.js config has
  active:false. Activate slots and add image files under ads/ when ready.

CLASS COVERAGE NOTE
The supplied repository includes Class X and Class XII subject note/mock portals.
The new 9–10 and 11–12 selectors group those supplied resources into the requested
class bands; they do not invent separate Class IX or Class XI files.

GITHUB PAGES DEPLOYMENT
1. Create a fresh GitHub repository.
2. Upload the CONTENTS of this ZIP to the repository root (not the ZIP itself).
3. Ensure index.html is at repository root.
4. Enable GitHub Pages from the main branch / root folder.
5. Open the published HTTPS URL.

LOCAL TESTING
- Do not open Quest via file:/// because its question catalogue is loaded using fetch().
- Start a local server from the repository root. With Python 3:
    py -m http.server 8000
  Then open http://localhost:8000/

IMPORTANT
- Quest application files and its question data have been included as supplied from
  the previously integrated working package. Routine future monthly updates should
  replace the quest/data folder only, preserving the app files.
