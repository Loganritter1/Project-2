# Cold-Run Record

| Field | Record |
|---|---|
| Repository tested | `https://github.com/Loganritter1/Project-2` |
| Commit tested | `20e82e0` |
| Environment | Windows PowerShell with Python and Streamlit 1.66.0 |
| Fresh-clone command | `git clone https://github.com/Loganritter1/Project-2.git project2-submission-check` |
| Verification commands | `python -m pip check`; `python -m unittest discover -s tests -v`; `python run_validation.py` |
| Result | `pip check` reported no broken requirements; all seven tests passed; the validation runner regenerated the committed output. |
| Visible output | `output/visible-output.md` and `output/validation-results.json` |
| First failure | None in this fresh-clone verification. |
| Prior cross-platform repair | A macOS partner found that the Windows-style README path failed. Commit `c32d7e5` changed it to the cross-platform `lab13 files/app.py` path; the partner then reported a successful app launch. |

The interactive Streamlit app remains the final manual launch check: `python -m streamlit run "lab13 files/app.py"`.
