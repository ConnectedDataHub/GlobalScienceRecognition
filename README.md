# Recognition fragmentation and the diffusion of ideas in global science

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24322474.svg)](https://doi.org/10.5281/zenodo.24322474)

Code and processed data for the paper

> Alexander J. Gates, Jianjian Gao and Indraneel Mane. *Recognition fragmentation and the diffusion of ideas in global science.*

## Repository structure

```
code/      notebooks and scripts that build the data, run the analyses and draw the figures and tables
data/      processed country-level data read by notebooks 3 to 22
figures/   figures of the paper (main text and Supplementary Information)
tables/    LaTeX regression tables (Table 1 and Supplementary Tables S6, S8, S10 and S11)
```

The code also writes these folders when it runs:

```
Source Data/   the data behind each figure and table, one Excel file each, with a README.txt
figures/       regenerated figures
```

[`code/README.txt`](code/README.txt) describes each notebook in detail: its inputs, its outputs, and the
figures and tables it makes.

## Notebooks

| Step | Notebook or script | Produces |
|---|---|---|
| 1 | `1_GlobalCitationNetwork_dataprep.ipynb` | country citation counts and covariates from OpenAlex |
| 2 | `2_GlobalCitationNetwork_citationpreferences.ipynb` | national citation preferences and the journal bootstrap |
| 3–4 | `3_…_Fig1.py`, `4_…_Fig2.py` | Figs. 1 and 2 |
| 5–7 | `5_…_Fig3`, `6_…_Fig4_TableS10`, `7_…_Table1_ideadiffusion` | Figs. 3 and 4, Table 1, Supplementary Table S10 |
| 8 | `8_…_FigS18_randomnullmodelcomparison` | Supplementary Fig. S18 (null models) |
| 9–22 | `9_…` to `22_…` | the other Supplementary Figures (S1–S17) and Tables (S3–S12) |

**What runs with this repository:** notebooks 1 and 2, and the null-model cells of notebook 8, need the full
OpenAlex database. They are included to document how the processed data were made. Scripts 3 and 4, notebooks
5 to 7 and 9 to 22, and the comparison part of notebook 8 only need the files in `data/`.

## Running the code

1. Install Python 3 and the packages listed under Requirements.
2. Run the notebooks from the `code` folder. They read `../data` and write `../Source Data` and `../figures`.
3. Notebooks that read the raw OpenAlex data need paths set at the top of the notebook:
   - `path2openalex`: the OpenAlex database in pySciSci format (notebooks 1 and 2, and the null-model
     cells 3 and 5 of notebook 8)
   - `path2countrydata`: the folder for the processed country-level data (notebooks 1 and 2)

For example:

```bash
cd code
python 3_GlobalCitationNetwork_Fig1.py
jupyter nbconvert --to notebook --execute 5_GlobalCitationNetwork_Fig3.ipynb
```

## Requirements

Python 3 with:
- pandas, numpy, scipy, statsmodels, scikit-learn, networkx and nltk
- matplotlib, seaborn and SciencePlots
- openpyxl, for the Source Data Excel files
- [pySciSci](https://github.com/SciSciCollective/pyscisci)

## Data

The primary data source is [OpenAlex](https://openalex.org/). The country covariates come from:
- the World Bank (GDP per capita and population)
- Melitz and Toubal (official spoken languages)
- the CEPII GeoDist dataset (geographic distance and continent)
- Nicolas et al. (bilateral Science and Technology Agreements)

`data/` holds the processed country-level files derived from these sources. The publication-level OpenAlex data
are not included because of their size.

## Citation

This repository is archived on Zenodo (version 1.0.0): [doi:10.5281/zenodo.24322474](https://doi.org/10.5281/zenodo.24322474).
If you use the code, please cite the paper and this archive.

## Contact

Alexander J. Gates, School of Data Science, University of Virginia (agates@virginia.edu).

## License

MIT License; see [LICENSE](LICENSE).
