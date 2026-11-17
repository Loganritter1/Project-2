# Video Runbook

Every video opens with: "I used OpenAI Codex to help explain requirements, plan and improve the app. I reviewed the code and calculations, selected the inputs and process, and the analysis and decision are mine. This is educational only, not investment advice."

## Video 1: System and thinking changed (maximum 3 minutes)

1. State the original pilot recommendation and the point-in-time historical-return input.
2. Show the 36-month-window result and explain why the 25-point shift supports pilot rather than adoption.
3. Show one AI suggestion or claim, the independent calculation/check performed, and whether it was accepted, qualified, or rejected.
4. Close with the remaining adoption conditions: costs, policy treatment, and monitoring.

## Video 2: Code walkthrough (maximum 5 minutes)

1. Open `README.md` and run the documented command.
2. Walk through `portfolio.py`: price estimation, correlation validation, grid search, and stop behavior.
3. Walk through `app.py`: two baselines, proposed mix, verdict scorecards, controls, and chart.
4. Run `python -m unittest discover -s tests -v` and `python run_validation.py`.
5. Show `output/visible-output.md` and name the highest-risk limitation.

## Video 3: Committee presentation (maximum 5 minutes)

1. Open with the Streamlit app running live and state: "Pilot, not adopt."
2. Show the 60% SGOV / 40% ACWI base case and baseline verdicts.
3. Show the locked changed-input result: 35% SGOV / 65% ACWI after ACWI is reduced to 8%.
4. Explain the cost and reserve stresses, reversal trigger, monitoring, and the committee ask.
