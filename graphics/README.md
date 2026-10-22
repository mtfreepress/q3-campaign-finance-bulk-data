Generate the graphics data with `python3 build-graphics-data.py` from the project
root. This script uses only the Python standard library. Amounts are dollars,
formatted to two decimal places, and party codes are preserved from
`CAND_PTY_AFFILIATION` (`REP`, `DEM`, `LIB`, `IND`).

Candidate financial values come from
`output-q3-bulk-data/candidate-summaries-q3/House Senate Montana 2026.csv`.
Candidates are matched by FEC candidate ID. `TTL_RECEIPTS` is used for both
`totalCandidateRaised` and `totalReceipts`; `OTHER_POL_CMTE_CONTRIB`,
`POL_PTY_CONTRIB`, and `TTL_INDIV_CONTRIB` supply the three bar-chart categories.
These categories do not exhaust total receipts; for example, candidate loans,
candidate contributions, and transfers are separate source fields.

PAC spending comes from
`output-q3-bulk-data/montana-ies-by-candidate/Montana Super PAC IEs.csv`.
`exp_amo` is summed by candidate and `sup_opp` (`S` support, `O` oppose).
The source's total row is excluded. The individual candidate sheets are views
of this file and are not added again. A VOTERISE entry for $1,127.25 lacks a
candidate ID but names Bankhead; its `S` code assigns it to her support total,
even though it also appears in the source's Bankhead Oppose sheet. Records are
summed as supplied, without additional amendment filtering or date filtering.

Source coverage dates vary: Bankhead's candidate summary runs through
October 14, 2026; the other eight matched candidates run through September 30,
2026. The PAC workbook is labeled through October 19, 2026. These are the
provided cumulative figures, not isolated third-quarter activity.

Patrick McKraken does not appear in any supplied candidate summary (including
the national file). His row has blank party and financial fields, meaning
missing data rather than zero. No party or financial values are inferred.
Aaron Flint is used for the bubble-chart request's “Aaron Fling”; Sam Forstag
matches SAMUEL KELLEY FORSTAG, and Brian J Miller matches BRIAN JAMES MILLER.
