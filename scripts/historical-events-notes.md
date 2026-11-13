# Historical Events — Research Notes

Compiled: 2026-11-09
Data file: `data/historical-events.json` (95 entries)

## 1. What this file is

A set of verified historical dates for Outrank (Nepal government-exam
preparation portal), covering the dates Lok Sewa GK actually asks: Nepal's
unification and political history, the seven constitutions, Nepal's institutions,
Nepal's international milestones, and world-history dates in the GK syllabus.

## 2. Method

1. Every date was checked against at least **two reputable sources** using web
   search (`browser_search`) and, where needed, page text (`browser_open`).
   Reputable sources used: Wikipedia history/constitution/institution articles,
   the Nepal News diplomatic timeline, Nepali Times, Rising Nepal Daily,
   official treaty texts (FAO / Government of India), the Nepal Rastra Bank
   official PDF, the Tribhuvan University official site, the Colombo Plan
   official member list, Britannica and Encyclopedia.com.
2. A date was recorded as an exact `date_ad` only when **two or more sources
   agreed on that exact day**. Where sources agreed on the event and year but
   the exact day was less firmly documented, the entry is marked `confidence:
   "medium"`.
3. Where sources **disagreed on a date**, the exact date was NOT used. The
   entry was either kept year-only (with the dispute noted in its summary) or
   dropped entirely. See §5 for the full list.
4. No date was invented, estimated or converted from AD to BS by guessing.

## 3. Bikram Sambat (BS) date policy

- `day_bs` ("MM-DD") is set **only when a source explicitly gave the BS
  month and day** (e.g. Falgun 7, 2007 BS for 18 Feb 1951; Ashoj 3, 2072 BS
  for 20 Sep 2015; Baisakh 14, 2013 BS for 26 Apr 1956).
- `year_bs` is set when the source gave the BS year, or when the AD month is
  known so the BS year is deterministic (the BS new year falls around
  mid-April: January–mid-April = AD − 57, mid-April–December = AD − 56).
  For year-only AD events with an unknown month, `year_bs` is null.
- For world-history events and non-Nepal international organisations,
  `year_bs` is null — the BS year is not exam-relevant there and `date_ad`
  is the anchor.
- BS month numbers: Baisakh 01, Jestha 02, Asar 03, Shrawan 04, Bhadra 05,
  Ashwin 06, Kartik 07, Mangsir 08, Poush 09, Magh 10, Falgun 11, Chaitra 12.
- Wars and long events are anchored on their **start date** as `date_ad`,
  with the end date stated in the summary (First World War, Second World War,
  Maoist insurgency).

## 4. Confidence

- `high` — two or more reputable sources agree on the exact date.
- `medium` — sources agree on the event and year, but the exact day rests on
  a single detailed source, or the supporting sources are weaker (study
  material, GK notes). These entries are still safe to use, but the day
  should not be quoted as a settled fact without the caveat.

Counts: 54 high, 41 medium (of 95 entries).

## 5. Dates EXCLUDED because sources disagreed

These dates are **not** used as exact `date_ad` values anywhere in the JSON.
Where an entry is kept year-only, the dispute is also noted in its summary.

| # | Event | Conflicting dates | Treatment |
|---|-------|-------------------|-----------|
| 1 | Kathmandu conquered by Prithvi Narayan Shah | 25 Sep 1768 (Medieval History of Nepal / UC Press Levy / Thamel) vs 26 Sep 1768, 13 Ashwin 1825 BS (Battle of Kathmandu) vs 29 Sep 1768 (Country Studies / Makalu Adventure) | Exact day excluded; Kathmandu Valley unification kept as a year-only 1769 entry |
| 2 | Bhaktapur captured | 25 Nov 1769 vs night of 10 Nov 1769 (Levy / Stiller via Bhasha Vamsavali) | Exact day excluded; covered by the year-only 1769 valley-unification entry |
| 3 | Gorkhapatra first issue | 6 May 1901 (Rising Nepal Daily) vs 7 May 1901 (Kathmandu Metro anniversary dating); a Malla essay gives Monday, Jestha 3, 1958 BS, which does not align cleanly with either | Kept year-only (1901) |
| 4 | Radio Nepal established | 1 Apr 1951 (Academia.edu PSB paper, Freedom Forum, Globethics) vs 2 Apr 1951 (Rising Nepal Daily, Piromomo) | Kept year-only (1951) |
| 5 | Durbar High School founded | 1853 (Spotlight Nepal / Bajracharya et al.; R.M. Nepal, NepJOL 2025) vs 1854 (Samriddhi, Amar Shrestha blog, Poudel paper) vs 1883 and 1884 (other sources) vs 1910 (one academic paper, internally inconsistent — Jung Bahadur died 1877) | **Excluded entirely** — too many conflicting years, no trustworthy anchor |
| 6 | Nepal joined WTO | 23 Apr 2004 (Bikram Khatri notes) vs 24 Apr 2004 (CNI Nepal) | Kept year-only (2004) |
| 7 | Nepal joined BIMSTEC | Feb 2004 (Prepp / AssignmentPoint) vs membership granted 2003 (CNI Nepal) | Nepal-joining entry excluded; BIMSTEC founding (6 June 1997) kept |
| 8 | First Civil Service Act promulgated | 7 Sep 1956 (Rising Nepal Daily, CESLAM; Civil Service Day observed 7 Sep / Bhadra 22) vs 6 Sep 1956 (Khabarhub, Ratopati) | Kept year-only (1956) |
| 9 | Interim Constitution third amendment (republic) | 27 Dec 2007 vs 28 Dec 2007 (sources differ on the day the Interim Constitution was amended to declare Nepal a federal democratic republic) | Entry not created |
| 10 | Interim Government of Nepal Act 1951 — promulgation date | 30 Mar 1951 promulgated (SouthAsiaMonitor) vs 11 Apr 1951 promulgated/in force (Wikipedia, MyRepublica) | Kept 11 Apr 1951 (two sources agree); the 30 Mar date is most likely the promulgation-vs-effective-date distinction, recorded here rather than treated as a flat exclusion |
| 11 | 1951 revolution — start of Jana Andolan II | 4 Apr 2006 vs 6 Apr 2006 (start of the April 2006 protests) | Only the 24 Apr 2006 parliament-restoration entry is used; no start-date entry |
| 12 | 2015 Constitution adoption vote count | 538 of 598 in favour (Wikipedia) vs 507 in favour (Loksewa Pathsala) | Vote count not included in any summary (already logged in SOURCES.md §10.8) |
| 13 | Nepal Rastra Bank first banknotes | 19 Sep 1959 vs 19 Feb 1960 | Not included (already logged in SOURCES.md §10.9) |
| 14 | Sugauli Treaty BS year | 1872 BS (most sources) vs 1873 BS (one NepJOL article) | 1872 BS used; the 1873 figure is treated as that source's error |
| 15 | Tribhuvan University BS day | 11 Asar 2016 BS / 25 June 1959 (Wikipedia, TU site, Gurubaa) vs Asar 30 (stray Facebook comments) | 25 June 1959 kept as high confidence; the Facebook claim is not a reputable source and was disregarded |
| 16 | Bir Hospital founded | 1890 (common GK, NepJOL science table) vs 1865 (one low-quality PDF) | **Excluded** — no second reputable source confirms either year |
| 17 | Rastriya Banijya Bank founded 23 Jan 1966 | Only one source found (a bbsnotes internship PDF) | **Excluded** — needs a second reputable source |
| 18 | Earthquake magnitudes | 1934 quake: 8.0–8.4; 1988 quake: 6.8–6.9; 2015 quake casualty counts vary | Exact magnitudes omitted or given as "about"; 1934 given as "about 8.0", 2015 as Mw 7.8 with "about 9,000" dead |
| 19 | National referendum 1980 vote share | 57.4% vs 54.79% in favour of Panchayat | Vote share omitted from the summary |
| 20 | Pakistan Independence Day | Power transferred at midnight 14/15 Aug 1947; Pakistan celebrates 14 Aug (from 1948), India 15 Aug | Not treated as a disagreement — the nuance is stated in the summary |
| 21 | Buddha's birth year | 563 BCE (Nepali GK convention) vs c. 480 BCE (scholarly range) | Not researched in this session; no entry created |
| 22 | First general election under the 1990 Constitution (May 1991), first census (1911), first five-year plan (1956), Nepal Academy, NHRC, first president elected (21 July 2008), NAM first summit day (1 Sep 1961) | Dates not verified against two sources in this session | Not included; candidates for a future verification pass |

## 6. Sources relied on most

- Wikipedia history/constitution/institution articles — the single most-used
  source family (cross-checked against a second source for every entry).
- Nepal News diplomatic timeline (`english.nepalnews.com/s/long-reads/nepals-diplomatic-journey-a-chronological-timeline/`) — Nepal's
  international milestones (UN, treaties, SAARC, peacekeeping).
- Nepali Times / Rising Nepal Daily / The Himalayan Times / Online Khabar —
  Nepal political and institutional dates.
- Official treaty texts via FAO and the Government of India (Mahakali Treaty),
  the Nepal Rastra Bank official history PDF, the Tribhuvan University
  official site, and the Colombo Plan official member list.
- GK reference notes (Bikram Khatri notes, Testbook, Encyclopedia.com,
  Britannica) — used as the second source for organisation dates, never
  as the sole source.

## 7. Coverage

95 entries: nepal-history 35, constitution 13, nepal-institutions 17,
international 16, world-history 14.

Category balance is close to the target (roughly 40% Nepal history,
20% constitution, 15% institutions, 15% international, 10% world history)
except that constitution is at ~14% and world history at ~15% — quality
over exact split; no weak constitution or world-history entries were added
just to hit the percentages.

## 8. Notes for the next verification pass

- Verify: first census of Nepal (1911), first five-year plan (1956),
  Nepal Academy establishment, National Human Rights Commission (2000),
  first president Ram Baran Yadav elected (21 July 2008), Rastriya
  Banijya Bank founding (23 Jan 1966), Bir Hospital founding (1890?).
- Re-check the Sugauli Treaty BS-year typo (1873) if the NepJOL article is
  ever cited elsewhere.
- The Supreme Court lineage (Pradhan Nyayalaya roots 1940, reconstituted
  1952) and the CIAA predecessor (CPAA conceived 1975, established 1977)
  are noted here as lineage, not competing establishment dates.
