CBSEMOCK MATHEMATICS VIRTUAL LABS — V1.1 QA UPDATE

Contents
- 20 standalone interactive mathematics laboratory HTML pages
- index.html collection landing page
- Linear Function Explorer (Lab 01) retained unchanged as the approved gold standard

V1.1 mathematical corrections and alignment
- Lab 15: the selectable die-face count now drives both the dice simulation and the theoretical probability of an even result. For a fair die numbered 1..F, P(even) = floor(F/2)/F.
- Lab 17: Matrix Operations Studio now provides two editable 2x2 matrices and a scalar. Live outputs include A+B, kA and det(A).
- Lab 18: the transformation sequence is explicit and calculated in order: reflect across the x-axis, rotate anticlockwise about the origin, then translate by (k,k). The live explanation distinguishes length-preserving reflection/rotation from translation.
- Lab 20: the area interval is normalised to lower and upper endpoints, so reversing the endpoint controls does not produce a negative geometric area. The visual rectangles use the same interval.

Validation performed
- All 20 HTML pages are present.
- All inline JavaScript blocks passed Node.js syntax checks.
- Calculation-level checks were run for the mathematical result functions, including representative values for all labs and targeted checks for Labs 15, 17, 18 and 20.
- The approved Lab 01 file was retained byte-for-byte.

Browser testing limitation
A Chromium end-to-end run could not be completed in this environment: browser navigation was blocked by the execution environment (ERR_BLOCKED_BY_ADMINISTRATOR), and the attempted embedded-page run terminated. Therefore this package is not represented as fully browser-tested. Please test the pages in the target deployment/browser before publishing to students.

These are educational simulations and should be reviewed by the mathematics department before formal assessment use.
