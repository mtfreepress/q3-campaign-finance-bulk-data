#!/usr/bin/env python3
"""Build the two graphics CSVs from the converted campaign finance data."""

import csv
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'output-q3-bulk-data'
GRAPHICS = ROOT / 'graphics'
# Explicit IDs avoid differences in spelling and initials between source files.
CANDIDATES = [
    ('Kurt Alme', 'S6MT00295'),
    ('Alani Bankhead', 'S6MT00253'),
    ('Kyle Austin', 'S6MT00261'),
    ('Seth Bodnar', 'S6MT00287'),
    ('Aaron Flint', 'H6MT01152'),
    ('Sam Forstag', 'H6MT01137'),
    ('Troy Downing', 'H4MT02098'),
    ('Brian J Miller', 'H6MT02150'),
    ('Patrick McKraken', None),  # No filing in the supplied candidate summaries.
    ('Michael D Eisenhauer', 'H6MT02168'),
]
BUBBLE_IDS = {'S6MT00295', 'S6MT00253', 'S6MT00287', 'H6MT01152', 'H6MT01137'}


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as handle:
        # The source has a literal backslash-t appended to one field name.
        return [{key.strip().removesuffix(r'\t'): value for key, value in row.items()}
                for row in csv.DictReader(handle)]


def money(value):
    """Use decimal arithmetic and export dollar amounts to the nearest cent."""
    return format(Decimal(value).quantize(Decimal('0.01')), '.2f')


def write_csv(name, fields, rows):
    with (GRAPHICS / name).open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote graphics/{name}: {len(rows)} candidates')


def main():
    summaries = read_csv(DATA / 'candidate-summaries-q3' / 'House Senate Montana 2026.csv')
    candidates = {}
    for row in summaries:
        candidate_id = row['CAND_ID']
        if candidate_id in candidates:
            raise ValueError(f'Duplicate candidate summary: {candidate_id}')
        candidates[candidate_id] = row

    totals = {candidate_id: {'S': Decimal(0), 'O': Decimal(0)}
              for candidate_id in BUBBLE_IDS}
    expenditures = read_csv(DATA / 'montana-ies-by-candidate' / 'Montana Super PAC IEs.csv')
    for row in expenditures:
        # Total rows have no candidate or support/oppose code.
        if not row['cand_id'] and not row['cand_name']:
            continue
        candidate_id = row['cand_id']
        if not candidate_id and row['cand_name'].strip().casefold() == 'bankhead, alani':
            candidate_id = 'S6MT00253'
        if candidate_id not in totals:
            continue
        direction = row['sup_opp'].strip()
        if direction not in ('S', 'O'):
            raise ValueError(f'Unknown support/oppose code: {row}')
        totals[candidate_id][direction] += Decimal(row['exp_amo'])

    bubble_rows = []
    bar_rows = []
    for name, candidate_id in CANDIDATES:
        if candidate_id is None:
            bar_rows.append({'candidate': name})
            print(f'WARNING: {name} has no supplied filing; party and amounts left blank.')
            continue
        filing = candidates[candidate_id]
        common = {'candidate': name, 'party': filing['CAND_PTY_AFFILIATION']}
        bar_rows.append({
            **common,
            'pacMoney': money(filing['OTHER_POL_CMTE_CONTRIB']),
            'partyCommitteeMoney': money(filing['POL_PTY_CONTRIB']),
            'individualDonors': money(filing['TTL_INDIV_CONTRIB']),
            'totalReceipts': money(filing['TTL_RECEIPTS']),
        })
        if candidate_id in BUBBLE_IDS:
            bubble_rows.append({
                **common,
                'pacSupport': money(totals[candidate_id]['S']),
                'pacOppose': money(totals[candidate_id]['O']),
                'totalCandidateRaised': money(filing['TTL_RECEIPTS']),
            })

    GRAPHICS.mkdir(parents=True, exist_ok=True)
    write_csv('bubble-chart.csv',
              ['candidate', 'party', 'pacSupport', 'pacOppose', 'totalCandidateRaised'],
              bubble_rows)
    write_csv('bar-chart.csv',
              ['candidate', 'party', 'pacMoney', 'partyCommitteeMoney',
               'individualDonors', 'totalReceipts'], bar_rows)


if __name__ == '__main__':
    main()
