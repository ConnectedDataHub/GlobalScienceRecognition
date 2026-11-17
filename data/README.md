# Data for "Global citation network" (national citation preferences)

This folder holds the processed, country-level data read by the code in [`../code`](../code). The files
come from OpenAlex and were produced by notebooks 1, 2 and 8 (see
[`code/README.txt`](../code/README.txt)) or aggregated from publication-level data. The raw OpenAlex
database and the publication-level files are not included because they are too large.

- Countries are two-letter ISO 3166-1 alpha-2 codes.
- All `.csv.gz` files are gzip-compressed CSV files and can be read directly with `pandas.read_csv`.
- The data files are not tracked by git (see [`../.gitignore`](../.gitignore)). Download them from Zenodo,
  [doi:10.5281/zenodo.24322547](https://doi.org/10.5281/zenodo.24322547), into this folder.
- "Used by" lists the numbers of the notebooks and scripts in `code/`.

## Overview

| File | Size | Contents | Used by |
|---|---|---|---|
| `oa_countrycites_nosameorg_auc.csv.gz` | 9.6 MB | National citation preferences (main network) | 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 20 |
| `oa_countrycites_nosameorg_journalbootstrap_auc.csv.gz` | 4.6 MB | Journal bootstrap citation preferences | 6 |
| `oa_countrycites_noselfauthoraff_noselfcite_auc.csv.gz` | 13 MB | Citation preferences without country self-citations | 18 |
| `oa_countrycites_noselfauthoraff_randgraph_auc.csv.gz` | 9.9 MB | Citation preferences of the random citation null model | 8 |
| `link_prediction_panel_data_1990_2017.csv.gz` | 63 MB | Country-pair panel for link prediction | 5, 6, 9, 10, 17, 18, 20 |
| `diffusion_panel_data_1990_2017.csv.gz` | 1.7 MB | Country-pair panel for idea diffusion | 7, 15, 21 |
| `oa_country_productivity.csv` | 236 KB | Publications per country and year | 5, 10 |
| `oa_cocountry_collaboration_network.csv.gz` | 1.6 MB | Yearly country collaboration network | 14 |
| `coauthorship_2017.csv.gz` | 80 KB | 2017 country co-authorship network | 14 |
| `countries_2017.csv.gz` | 4 KB | Countries of the 2017 co-authorship network | 14, 22 |
| `countrycites_yearly.csv.gz` | 1.8 MB | Yearly citations between countries | 14 |
| `citation_network_2017.csv.gz` | 168 KB | Country citations to the 2017 publications, original and randomized | 14, 22 |
| `random_country_citation_network2017.csv.gz` | 455 MB | Citations of the random country null model | 8 |

## National citation preferences

### `oa_countrycites_nosameorg_auc.csv.gz`

The national citation preference of each citing country for the publications of each cited country and
year, without author self-citations and same-organization citations. This is the main network used in
the paper. Output of notebook 2.

| Column | Description |
|---|---|
| `CitingCountry` | citing country |
| `CitedYear` | publication year of the cited publications |
| `CitedCountry` | cited country |
| `AUC` | citation preference (0.5 = no preference) |
| `Cov` | DeLong variance of the AUC |
| `N` | number of cited publications |

### `oa_countrycites_nosameorg_journalbootstrap_auc.csv.gz`

Journal bootstrap citation preferences: mean and STD of the AUC over 100 bootstrap samples stratified by
journal, with the significance test (Holm-Sidak, alpha = 0.01 within each year). Output of notebook 2.
Used for Fig. 4 and Supplementary Table S10.

Columns: `CitingCountry`, `CitedYear`, `CitedCountry`, `AUC`, `N`, `isample`, `STD`, `Zscore`, `pvalue`,
`Significant`

### `oa_countrycites_noselfauthoraff_noselfcite_auc.csv.gz`

Citation preferences recomputed without country self-citations (Supplementary Note 8, Supplementary
Table S11). Same columns as `oa_countrycites_nosameorg_auc.csv.gz`.

### `oa_countrycites_noselfauthoraff_randgraph_auc.csv.gz`

Citation preferences of the random citation graph null model (Supplementary Fig. S18). Built in
notebook 8 (6th cell) from the raw OpenAlex database. Same columns as
`oa_countrycites_nosameorg_auc.csv.gz`.

## Regression panels

### `link_prediction_panel_data_1990_2017.csv.gz`

Country-pair by year panel (1990-2017) of covariates for the multinomial link prediction models
(Fig. 3A, Fig. 4A, Supplementary Tables S6-S11). The prefix `o` is the origin (citing) country and `t`
the target (cited) country. Population, GDP and GDP per capita are log-transformed.

| Column | Description |
|---|---|
| `oCountry`, `tCountry` | origin and target country |
| `year` | year |
| `oPop`, `oGDP`, `oGDP_PCAP`, `tPop`, `tGDP`, `tGDP_PCAP` | population, GDP and GDP per capita |
| `comlang_off` | common official language |
| `PhysicalDistance` | distance between the countries |
| `CollabStrength` | collaboration strength |
| `oTopFrac`, `tTopFrac` | share of publications in top journals |
| `cumulative_laws` | cumulative laws |
| `oContinent`, `tContinent`, `SameContinent` | continents and whether they are the same |
| `TopicSimilarity` | topic similarity |

### `diffusion_panel_data_1990_2017.csv.gz`

Country-pair panel for the idea diffusion regression (Table 1, Supplementary Fig. S14, Supplementary
Table S12): for each origin country, target country and idea, whether the idea spread, with the
covariates of both countries. The suffix `_o` is the origin and `_d` the destination country; `_x` and
`_y` are the merged productivity columns of the two countries.

Columns: `Origin`, `Country`, `Idea`, `Norigin`, `Ntarget`, `Fideas`, `Pedge`, `Nedge`, `SameComm`,
`Year_x`, `NumPub_d`, `TopJournal_x`, `FracTop_x`, `Year_y`, `NumPub_o`, `TopJournal_y`, `FracTop_y`,
`Ncites`, `NormNcites`, `logNormNcites`, `GDP_d`, `Pop_d`, `GNI_d`, `GDP_PCAP_d`, `GNI_PCAP_d`, `GDP_o`,
`Pop_o`, `GNI_o`, `GDP_PCAP_o`, `GNI_PCAP_o`, `comlang_off`, `dist`, `iCountry`, `jCountry`,
`FieldDistance`, `eSign`, `pr_o`, `pr_d`

## Country productivity and collaboration

### `oa_country_productivity.csv`

Publications per country and year.

Columns: `Year`, `Country`, `NumPub`, `TopJournal` (publications in top journals), `FracTop` (their share)

### `oa_cocountry_collaboration_network.csv.gz`

Yearly country collaboration network (number of co-authored publications).

Columns: `Year`, `oCountry`, `tCountry`, `CollabStrength`

### `coauthorship_2017.csv.gz`

2017 country co-authorship network (Supplementary Figs. S11A and S12), aggregated from the
publication-level co-authorship data (not included).

Columns: `Country1`, `Country2`, `CoauthorshipStrength`

### `countries_2017.csv.gz`

The countries of the 2017 co-authorship network.

Columns: `Country`

### `countrycites_yearly.csv.gz`

Yearly citations between countries, without self-citations and same-affiliation citations, aggregated
from the publication-level citation data (not included).

Columns: `Year`, `CitingCountry`, `Country` (cited country), `CountryCitations`

## Citation networks of the 2017 publications

### `citation_network_2017.csv.gz`

Citations from each citing country to the 2017 publications of each cited country, original and with the
cited country permuted (fixed random seed). Used for Supplementary Figs. S11B and S13. Aggregated from
the publication-level citations to the 2017 publications (not included).

Columns: `CitingCountry`, `CitedCountry`, `Citations`, `RandomizedCitations`

### `random_country_citation_network2017.csv.gz`

Publication-level citations of the random country null model, with the country of each publication
permuted within its year (Supplementary Fig. S18). Built in notebook 8 (4th cell) from the raw OpenAlex
database.
An empty country means the publication has no country.

Columns: `CitingPublicationId`, `CitingYear`, `CitedPublicationId`, `CitedYear`, `CitingCountry`,
`CitedCountry`

## Files referenced by the code but not in this folder

| File | Description |
|---|---|
| `Chengetal_idealist.csv.gz` | list of scientific ideas (n-grams) used to track idea diffusion (input of notebook 1) |
| `pub2ref2017.csv.gz`, `oa_pub2country.csv.gz` | publication-level citations to the 2017 publications and the countries of each publication, from which `citation_network_2017.csv.gz` was built; too large for the repository |

Notebooks 1, 2 and 8 also need the raw OpenAlex database (pySciSci format); see
[`code/README.txt`](../code/README.txt).
