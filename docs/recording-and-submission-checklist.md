# Recording and Submission Checklist

## Before recording

- [ ] Run `python -m streamlit run "lab13 files/app.py"` and keep the app open.
- [ ] Open `docs/zoom-video-scripts.md`, `output/visible-output.md`, and `docs/decision-memo.md`.
- [ ] Turn on Zoom webcam and microphone; share only the required window/tab.
- [ ] Close notifications, private browser tabs, passwords, and personal files.
- [ ] Practice the disclosure and recommendation: **Pilot, not adopt.**

## Recordings

- [ ] Video 1: research evolution and one AI-output check; maximum 3:00.
- [ ] Video 2: code/data walkthrough, test run, validation evidence, and limitation; maximum 5:00.
- [ ] Video 3: open with the live app, present the committee recommendation, risks, triggers, and ask; maximum 5:00.
- [ ] Use the same reported values in every video:
  - Base case: 60% SGOV / 40% ACWI; 6.61% return; 5.99% volatility.
  - Changed-input case: 35% SGOV / 65% ACWI; 6.52% return; 9.65% volatility.
  - Recommendation: non-funded pilot, not adoption.

## YouTube and transcripts

- [ ] Upload each recording as **Unlisted**, not Private.
- [ ] Enable captions.
- [ ] Correct captions for ticker names, percentages, the recommendation, and material finance terms.
- [ ] Save the corrected text as `docs/transcript-video-1.txt`, `docs/transcript-video-2.txt`, and `docs/transcript-video-3.txt`.
- [ ] Verify each video opens in a logged-out/private browser window.

## Final repository check

- [ ] Add the final video URLs, durations, and timestamp indices to `docs/submission-manifest.csv`.
- [ ] Commit and push the three transcript files and completed manifest.
- [ ] Confirm the GitHub repository includes `README.md`, `requirements.txt`, `tests/`, `output/`, `docs/decision-memo.md`, and `docs/validation-and-ai-use.md`.
- [ ] Re-run `python -m unittest discover -s tests -v`.
- [ ] Re-run `python run_validation.py` and confirm `output/visible-output.md` still matches the memo.

## Brightspace submission

- [ ] Submit the GitHub repository URL.
- [ ] Submit all three Unlisted YouTube links.
- [ ] Attach `docs/decision-memo.md` and `docs/validation-and-ai-use.md`.
- [ ] Attach the completed manifest and all three corrected transcript files, if required by the submission form.
- [ ] Do not submit `lab20.md`.
