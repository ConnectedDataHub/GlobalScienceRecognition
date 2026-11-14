import numpy as np 
import pandas as pd

import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

def pvalue2stars(pvalue):
    if pvalue < 0.001:
        return "^{***}"
    elif pvalue < 0.01:
        return "^{**}"
    elif pvalue < 0.05:
        return "^{*}"
    else:
        return ""


def format_pvalue(pvalue):
    # exact p-values to the third decimal; the smallest reported p-value is p < 0.001
    # the braces keep "p <" and its value on the same line in narrow table cells
    if pvalue < 0.001:
        return "${p < 0.001}$"
    return "${p = " + "{:.3f}".format(pvalue) + "}$"


def format_number(x, decimals=2):
    # fixed number of decimals; a value that rounds to zero is shown without a minus sign
    text = "{:.{}f}".format(x, decimals)
    if float(text) == 0:
        text = text.lstrip('-')
    return text


def table_row(varname='const', offset=0, roun=3, modellist=[], namedict={},i=0,j=1):
    
    row_text = namedict[varname] + " & "*(offset+1) + " & ".join([ "$" + format_number(model.params[i][varname], roun) + "$" for model in modellist[offset:]]) + "\\\\ \n"

    row_text += " & "*(offset+1) + " & ".join([ "$(" + format_number(model.conf_int().loc[str(j)].loc[varname]['lower'], roun) + ", " + format_number(model.conf_int().loc[str(j)].loc[varname]['upper'], roun) + ")$" for model in modellist[offset:]]) + "\\\\ \n"
    row_text +=  " & "*(offset+1) + " & ".join([ "S.E.\\,$" + format_number(model.bse[i][varname], roun) + "$; " + format_pvalue(model.pvalues[i][varname]) for model in modellist[offset:]]) + "\\\\ [0.8ex]  \n"

    return row_text

def make_multinomial_latex_table(fit_models, exog_var_sets = [], dep_var = "", namedict = {}, caption_text="",
                                 label="table:multinomialfull", fname=None):
    """
    The LaTeX table of a series of nested multinomial logit models (statsmodels MNLogit) for the positive (1) and
    negative (2) citation preference compared to no preference (0). The year fixed effects are not shown; the
    Year FE row reports whether the models include them. The table is printed, returned and, if fname is given,
    written to the file fname.
    """
    
    Nmodels = len(exog_var_sets)
    empty_cells = " &"*Nmodels
    table_text= """{\\tiny
    \\begin{longtable}{p{0.2\\linewidth}"""+"p{0.12\\linewidth}"*Nmodels+"}"+"""\\caption{\\textbf{""" + caption_text + """} Model coefficients (log-odds of a positive or negative citation preference relative to no preference) with 95\\% confidence intervals in parentheses, followed by the standard error (S.E.) and the exact $p$-value. $p$-values are from two-sided Wald $z$-tests of each coefficient, without adjustment for multiple comparisons. The LLR $\\chi^2$ is a likelihood-ratio test against the intercept-only model.} 
      \\label{""" + label + """} \\\\
      \\hline \\hline \\\\
    \\multicolumn{"""+str(Nmodels+1)+"""}{c}{\\textbf{Dependent variable: Citation preference}} \\\\ \\hline 
     & \\multicolumn{"""+str(Nmodels)+"""}{c}{Model}  \\\\"""
    
    table_text += "\\cline{2-" + str(Nmodels + 1) + "}"

    for icol in range(Nmodels):
        table_text += "& (" + str(icol + 1) + ")"
    
    
    table_text += """\\\\[0.8ex]
    \\hline
    \\endfirsthead"""

    table_text += """\\multicolumn{2}{c}%
      {{\\tablename\\ \\thetable{} -- continued from previous page}} \\\\
      \\hline \\\\"""

    for icol in range(Nmodels):
        table_text += "& (" + str(icol + 1) + ")"

    table_text += """\\\\
      \\hline
      \\endhead """

    table_text += "\\hline"+"&"*(Nmodels+1-2)+ """\\multicolumn{2}{r}{{Continued on next page}} \\\\ \\endfoot
    \\hline
    \\caption*{} \\\\
    \\endlastfoot"""
    
    for title, i, j in [("Positive", 0, 1), ("Negative", 1, 2)]:
        if i == 1:
            table_text += """ \\hline \\\\"""
        table_text += """\\textbf{Citation preference: """ + title + """}""" + empty_cells + """ \\\\ [1.8ex]"""

        # add constant
        table_text += table_row(varname='const', offset=0, roun=3, modellist=fit_models, namedict=namedict,i=i,j=j)

        for offset, varlist in enumerate(exog_var_sets):
            for var in varlist:
                if not 'year' in var:  #skip the year fixed effects
                    table_text += table_row(varname=var, offset=offset, roun=3, modellist=fit_models, namedict=namedict,i=i,j=j)

    table_text += """\\hline 
\\hline \\\\[-1.8ex] \n"""
    
    table_text += "Observations & " + " & ".join([str(int(model.nobs)) for model in fit_models]) + " \\\\ \n"
    table_text += "Pseudo $R^2$ & " + " & ".join([format_number(model.prsquared, 4) for model in fit_models]) + " \\\\ \n"
    table_text += "Log Likelihood & " + " & ".join(["$" + format_number(model.llf, 2) + "$" for model in fit_models]) + " \\\\ \n"

    fstat_text = []
    for model in fit_models:
        fstat_text.append("$" + format_number(model.llr, 2) + "$ (d.f. $= " + str(int(model.df_model)) + "$; " + format_pvalue(model.llr_pvalue) + ")")
        
    table_text += "LLR $\\chi^2$  & " + " & ".join(fstat_text) + " \\\\ \n"

    # the year fixed effects are included if the model has year dummies
    year_fe = ['Yes' if any('year' in str(v) for v in model.params.index) else 'No' for model in fit_models]
    table_text += "Year FE  & " + " & ".join(year_fe) + " \\\\ \n"
    
    table_text += "\\hline \n\\end{longtable} } "

    print(table_text)
    if fname is not None:
        with open(fname, 'w') as outfile:
            outfile.write(table_text + "\n")
    return table_text


def make_multinomial_latex_tables_split(fit_models, exog_var_sets = [], dep_var = "", namedict = {}, caption_text="",
                                        label="table:multinomialfull", fname=None):
    """
    The same multinomial logit models as make_multinomial_latex_table, split into two tables that each fit on one
    page: part a with the coefficients for the positive citation preference (1), and part b with the coefficients
    for the negative citation preference (2) followed by the model statistics (observations, pseudo R2, log
    likelihood, LLR chi2, year fixed effects), which are shared by both parts. The parts are numbered with the
    letters a and b (e.g. Table S6a and S6b), so the numbers of the other tables do not change; \\ref{label} gives
    the table number (S6), and \\ref{label:positive} and \\ref{label:negative} the parts. The tables are printed,
    returned and, if fname is given, written to the file fname.
    """

    Nmodels = len(exog_var_sets)
    test_text = ("$p$-values are from two-sided Wald $z$-tests of each coefficient, without adjustment for multiple "
                 "comparisons.")

    # the table number without a letter, for \ref{label}
    table_text = "\\refstepcounter{table}\\label{" + label + "}\\addtocounter{table}{-1}%\n"

    for part, title, i, j in [("a", "Positive", 0, 1), ("b", "Negative", 1, 2)]:
        caption = ("\\textbf{" + caption_text + " (" + part + ") " + title + " citation preference.} "
                   "Model coefficients (log-odds of a " + title.lower() + " citation preference relative to no preference) "
                   "with 95\\% confidence intervals in parentheses, followed by the standard error (S.E.) and the exact "
                   "$p$-value. " + test_text)
        if part == "a":
            caption += (" The coefficients for the negative citation preference and the model statistics are in "
                        "Table \\ref{" + label + ":negative}.")
        else:
            caption += (" The coefficients for the positive citation preference are in Table \\ref{" + label +
                        ":positive}; the model statistics are shared by both parts. The LLR $\\chi^2$ is a "
                        "likelihood-ratio test against the intercept-only model.")

        table_text += "\\begin{table}[H]\n"
        if part == "b":
            # part b keeps the number of part a
            table_text += "\\addtocounter{table}{-1}\n"
        table_text += "\\let\\origthetable\\thetable\\renewcommand{\\thetable}{\\origthetable " + part + "}\n"
        table_text += "\\caption{" + caption + "}\n"
        table_text += "\\label{" + label + (":positive" if part == "a" else ":negative") + "}\n"
        table_text += "\\centering\n{\\tiny\n\\begin{tabular}{p{0.2\\linewidth}" + "p{0.11\\linewidth}"*Nmodels + "}\n"
        table_text += "\\hline \\hline \\\\[-1.8ex]\n"
        table_text += ("\\multicolumn{" + str(Nmodels+1) + "}{c}{\\textbf{Dependent variable: Citation preference ("
                       + title.lower() + " vs no preference)}} \\\\ \\hline \n")
        table_text += " & \\multicolumn{" + str(Nmodels) + "}{c}{Model} \\\\"
        table_text += "\\cline{2-" + str(Nmodels + 1) + "}"
        for icol in range(Nmodels):
            table_text += "& (" + str(icol + 1) + ")"
        table_text += "\\\\[0.8ex]\n\\hline \\\\[-1.8ex]\n"

        # add constant
        table_text += table_row(varname='const', offset=0, roun=3, modellist=fit_models, namedict=namedict,i=i,j=j)

        for offset, varlist in enumerate(exog_var_sets):
            for var in varlist:
                if not 'year' in var:  #skip the year fixed effects
                    table_text += table_row(varname=var, offset=offset, roun=3, modellist=fit_models, namedict=namedict,i=i,j=j)

        if part == "b":
            table_text += "\\hline \n\\hline \\\\[-1.8ex] \n"
            table_text += "Observations & " + " & ".join([str(int(model.nobs)) for model in fit_models]) + " \\\\ \n"
            table_text += "Pseudo $R^2$ & " + " & ".join([format_number(model.prsquared, 4) for model in fit_models]) + " \\\\ \n"
            table_text += "Log Likelihood & " + " & ".join(["$" + format_number(model.llf, 2) + "$" for model in fit_models]) + " \\\\ \n"

            fstat_text = []
            for model in fit_models:
                fstat_text.append("$" + format_number(model.llr, 2) + "$ (d.f. $= " + str(int(model.df_model)) + "$; " + format_pvalue(model.llr_pvalue) + ")")
            table_text += "LLR $\\chi^2$  & " + " & ".join(fstat_text) + " \\\\ \n"

            # the year fixed effects are included if the model has year dummies
            year_fe = ['Yes' if any('year' in str(v) for v in model.params.index) else 'No' for model in fit_models]
            table_text += "Year FE  & " + " & ".join(year_fe) + " \\\\ \n"

        table_text += "\\hline \n\\end{tabular}\n}\n\\end{table}\n"

    print(table_text)
    if fname is not None:
        with open(fname, 'w') as outfile:
            outfile.write(table_text + "\n")
    return table_text


def glm_table_row(varname='const', offset=0, roun=3, modellist=[], namedict={}):
    # one variable of the GLM table: coefficient, confidence interval, standard error and p-value
    row_text = namedict.get(varname, varname) + " & "*(offset+1) + " & ".join([ "$" + format_number(model.params[varname], roun) + "$" for model in modellist[offset:]]) + "\\\\ \n"
    row_text +=  " & "*(offset+1) + " & ".join([ "$(" + format_number(model.conf_int().loc[varname][0], roun) + ", " + format_number(model.conf_int().loc[varname][1], roun) + ")$" for model in modellist[offset:]]) + "\\\\ \n"
    row_text +=  " & "*(offset+1) + " & ".join([ "S.E.\\,$" + format_number(model.bse[varname], roun) + "$; " + format_pvalue(model.pvalues[varname]) for model in modellist[offset:]]) + "\\\\ [0.8ex]  \n"
    return row_text


def make_glm_latex_table(fit_models, exog_var_sets = [], namedict = {}, caption_text="", dep_var_text="",
                         label="table:", use_const = True, use_adj_box = True, fname=None):
    """
    The LaTeX table of a series of nested GLM models (statsmodels GLM, e.g. the weighted logistic regression for
    idea diffusion). The table is printed, returned and, if fname is given, written to
    the file fname.
    """
    Nmodels = len(exog_var_sets)

    table_text = """\\begin{table}[H] \\centering 
    \\small
  \\caption{""" + caption_text + """} 
\\label{""" + label + """}"""
    if use_adj_box:
        table_text += """\n\\begin{adjustbox}{max width=\\textwidth} \n"""
    
    table_text += """\\begin{tabular}{l""" + "l"*Nmodels + "}"
    
    table_text += """\\\\[-1.8ex]\\hline 
\\hline \\\\[-1.8ex] 
\\multicolumn{""" + str(Nmodels+1) + """}{c}{Dependent variable: """ + dep_var_text + """} \\\\[0.8ex]\\hline 
 & \\multicolumn{""" + str(Nmodels) + """}{c}{Model}  \\\\ """
    
    table_text += "\\cline{2-" + str(Nmodels + 1) + "} \\\\[-1.8ex] "
    
    for icol in range(Nmodels):
        table_text += "& (" + str(icol + 1) + ")"
    
    table_text += " \\\\ \\hline \\\\[-1.8ex] \n"
    
    # add constant
    if use_const:
        table_text += glm_table_row(varname='const', offset=0, roun=3, modellist=fit_models, namedict=namedict)
    
    for offset, varlist in enumerate(exog_var_sets):
        for var in varlist:
            table_text += glm_table_row(varname=var, offset=offset, roun=3, modellist=fit_models, namedict=namedict)
    
    table_text += """\\hline 
\\hline \\\\[-1.8ex] \n"""
    
    table_text += "Observations & " + " & ".join([str(int(model.nobs)) for model in fit_models]) + " \\\\ \n"
    table_text += "pseudo-$R^2$ & " + " & ".join([format_number(model.pseudo_rsquared(kind='mcf'), 4) for model in fit_models]) + " \\\\ \n"
    table_text += "Log Likelihood & " + " & ".join(["$" + format_number(model.llf, 2) + "$" for model in fit_models]) + " \\\\ \n"
    
    fstat_text = []
    for model in fit_models:
        A = np.identity(len(model.params))
        f_test = model.f_test(A[1:,:])
        fstat_text.append("$" + format_number(f_test.fvalue, 2) + "$ (d.f. $= " + str(int(f_test.df_num)) + "$; " + format_pvalue(f_test.pvalue) + ")")
        
    table_text += "F statistic & " + " & ".join(fstat_text) + " \\\\ \n"
    table_text += "\\hline \n\\end{tabular}"
    if use_adj_box:
        table_text += """\n\\end{adjustbox}"""
    
    table_text += "\n\\end{table}"

    print(table_text)
    if fname is not None:
        with open(fname, 'w') as outfile:
            outfile.write(table_text + "\n")
    return table_text

def logistic_coefficient_plot(df1, df2, colours, Model_features, ax=None):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(5,12))
    
    
    df1s=df1[df1['pvalues']<=0.05]
    df1ns=df1[df1['pvalues']>0.05]

    df2s=df2[df2['pvalues']<=0.05]
    df2ns=df2[df2['pvalues']>0.05]

    x1s = df1s['risk']
    y1s = np.array(df1s.index.to_list())-0.2
    xerror1s = df1s['xerror']

    x1ns = df1ns['risk']
    y1ns = np.array(df1ns.index.to_list())-0.2
    xerror1ns = df1ns['xerror']

    x2s = df2s['risk']
    y2s = np.array(df2s.index.to_list())+0.2
    xerror2s = df2s['xerror']

    x2ns = df2ns['risk']
    y2ns = np.array(df2ns.index.to_list())+0.2
    xerror2ns = df2ns['xerror']
    
    y=df1.index.to_list()
    
    ax.errorbar(x1s, y1s, xerr=xerror1s, fmt='o',color=colours[1],label="Positive recognition",ms=4)
    ax.errorbar(x2s, y2s, xerr=xerror2s, fmt='o',color=colours[2],label="Negative recognition",ms=4)
    
    ax.errorbar(x1ns, y1ns, xerr=xerror1ns, fmt='o',color=colours[1],mfc='w',mew=1,label="Positive recognition(not sig)",ms=4)
    ax.errorbar(x2ns, y2ns, xerr=xerror2ns, fmt='o',color=colours[2],mfc='w',mew=1,label="Negative recognition(not sig)",ms=4)

    #ax.errorbar(x1ns, y1ns, xerr=xerror1ns, fmt='o',color=colours[1],label="Positive recognition(not sig)",ms=4, alpha=0.5)
    #ax.errorbar(x2ns, y2ns, xerr=xerror2ns, fmt='o',color=colours[2],label="Negative recognition(not sig)",ms=4, alpha=0.5)

    ax.invert_yaxis()
    
    ax.axvline(x=0, color=colours[0],  linestyle='--',ymin=0,ymax=0.98)

    sns.despine(top=True, right=True, left=True, bottom=False)

    ylabels=df1['item']
    ax.set_yticks(y)
    ax.set_yticklabels(ylabels)
    ax.set_xticks([-3,-2,-1,0,1,2,3,4])
    ax.tick_params(axis="both", which="both", bottom=True, top=False,    
                    labelbottom=True, left=False, right=False, labelleft=True,labelsize=9) 

    ax.set_ylim([len(Model_features)+2.5,0])
    ax.set_xlabel("Regression coefficient",fontsize=10)

    hlines=y
    counter=0
    for ix in hlines: 
        if counter % 2 == 0:
            ax.axhspan(ix - 0.5, ix + 0.5, color=colours[0],alpha=0.3, zorder=0,lw=0)
        counter += 1


    plt.legend(bbox_to_anchor=(-0.3, 0.55, 0.5, 0.5),
        fontsize=10,
               loc="upper left",
               ncol=2,
               markerscale=1,
               frameon=False,
               handletextpad=.1,
               columnspacing=.2)
    
    return ax


def logistic_odds_ratio_plot(df1, df2, colours, ax=None):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(5,12))
    
    
    df1s=df1[df1['pvalues']<=0.05]
    df1ns=df1[df1['pvalues']>0.05]

    df2s=df2[df2['pvalues']<=0.05]
    df2ns=df2[df2['pvalues']>0.05]

    x1s = df1s['odds_risk']
    y1s = np.array(df1s.index.to_list())-0.2
    xerror1s = [df1s['odds_risk']-df1s['odds_0'], df1s['odds_1']-df1s['odds_risk']]


    x1ns = df1ns['odds_risk']
    y1ns = np.array(df1ns.index.to_list())-0.2
    xerror1ns = [df1ns['odds_risk']-df1ns['odds_0'], df1ns['odds_1']-df1ns['odds_risk']]

    x2s = df2s['odds_risk']
    y2s = np.array(df2s.index.to_list())+0.2
    xerror2s = [df2s['odds_risk']-df2s['odds_0'], df2s['odds_1']-df2s['odds_risk']]

    x2ns = df2ns['odds_risk']
    y2ns = np.array(df2ns.index.to_list())+0.2
    xerror2ns = [df2ns['odds_risk']-df2ns['odds_0'], df2ns['odds_1']-df2ns['odds_risk']]
    
    y=df1.index.to_list()
    
    ax.errorbar(x1s, y1s, xerr=xerror1s, fmt='o',color=colours[1],label="Positive recognition",ms=4)
    ax.errorbar(x2s, y2s, xerr=xerror2s, fmt='o',color=colours[2],label="Negative recognition",ms=4)
    
    ax.errorbar(x1ns, y1ns, xerr=xerror1ns, fmt='o',color=colours[1], mfc='w', mew=1,label="Positive recognition(not sig)", ms=4)
    ax.errorbar(x2ns, y2ns, xerr=xerror2ns, fmt='o',color=colours[2], mfc='w', mew=1,label="Negative recognition(not sig)", ms=4)

    ax.invert_yaxis()
    ax.set_xscale('log', base=10)
    
    from matplotlib.ticker import ScalarFormatter
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    formatter.set_useMathText(False)
    ax.xaxis.set_major_formatter(formatter)


    ax.axvline(x=1, color=colours[0],  linestyle='--',ymin=0,ymax=0.98)

    sns.despine(top=True, right=True, left=True, bottom=False)

    ylabels=df1['item']
    ax.set_yticks(y)
    ax.set_yticklabels(ylabels)
    ax.tick_params(axis="both", which="both", bottom=True, top=False,    
                    labelbottom=True, left=False, right=False, labelleft=True,labelsize=9) 

    ax.set_ylim([max(y)+0.5, min(y)-0.5])
    ax.set_xlabel("Odds ratio",fontsize=10)

    hlines=y
    counter=0
    for ix in hlines: 
        if counter % 2 == 0:
            ax.axhspan(ix - 0.5, ix + 0.5, color=colours[0],alpha=0.3, zorder=0,lw=0)
        counter += 1


    plt.legend(bbox_to_anchor=(-0.3, 0.55, 0.5, 0.5),
        fontsize=10,
               loc="upper left",
               ncol=2,
               markerscale=1,
               frameon=False,
               handletextpad=.1,
               columnspacing=.2)
    
    return ax
