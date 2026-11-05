---
title: 'Minutes to Decimal: How to Convert Timesheet Hours for Payroll (With Chart)'
description: 'Payroll systems reject times written as 7:45 — they need 7.75. Learn the minutes-to-decimal formula, the 3.20-vs-3.33 mistake that causes payroll errors, a free conversion chart, and rounding rules that keep you compliant.'
pubDate: 2026-11-05
heroImage: '../../assets/blog-placeholder-4.jpg'
category: 'Productivity'
---

If you run payroll or fill out a timesheet, you have run into this problem: your time clock says **7 hours 45 minutes**, but your payroll software only accepts **7.75**. Type 7.45 and someone gets paid for the wrong amount of time.

This conversion trips up more people than you would expect, and the errors are not small — over a year of weekly timesheets, a consistent 15-minute mistake per entry is real money. Here is how the conversion actually works, the trap that causes most payroll mistakes, and the rounding rules to know.

## The formula: divide minutes by 60

Converting minutes to decimal hours is one calculation:

```
decimal hours = hours + (minutes ÷ 60)
```

Minutes are a fraction of an hour — 30 minutes is 30/60, which is 0.5. So:

| Time clock says | Calculation | Decimal |
|-----------------|-------------|---------|
| 7:30 | 7 + (30 ÷ 60) | 7.50 |
| 7:45 | 7 + (45 ÷ 60) | 7.75 |
| 8:15 | 8 + (15 ÷ 60) | 8.25 |
| 6:20 | 6 + (20 ÷ 60) | 6.33 |
| 5:05 | 5 + (5 ÷ 60) | 5.08 |

That last rule matters: minutes divide by **60**, not by 100. Most payroll mistakes start here.

## The mistake that causes wrong paychecks

The most common error looks completely harmless. Someone works **3 hours 20 minutes** and writes down **3.20**, because it feels natural — "twenty minutes, point twenty."

But 3.20 means **3 hours 12 minutes** (0.20 × 60 = 12), while the person actually worked 3 hours 20 minutes, which is **3.33**. Short by 8 minutes per entry.

The reverse mistake happens too: **4.35 does not mean 4 hours 35 minutes**. It means 4 hours and 0.35 × 60 = 21 minutes. If you meant 4:35, the correct decimal is **4.58**.

A quick sanity check: the two digits after the decimal point can never be read as minutes. If the number after the decimal is above .59, something is wrong — no timesheet entry should ever end in .75 meaning "75 minutes."

## Minutes to decimal conversion chart

For quick reference, here are the conversions you will actually use. Most payroll systems round to two decimal places.

| Minutes | Decimal | Minutes | Decimal |
|---------|---------|---------|---------|
| 1 | 0.02 | 35 | 0.58 |
| 5 | 0.08 | 40 | 0.67 |
| 10 | 0.17 | 45 | 0.75 |
| 15 | 0.25 | 50 | 0.83 |
| 20 | 0.33 | 55 | 0.92 |
| 25 | 0.42 | 60 | 1.00 |
| 30 | 0.50 | | |

Notice the pattern: 15 minutes is exactly 0.25 (a quarter hour), 30 is 0.50, 45 is 0.75. Quarters are the easy anchors — everything else you either divide or look up. A fuller [minutes-to-decimal chart](https://www.minutestodecimal.org/minutes-to-decimal-chart) covers every minute from 1 to 59 if you need the exact value for an odd entry like 37 minutes.

## Going the other way: decimal back to hours and minutes

Sometimes the conversion runs in reverse — a payroll report says you worked **38.75 hours** and you want to know what that is in actual time:

```
minutes = decimal portion × 60
```

So 38.75 = 38 hours + (0.75 × 60) = **38 hours 30 minutes**.

Two more examples:

- **6.10 hours** = 6 hours + (0.10 × 60) = 6 hours 6 minutes (not 6 hours 10)
- **22.88 hours** = 22 hours + (0.88 × 60) = 22 hours 52.8 minutes, roughly 22:53

If you do this often, a [decimal-to-hours calculator](https://www.minutestodecimal.org/decimal-to-hours-calculator) saves you the arithmetic, and the same site converts in both directions so you can double-check either way.

## Rounding rules (the legal part)

If your time clock records time to the minute, you do not have to round at all — you can pay to the exact minute. But many workplaces round to the nearest quarter hour, and the [Department of Labor](https://www.dol.gov/agencies/whd/flsa) allows that under the FLSA as long as the rounding is neutral over time:

- **1–7 minutes** past a quarter mark → round **down**
- **8–14 minutes** past → round **up**

For example, clocking in at 8:07 rounds to 8:00; clocking in at 8:08 rounds to 8:15. Rounding only in the employer's favor every single day is not neutral — that is when it turns into a wage violation. If you want the details, this guide on [time card rounding rules](https://www.minutestodecimal.org/guides/time-card-rounding) walks through the accepted practices with examples.

## A complete payroll example

Here is the whole process end to end for one employee's week, paid $22/hour with 1.5× overtime after 40 hours:

| Day | In | Out | Total |
|-----|-----|------|-------|
| Mon | 9:00 | 17:30 | 8:30 |
| Tue | 8:45 | 17:15 | 8:30 |
| Wed | 9:15 | 18:00 | 8:45 |
| Thu | 9:00 | 17:00 | 8:00 |
| Fri | 9:30 | 14:30 | 5:00 |

**Step 1 — convert each day to decimal:**

8:30 → 8.50, 8:30 → 8.50, 8:45 → 8.75, 8:00 → 8.00, 5:00 → 5.00

**Step 2 — add up:** 8.50 + 8.50 + 8.75 + 8.00 + 5.00 = **38.75 hours**

**Step 3 — split regular and overtime:** 38.75 is under 40, so it is all regular time.

**Step 4 — calculate pay:** 38.75 × $22 = **$852.50**

If the total had come to 42.50 instead, the first 40 hours pay at $22 and the remaining 2.50 hours at $33 (time and a half) — worth reading the [overtime in decimal hours](https://www.minutestodecimal.org/guides/overtime-decimal-hours) breakdown, because the most common error is applying the multiplier to the wrong base.

## Do it once, then automate it

Manual conversion works, but it does not scale. If you process timesheets every week:

1. **For a single conversion**, the [minutes-to-decimal converter](https://www.minutestodecimal.org) on the homepage handles both directions and shows the math — nothing to install, runs in the browser.
2. **For a full week of in/out times**, a [weekly timesheet calculator](https://www.minutestodecimal.org/weekly-timesheet-calculator) takes each day's clock-in and clock-out, totals the week, and outputs the decimal hours your payroll software wants.
3. **For repeated use in your own tools**, some converter sites offer embeddable widgets, so the calculator lives directly on your company's internal page.

The formula never changes: **minutes ÷ 60, added to hours**. Everything else — charts, calculators, rounding rules — is just making that one division harder to get wrong.
