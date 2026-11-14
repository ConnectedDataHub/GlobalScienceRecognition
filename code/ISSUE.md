# Open issues

Open issues found while preparing the code, Source Data and figures for the Nature Communications
revision. File names refer to this `code` folder unless stated otherwise.

## 1. Missing data (needed from the co-author)

| Missing file | Needed for | Effect |
|---|---|---|
| `oa_countrycites_nosameorg.csv.gz` (article-level country citations, the original used for Fig. 1) | Fig. 1 scatter plots (citation distributions of JP→CH/AU/IN, 2017) | `SourceData_1_Fig1.xlsx` only has the AUC, N, Z-score and p-value of the three pairs, not the plotted distributions. The later build in `BootstrapData/oa_countrycites_nosameorg_journal.csv.gz` gives slightly different values (CH: N = 10,849 vs 10,884; AUC = 0.5352 vs 0.5360), so it was not used. |
| `oa_pub2country.csv.gz` (country of every publication) | Supplementary Fig. S11B and Fig. S13 (2017 citation network) | Not reproduced. The citing publications in `pub2ref2017.csv.gz` are from 2018–2022; only 3% are covered by `coauthor2017.csv.gz`. |
| `random_country_citation_network2017.csv.gz`, `oa_countrycites_noselfauthoraff_randgraph_auc.csv.gz` (in `/Users/hgt6rn/Downloads/`) | Supplementary Fig. S18 (`8_GlobalCitationNetwork_FigS18_randomnullmodelcomparison.ipynb`) | Notebook 8 cannot run; its inputs are not in Source Data. |

## 2. Bugs in the code

- **`8_GlobalCitationNetwork_FigS18_randomnullmodelcomparison.ipynb`, cell 13**: the Z-score of the random
  citation graph is computed from the other null model:
  `randcitegraph['Zscore'] = (rand_country_auc['AUC'] - 0.5)/np.sqrt(rand_country_auc['Cov'])`.
  It should use `randcitegraph`. This affects the "Random Citation" curve of Supplementary Fig. S18.
- **`2_GlobalCitationNetwork_citationpreferences.ipynb`, cell 3**: `pub2journal = os.path.join(...)` is missing
  `pd.read_csv(...)`, and `path2oa` is not defined.
- **`2_GlobalCitationNetwork_citationpreferences.ipynb`, cell 4**: the closing parenthesis of `os.path.join(...)` in
  `to_csv` is misplaced (`compression=` and the other arguments are passed to `os.path.join`). The output name
  `nationalcitation_bootstrap_u100.csv.gz` also differs from the per-year files
  (`nationalcitation_bootstrap_u100_<year>.csv.gz`) read by the figure notebook.
- **Hard-coded paths** to the co-author's machine (`/Users/hgt6rn/...`) in notebooks 1, 2 and 8.

## 3. Inconsistencies between figures, tables and text

- **Standardization of the regression models (Fig. 3A, Fig. 4A).** The submitted Fig. 3A and Fig. 4A
  (`paper/Figures`) were drawn with the continuous variables standardized once over the whole panel, while
  Supplementary Tables S6 and S10 standardize within each model's estimation sample. The fit statistics and
  significance are identical; only the size of the odds ratios differs (e.g. Fig. 3A target top journal
  fraction ≈ 6.5 vs 4.5). Notebooks 5 and 6 now use per-model standardization and match Tables S6 and S10
  exactly. The regenerated figures (`../figures`) have replaced Fig. 3 and Fig. 4 in `../paper/Figures`
  (resolved).
- **Supplementary Table S8** (cumulative network until 2017) has no year fixed effects: its LLR d.f. are 8, 12,
  16, 18, 20 and 24 (two outcomes × the number of variables), and refitting without year dummies reproduces the
  table exactly (Model 6: N = 744,760, pseudo R² = 0.349, log likelihood = −9190.39). The last row of the table,
  "Year FE: Yes", should be "No" (code: `Robustnesscheck1_03_25_2025`, cells 96–97; not yet in this folder).
- **Standardization check of the SI regression tables**: refitting Model 6 shows that Tables S6, S8, S10 and S11
  all use per-model standardization (all coefficients match exactly). The original notebooks found for S8 and
  S11 standardize over the whole panel, so the tables were produced by other versions of the code.
- **Supplementary Fig. S8** (`13_...FigS8_bridgeshubs.ipynb`) keeps country pairs with **N ≥ 2** cited
  articles, not N ≥ 50 as in the rest of the paper (as in the original notebook `Robustnesscheck1_03_25_2025`).
- **Supplementary Fig. S1** (`11_...FigS1_S3_S4_S5.ipynb`) uses the Holm–Sidak correction with
  **α = 0.001**, not 0.01 (as in the original notebook `IncreasingPolarization_analysis_03_21_23`).
- **Supplementary Fig. S12** (`14_...FigS11_S12.ipynb`): the citation preference curve uses the cumulative
  network with `keep='first'` (the first significant preference of each pair), while the rest of the paper uses
  `keep='last'` (the most recent). The citation curve uses `oa_countrycites_noselfauthoraff` (without
  self-citations and same-affiliation citations), and the copy on this machine (`NationalBiasOwn`, June 2025)
  includes four territories (AS, EH, GU, MP) not in the collaboration network; they are dropped (4,067 of
  512,304 rows). The regenerated curves match the published figure.
- **Fig. 2B** shows the negative edges among the 93 countries of the positive network (1,244 edges; CN
  in-degree 64), while Supplementary Table S3 describes the full negative network (145 countries, 1,471 edges;
  CN in-degree 86). The source data follow the figure.
- **Fig. 4B nodes**: 12 of the 105 countries of the journal bootstrap network have no community assignment
  (they are not in the five communities of the original network).
- **Table 1**: the analysis notebook only fitted Model (4); `7_GlobalCitationNetwork_Table1_ideadiffusion.ipynb`
  refits Models (1)–(3) for the Source Data (all values match Table 1).

## 4. Source Data and journal requirements still to do

- **Output Source Data for the Supplementary figures**: notebooks 10 (S6, S7, S9, S10), 11–16 and 8 (S18) do not
  yet write an output Source Data file.
- **Figure legends**: add "Source data are provided as a Source Data file." to every relevant figure legend
  (main text and SI). The Data Availability section already has "Source data are provided with this paper."
- **File size**: `SourceData_3_Fig3A_input.txt` (242 MB) and `SourceData_6_TableS6_input.txt` (190 MB) exceed
  the journal's guidance of about 30 MB per file; deposit them in a repository (e.g. Zenodo) and cite it.
- **Code DOI**: the editor asks for a DOI for the GitHub repository (e.g. via Zenodo), cited in the Code
  Availability statement and the reference list.
- **Captions**: consider stating "continuous variables standardized" in the captions of Fig. 3 and Fig. 4.
- **Network pictures** (Fig. 2, Fig. 4B, Supplementary Figs. S2, S11, S16) were drawn in Gephi; the code
  exports the networks (`../figures/networks`), but the layout is not reproduced by code.
- **`../data` folder**: no longer used by the analysis (only by the converters in `source_data/`); decide
  whether to keep or remove it.

## 5. Environment

- The default Jupyter kernel `python3` (system Python 3.9) fails to start (psutil built for a different CPU
  architecture).
- In the base Anaconda environment, `import pyscisci.all` fails (dask is incompatible with pandas).
- The notebooks run in the conda environment **`database`** (Python 3.11, pandas 1.5.3, statsmodels 0.14.0).
