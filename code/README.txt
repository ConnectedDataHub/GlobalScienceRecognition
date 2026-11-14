Code for "Global citation network" (national citation preferences)
====================================================================

This folder contains the code used to build the national citation preference
networks, run the analyses, and generate the figures, tables and Source Data.

Run order
---------
1_GlobalCitationNetwork_dataprep.ipynb                          (needs the raw OpenAlex database)
2_GlobalCitationNetwork_citationpreferences.ipynb               (needs outputs of 1)
3_GlobalCitationNetwork_Fig1.py                                 Fig. 1
4_GlobalCitationNetwork_Fig2.py                                 Fig. 2
5_GlobalCitationNetwork_Fig3.ipynb                              Fig. 3
6_GlobalCitationNetwork_Fig4_TableS10.ipynb                     Fig. 4 and Supplementary Table S10
7_GlobalCitationNetwork_Table1_ideadiffusion.ipynb              Table 1
8_GlobalCitationNetwork_FigS18_randomnullmodelcomparison.ipynb  Supplementary Fig. S18
                                                                (needs the raw OpenAlex database)
9_GlobalCitationNetwork_TableS6_multinomial.ipynb               Supplementary Table S6
10_GlobalCitationNetwork_FigS6_S7_S9_S10.ipynb                  Supplementary Figs. S6, S7, S9 and S10
11_GlobalCitationNetwork_FigS1_S3_S4_S5.ipynb                   Supplementary Figs. S1, S3, S4 and S5
12_GlobalCitationNetwork_FigS2_S16.ipynb                        Supplementary Figs. S2 and S16 (networks for Gephi)
13_GlobalCitationNetwork_FigS8_bridgeshubs.ipynb                Supplementary Fig. S8
14_GlobalCitationNetwork_FigS11_S12.ipynb                       Supplementary Figs. S11A and S12
15_GlobalCitationNetwork_FigS14_vifdiffusion.ipynb              Supplementary Fig. S14
16_GlobalCitationNetwork_FigS15_S17.ipynb                       Supplementary Figs. S15 and S17
17_GlobalCitationNetwork_TableS8_cumulative.ipynb              Supplementary Table S8
18_GlobalCitationNetwork_TableS11_selfcitations.ipynb          Supplementary Table S11
19_GlobalCitationNetwork_TableS3_S5_networkstats.ipynb          Supplementary Tables S3, S4 and S5
20_GlobalCitationNetwork_TableS7_S9_crossvalidation.ipynb       Supplementary Tables S7 and S9
21_GlobalCitationNetwork_TableS12_diffusioncrossvalidation.ipynb  Supplementary Table S12
22_GlobalCitationNetwork_FigS13_schubertglanzel.ipynb           Supplementary Fig. S13

Notebooks 1, 2 and 8 need the raw OpenAlex database and its processed outputs, which are
not included because of their size. Scripts 3 and 4 and notebooks 5, 6, 7 and 9 to 22
only need the processed data in ../data.

The code reads its input from ../data and writes the Source Data (the data behind each figure and table)
to ../Source Data.

Run the notebooks from this code folder (the default in Jupyter and VS Code); the data and Source Data
folders are found one level up. They can also be run from the main folder (the folder that
contains "data" and "Source Data") with this code folder on the Python path (for vizutils.py and
sourcedatautils.py).

Regenerated figures are saved in ../figures (the figures of the submitted paper are in
../paper/Figures).

Paths to set at the top of the notebooks:
  path2openalex     location of the OpenAlex database (pySciSci format)
  path2countrydata  location of the processed country-level data (notebooks 1, 2 and 8)
  path2sourcedata   location of the Source Data folder ("Source Data"); the data folder (path2data) is
                    next to it


Input data (../data)
--------------------
The processed data used by the analyses (outputs of notebooks 1 and 2, and of data_prep/):

oa_countrycites_nosameorg_auc.csv.gz              national citation preference (AUC) for each citing country,
                                                  cited country and year; output of notebook 2
oa_country_productivity.csv                       number of publications per country and year
link_prediction_panel_data_1990_2017.csv.gz       country-pair panel used in the multinomial link prediction
                                                  (Fig. 3A, Fig. 4A, Supplementary Tables S6, S8, S10, S11)
oa_countrycites_nosameorg_journalbootstrap_auc.csv.gz  journal bootstrap national citation preference (mean AUC
                                                  and STD over 100 bootstrap samples stratified by journal);
                                                  output of notebook 2
oa_countrycites_noselfauthoraff_noselfcite_auc.csv.gz  national citation preference without country
                                                  self-citations (Supplementary Table S11)
oa_countrycites_noselfauthoraff_randgraph_auc.csv.gz   national citation preference of the random citation null
                                                  model (Supplementary Fig. S18); computed on the cluster
diffusion_panel_data_1990_2017.csv.gz             country-pair panel used in the idea diffusion regression
Chengetal_idealist.csv.gz                         list of scientific ideas (n-grams) used to track idea diffusion
oa_cocountry_collaboration_network.csv.gz         yearly country collaboration network
coauthorship_2017.csv.gz                          2017 country co-authorship network (data_prep/make_data_FigS11_S12.py)
countries_2017.csv.gz                             the countries of the 2017 co-authorship network (same script)
countrycites_yearly.csv.gz                        yearly citations between countries, without self-citations and
                                                  same-affiliation citations (same script)
citation_network_2017.csv.gz                      citations from each citing country to the 2017 publications of each
                                                  cited country, original and with the cited country permuted
                                                  (Supplementary Figs. S11B and S13; data_prep/make_data_FigS13_S18.py)
oa_countrycites_randcountry2017_auc.csv.gz        national citation preference of the random country null model for
                                                  the 2017 publications (Supplementary Fig. S18; same script)
pub2ref2017.csv.gz, oa_pub2country.csv.gz         publication-level inputs of data_prep/make_data_FigS13_S18.py: the
                                                  citations to the 2017 publications within 5 years (without author
                                                  self-citations and same-affiliation citations) and the countries of
                                                  each publication; too large for the repository


1_GlobalCitationNetwork_dataprep.ipynb
--------------------------------------
Builds the publication-to-country mapping, the country citation counts, and the country covariates.

Input:
  OpenAlex database (path2openalex): publications, affiliations, publication-author-affiliation,
    pub2ref, pub2field, publication abstracts
  ../data/Chengetal_idealist.csv.gz

Output (path2countrydata):
  oa_pub2country.csv.gz                    publication to country(ies)
  oa_countryproductivity.csv.gz            publications per country
  oa_countryproductivity_yearly.csv.gz     publications per country and year
  oa_c5.csv.gz                             5-year citations of each publication
  oa_countrycites.csv.gz                   citations from each country to each publication
  oa_countrycites_noself.csv.gz            same, without author self-citations
  oa_countrycites_nosameorg.csv.gz         same, without author self-citations and same-organization
                                           citations (used in the paper)
  oa_countrycites_nosameorg_journal.csv.gz same as above with the cited journal (for the journal bootstrap)
  oa_cocountry_collaboration_network.npy   country collaboration network
  oa_cocountry_collaboration_network_country2int.json  country index of the collaboration network
  oa_journal_diversity.csv.gz, oa_country_journal_diversity.csv.gz   journal diversity
  oa_global_topic2_diversity.csv.gz, oa_country_topic1_diversity.csv.gz,
  oa_country_topic2_diversity.csv.gz       topic diversity
  oa_journal_field_meanlogc5.csv.gz, oa_yearly_top_journals.csv.gz,
  oa_countrytopproductivity.csv.gz, oa_globaltopjournal.csv.gz   top journal publications
  pub2idea/pub2idea*.csv.gz (path2openalex)  ideas found in each publication abstract


2_GlobalCitationNetwork_citationpreferences.ipynb
-------------------------------------------------
Computes the national citation preference (AUC with DeLong variance) for every citing country,
cited country and year, and the journal bootstrap version.

Input:
  oa_countrycites_nosameorg.csv.gz         (output of notebook 1)
  pub2journal.csv.gz                       (OpenAlex)

Output:
  oa_countrycites_nosameorg_auc.csv.gz     national citation preferences (provided in
                                           ../data)
  nationalcitation_bootstrap_u100.csv.gz   journal bootstrap citation preferences (Fig. 4)


3_GlobalCitationNetwork_Fig1.py
-------------------------------
Builds the Source Data for Fig. 1. Run from this folder with:  python 3_GlobalCitationNetwork_Fig1.py

Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz
Output: ../Source Data/SourceData_1_Fig1.xlsx
        ../Source Data/README.txt


4_GlobalCitationNetwork_Fig2.py
-------------------------------
Builds the Source Data for Fig. 2. Run from this folder with:  python 4_GlobalCitationNetwork_Fig2.py

Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz
Output: ../Source Data/SourceData_2_Fig2.xlsx
        ../Source Data/README.txt


Notebooks 5 to 10
-----------------
Each notebook has the shared set-up (imports, significance test, cumulative network) and the cells its
display items need. Each runs on its own from the files in ../data, except notebook 8, which needs the raw
OpenAlex database.

5_GlobalCitationNetwork_Fig3.ipynb
  Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz,
          ../data/oa_country_productivity.csv, ../data/link_prediction_panel_data_1990_2017.csv.gz, vizutils.py
  Output: Fig. 3: A) odds ratios of the multinomial logit model (Model 6 of Supplementary Table S6),
          B, C) positive and negative in-degree over time, D) normalized entropy of the PageRank
          centrality, E) negative connection probability between communities
          ../figures/Fig3_networkfeatures.pdf
          ../Source Data/SourceData_3_Fig3.xlsx (Source Data for Fig. 3, last cell: plotted values,
          significant citation preferences and communities)
          ../Source Data/README.txt

6_GlobalCitationNetwork_Fig4_TableS10.ipynb
  Input:  ../data/oa_countrycites_nosameorg_journalbootstrap_auc.csv.gz,
          ../data/link_prediction_panel_data_1990_2017.csv.gz, vizutils.py,
          ../paper/Figures/Fig4B_bootstrapnetwork.png (the network picture of B)
  Output: Fig. 4: A) odds ratios of the multinomial logit model of the journal bootstrap citation
          preferences (1990-2017; continuous variables standardized once over the panel,
          as in Fig. 3), B) the journal bootstrap network (positive edges); the six models are those of
          Supplementary Table S10
          ../figures/Fig4_bootstrapnetworkfeatures.pdf
          Supplementary Table S10 (LaTeX): ../tables/TableS10.tex, and split into S10a (positive) and S10b
          (negative and model statistics), each on one page: ../tables/TableS10_split.tex
          the comparison of the original (N1) and journal bootstrap (N2) networks reported in the main text
          (printed, and in the sheet "N1 vs N2" of SourceData_4_Fig4.xlsx)
          ../Source Data/SourceData_4_Fig4.xlsx (Source Data for Fig. 4, last cell: odds ratios of A,
          nodes and positive edges of B, N1 vs N2 comparison)
          ../Source Data/SourceData_10_TableS10.xlsx (Source Data for Supplementary Table S10, last cell:
          coefficients and fit of the six models)
          ../Source Data/README.txt

7_GlobalCitationNetwork_Table1_ideadiffusion.ipynb
  Input:  ../data/diffusion_panel_data_1990_2017.csv.gz
  Output: Table 1: weighted logistic regression for idea diffusion (odds ratios, pseudo R2, VIF)
          ../Source Data/SourceData_5_Table1.xlsx (Source Data for Table 1, Models 1-4, last cell)
          ../Source Data/README.txt

9_GlobalCitationNetwork_TableS6_multinomial.ipynb
  Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz,
          ../data/link_prediction_panel_data_1990_2017.csv.gz, vizutils.py
  Output: Supplementary Table S6: fixed-effect multinomial logit regression for 1990-2017 (LaTeX),
          and the Wald tests comparing the positive and negative coefficients
          Supplementary Table S6 split into S6a (positive) and S6b (negative and model statistics), each on one
          page: ../tables/TableS6_split.tex
          ../Source Data/SourceData_6_TableS6.xlsx (Source Data for Supplementary Table S6, last cell)
          ../Source Data/README.txt

10_GlobalCitationNetwork_FigS6_S7_S9_S10.ipynb
  Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz,
          ../data/oa_country_productivity.csv, ../data/link_prediction_panel_data_1990_2017.csv.gz
  Output: Supplementary Fig. S6 (FigSI_CorrDegreePubs), Fig. S7 (FigSI_ProbEdgeSignPubs),
          Fig. S9 (FigSI_connectionprob) and Fig. S10 (FigSI_VIF_multi)


8_GlobalCitationNetwork_FigS18_randomnullmodelcomparison.ipynb
-------------------------------------------------------
Builds two null models (random country assignment and random citation graph) and compares their
citation preferences with the empirical network.

The null models are built from the raw OpenAlex database (cells 4 and 6). The comparison with the
empirical network (from "Compare the resulting networks") only needs the data folder: the random citation
null (oa_countrycites_noselfauthoraff_randgraph_auc.csv.gz) and the random country null for the 2017
publications (oa_countrycites_randcountry2017_auc.csv.gz, from data_prep/make_data_FigS13_S18.py).

Input:
  OpenAlex database: pub2doctype, pub2year, affiliations, publication-author-affiliation, pub2ref
  oa_pub2country.csv.gz                    (output of notebook 1)
  ../data/oa_countrycites_nosameorg_auc.csv.gz
  ../data/oa_countrycites_noselfauthoraff_randgraph_auc.csv.gz  (citation preferences of the random citation null)
  ../data/oa_countrycites_randcountry2017_auc.csv.gz           (citation preferences of the random country null)

Output:
  random_country_citation_network2017.csv.gz            random country null model citations
  oa_countrycites_noselfauthoraff_randgraph.csv.gz      random citation null model citations
  ../figures/FigSI_random_network_auc_dist.pdf          Supplementary Fig. S18
  ../Source Data/SourceData_FigS18.xlsx                 Source Data for Supplementary Fig. S18 (last cell)
  ../Source Data/README.txt


Notebooks 11 to 16: Supplementary Figures
-----------------------------------------
They read their input from ../data and save the figures in ../figures.

11_GlobalCitationNetwork_FigS1_S3_S4_S5.ipynb
  Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz
  Output: Supplementary Fig. S1 (four panels: ../figures/FigSI_globalpolitics_*.pdf; significance with the
          Holm-Sidak correction at alpha = 0.001),
          Fig. S3 (../figures/FigSI_AUCdist.pdf), Fig. S4 (../figures/SI_aucdeviation.pdf),
          Fig. S5 (../figures/FigSI_InterCommunityEdgeWeights.pdf)

12_GlobalCitationNetwork_FigS2_S16.ipynb
  Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz
  Output: the cumulative positive networks of 2000, 2005, 2010 and 2017 as gexf files
          (../figures/networks/pos_network_<year>.gexf), drawn in Gephi for Supplementary Figs. S2 and S16

13_GlobalCitationNetwork_FigS8_bridgeshubs.ipynb
  Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz
  Output: Supplementary Fig. S8 (../figures/FigSI_BridgesHubs.pdf); the
          country pairs with at least 2 (not 50) cited articles are kept

14_GlobalCitationNetwork_FigS11_S12.ipynb
  Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz,
          ../data/coauthorship_2017.csv.gz, countries_2017.csv.gz,
          oa_cocountry_collaboration_network.csv.gz, countrycites_yearly.csv.gz,
          citation_network_2017.csv.gz
  Output: Supplementary Fig. S11A and S11B edge lists (../figures/networks/normalized_coauthorship_2017_025.csv
          and normalized_citation_2017_03.csv, drawn in Gephi), Fig. S12 (../figures/FigSI_networkentropy.pdf)
  The S11B edge list is computed from ../data/citation_network_2017.csv.gz (data_prep/make_data_FigS13_S18.py).

15_GlobalCitationNetwork_FigS14_vifdiffusion.ipynb
  Input:  ../data/diffusion_panel_data_1990_2017.csv.gz
  Output: Supplementary Fig. S14 (../figures/FigSI_vif_diffusion.pdf)

16_GlobalCitationNetwork_FigS15_S17.ipynb
  Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz
  Output: Supplementary Fig. S15 (../figures/FigSI_new_edge_share.pdf),
          Fig. S17 (../figures/FigSI_community_pos28.pdf)


17_GlobalCitationNetwork_TableS8_cumulative.ipynb
-------------------------------------------------
Fits the multinomial logit models (1)-(6) on the cumulative citation
preference network till 2017 (each country pair keeps its most recent significant citation preference;
N >= 50, as in the main analysis). The models are cross-sectional: one row per country pair with the
covariates of 2017 (selected before merging with the cumulative edges), and no year fixed effects.

Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz,
        ../data/link_prediction_panel_data_1990_2017.csv.gz, vizutils.py, sourcedatautils.py
Output: Supplementary Table S8 (LaTeX): ../tables/TableS8.tex, and split into S8a (positive) and S8b (negative and
        model statistics), each on one page: ../tables/TableS8_split.tex
        ../Source Data/SourceData_8_TableS8.xlsx (Source Data for Supplementary Table S8, last cell)
        ../Source Data/README.txt


18_GlobalCitationNetwork_TableS11_selfcitations.ipynb
-----------------------------------------------------
Uses the model code of notebook 9. Fits the multinomial logit models (1)-(6) of Supplementary Table S6 on the national citation preferences
recomputed after removing country self-citations (Supplementary Note 8).

Input:  ../data/oa_countrycites_noselfauthoraff_noselfcite_auc.csv.gz,
        ../data/link_prediction_panel_data_1990_2017.csv.gz, vizutils.py, sourcedatautils.py
Output: Supplementary Table S11 (LaTeX): ../tables/TableS11.tex, and split into S11a (positive) and S11b (negative
        and model statistics), each on one page: ../tables/TableS11_split.tex
        ../Source Data/SourceData_11_TableS11.xlsx (Source Data for Supplementary Table S11, last cell)
        ../Source Data/README.txt


19_GlobalCitationNetwork_TableS3_S5_networkstats.ipynb
------------------------------------------------------
Descriptive statistics of the positive and negative networks (Supplementary Table S3: nodes, edges, density,
weakly connected components, average degree and PageRank) and the top 10 countries by in-degree and PageRank
centrality in the positive (Table S4) and negative (Table S5) networks, using the cumulative network of 1990-2017.

Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz, sourcedatautils.py
Output: ../Source Data/SourceData_3_TableS3.xlsx, SourceData_4_TableS4.xlsx, SourceData_5_TableS5.xlsx
        ../Source Data/README.txt


20_GlobalCitationNetwork_TableS7_S9_crossvalidation.ipynb
---------------------------------------------------------
Validates Model (6) of Supplementary Table S6: 5-fold stratified cross-validation (Supplementary Table S7) and a
forecasting validation that trains on 1990-2016 and tests on 2017 (Supplementary Table S9). Performance is
McFadden's pseudo R2 on the held-out data.

Input:  ../data/oa_countrycites_nosameorg_auc.csv.gz, ../data/link_prediction_panel_data_1990_2017.csv.gz,
        sourcedatautils.py
Output: ../Source Data/SourceData_7_TableS7.xlsx, SourceData_9_TableS9.xlsx
        ../Source Data/README.txt


22_GlobalCitationNetwork_FigS13_schubertglanzel.ipynb
-----------------------------------------------------
The country citation network of the 2017 publications and its country-randomized version, the Schubert and
Glanzel normalization, and Supplementary Fig. S13; also prints the Spearman correlations between the original and
randomized raw and normalized citation networks (Supplementary Note 9).

Input:  ../data/citation_network_2017.csv.gz, ../data/countries_2017.csv.gz, sourcedatautils.py
Output: ../figures/FigSI_sgcitenetwork.pdf
        ../Source Data/SourceData_FigS13.xlsx (Source Data for Supplementary Fig. S13, last cell)
        ../Source Data/README.txt


21_GlobalCitationNetwork_TableS12_diffusioncrossvalidation.ipynb
----------------------------------------------------------------
5-fold cross-validation of Model (4) of Table 1, the idea diffusion model (Supplementary Table S12). Performance
is McFadden's pseudo R2 on the held-out data.

Input:  ../data/diffusion_panel_data_1990_2017.csv.gz, sourcedatautils.py
Output: ../Source Data/SourceData_12_TableS12.xlsx
        ../Source Data/README.txt


Source Data of the Supplementary Figures
----------------------------------------
The last cell of each Supplementary Figure notebook writes the plotted values to ../Source Data (and updates
../Source Data/README.txt):

  10_GlobalCitationNetwork_FigS6_S7_S9_S10    SourceData_FigS6.xlsx, SourceData_FigS7.xlsx, SourceData_FigS9.xlsx,
                                              SourceData_FigS10.xlsx
  11_GlobalCitationNetwork_FigS1_S3_S4_S5     SourceData_FigS1.xlsx, SourceData_FigS3.xlsx, SourceData_FigS4.xlsx,
                                              SourceData_FigS5.xlsx
  12_GlobalCitationNetwork_FigS2_S16          SourceData_FigS2.xlsx, SourceData_FigS16.xlsx
  13_GlobalCitationNetwork_FigS8_bridgeshubs  SourceData_FigS8.xlsx
  14_GlobalCitationNetwork_FigS11_S12         SourceData_FigS11.xlsx (panel A), SourceData_FigS12.xlsx
  15_GlobalCitationNetwork_FigS14_vifdiffusion  SourceData_FigS14.xlsx
  16_GlobalCitationNetwork_FigS15_S17         SourceData_FigS15.xlsx, SourceData_FigS17.xlsx

Supplementary Fig. S11B and S13 need the publication-level citation data, and Supplementary Fig. S18 needs the
outputs of the null models computed on the cluster (hpc_code in the analysis folder), which are not included.


vizutils.py
-----------
Helper functions imported by notebooks 5, 6, 9, 17 and 18:
  pvalue2stars, table_row, make_multinomial_latex_table   LaTeX regression tables
  make_multinomial_latex_tables_split                     the same table split into a positive (a) and a negative (b)
                                                          table that each fit on one page
  logistic_coefficient_plot                               coefficient plot (Fig. 3A)
  logistic_odds_ratio_plot                                odds ratio plot (Fig. 4A)


sourcedatautils.py
------------------
Helper functions imported by scripts 3 and 4, notebooks 5, 6, 7, 9 to 22, and data_prep/:
  load_country_auc, load_net_auc      load the citation preferences from ../data and apply the
                                      significance test (N >= 50, Holm-Sidak correction with
                                      alpha = 0.01 within each year)
  cumulative_network                  build the cumulative citation preference network
  comm2country, country2commlabel     the five communities and their labels (1-5)
  write_source_data                   write a Source Data Excel file (README sheet and one table per
                                      sheet) and update ../Source Data/README.txt, which describes
                                      all Source Data files



Software
--------
Python 3 with pandas, numpy, scipy, statsmodels, networkx, matplotlib, seaborn, openpyxl,
and pySciSci (https://github.com/SciSciCollective/pyscisci).
