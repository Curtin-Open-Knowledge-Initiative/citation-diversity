{% import "report_macros.md" as helper with context %} {% include "report_css.html" %}

<!-- Title Page -->
<pdf:nexttemplate name="titlepage">
<pdf:nextpage>

<p class="subtitle">TITLE</p>
<p class="titlemeta"><br>DATE: {{ helper.created_at()|upper }}</p>


<!-- switch page templates -->
<pdf:nexttemplate name="report">

<pdf:nextpage>

# Summary and Abstract

The open access movement aims to remove access barriers to research outputs. It is hypothesised that this helps maximise
an article’s research impact as a result of lowering access restrictions caused by social inequality that favours
wealthier populations. Citations are often interpreted as a measure of impact. Openly accessible articles are said to
have increased citation counts as compared to their closed counterparts. Yet, quantitative studies have shown varied
results across research cohorts. The current literature lacks simple yet strong evidence to support the positive impact
of open access on citations. Here we show that open access outputs garner more diverse citationships across geographies
and disciplines. We perform a large-scale study of citing patterns across paired-samples of open access outputs versus
non-open access outputs using data integrated from multiple sources. We found that the open access groups are cited more
widely across different countries, sub-regions, regions and fields of study. Importantly, there are increased citations
from populations that traditionally have restricted access to closed publications. The results demonstrate a new
perspective to understanding the citation impact of open access practices. It provides a remarkably simple argument in
support of open access publishing, i.e., it gets cited by more authors from more places.

--

The goal of open access is to allow more people to read and use research outputs. An observed association of more highly
cited articles with open access has been claimed as evidence of increased usage but this remains controversial. In
addition, analysis of citation counts is evidence of increased usage, not a wider diversity of usage. We address this
gap by examining the association of open access with the diversity of citations. We show a robust association of a
higher diversity of citation sources by institution, country, region and field for publications from 2010-2020, and that
the effect is seen for both high and medium-low citation counts. Open Access through repositories shows a stronger
effect than open access publishing. Our study provides the first evidence at a global scale that open access is
achieving its goals of research outputs being available to, and used by, wider audiences.

# Article Text

The purpose of research is for it be used, either applied to solve problems and address issues, or more narrowly to
provide insight, capacity and inspiration for further research. The Open Access movement is founded on the goals of
putting research in the hands of more people and making it more usable. A seismic shift in access models has occurred
over the past decade with accessible outputs rising from around 10% of globally indexed outputs published in 2010 to
over 50% of all outputs published in 2020 being accessible in some form.

It has remained challenging to conclusively demonstrate the benefits of this shift. Collection of case studies and
narratives has been important, and a range of studies have sought quantitative evidence of enhanced usage in various
ways. An observed association of increased citation counts with open access to articles has provided the most global
evidence of enhanced usage. However, there are several confounding factors that make claims of a causal link less than
definitive. Specifically, a set of narrowly defined randomised control trials find no effect, and there is an argument
that access to resources and prestige may well be associated both the choice to make an output open access and the
likelihood of higher citations.

In addition to these issues we felt that a focus on citation counts fails to address some of the core goals of open
access, specifically that a wider range of researchers users have more access. Quantitative assessment of citation
source diversity is feasible at scale, and because standard measures of diversity are less sensitive to counts, may
allow us to address the issues of access to resources and prestige that are significant potential confounders in
analysis based simply on citation counts or velocity.

To analyse citation diversity we used the data system developed the Curtin Open Knowledge Initiative for analysis of
open knowledge performance. For the current analysis we used integrated data from Crossref, Microsoft Academic (MAG) and
the Research Organizations Register (ROR) to provide data on affiliations and location, field of research and
publication dates. We used Unpaywall data to define open access status.

For each of the 60 million publications in the dataset that had received at least one recorded citation we defined the
set of citing institutions, countries, regions and fields (using the MAG Level 0 fields). A single citing article may
represent citations from multiple sites (eg institutions) and each of these citation-sites is counted as contributing to
the diversity measures. For each of the 60 million articles we then calculate total citations, and the Shannon
Information Entropy and Gini ## Index as measures of diversity. Higher numbers are indicators of more diversity for both
measures.

We first replicate the observed association of open access with higher citations at this global scale, consistent with
previous literature but with the known caveats. Nonetheless we see that this association is robust across fields, years
of publication, and countries of publication (with some interesting exceptions) which offers avenues for further
analysis of the causal effects.

We show an enhanced diversity of citing institutions, countries and regions for open access research outputs (as defined
by the Unpaywall is_oa data element) with this effect being consistent for all publication years after 2010, across all
the fields examined here. There are differences over time, between fields and between author’s countries in the scale of
the effect, as well as the underlying diversity measures. These are interesting areas for future study. What is striking
is how consistent the observed effect is across all of these potential groupings (see supplementary data).

Significance measures are not easily applied, as we are not sampling. To evaluate confidence intervals we apply a
subsampling procedure. We also analyse the dependence of the effect on citation counts and show that the effect is
robust across the range of citation counts, with some limitations on the ability to analyse very low counts. ###CAN WE
SAY ANYTHING ABOUT WHAT THE EFFECT SIZE CORRESPONDS TO IN THE REAL WORLD###.

There are two interesting exceptions to the consistent behaviour of the effect. The first is that of the diversity of
citing fields by publication year, where the increased diversity for open access outputs only occurs after ##2010##. The
second is a similar pattern specifically for open access on publisher websites (sometimes referred to as “gold” and/or
“hybrid”). Whereas open access through repositories (“green”, which includes preprints in this analysis) is associated
with greater diversity of citations throughout the whole timeframe of analysis and with a larger overall effect of open
access, the “open access advantage” appears from 201##?? Onwards for open access provided via publisher websites.
Nonetheless for 2015 onwards the effect is consistent.

As an observational cohort study, our analysis is not able to define a causal link between open access and enhanced
diversity of citation sources. However, as a global analysis we can definitely say that within the full cohort in our
dataset of over 100 million outputs that open access outputs have a greater diversity of citation. To address the issue
of potentially confounding effects, particular that wealthier or more prestigious authors, institutions or countries
have greater ability to choose open access we note that citation diversity overall ###is frequently lower for wealthier
countries##SHOULD WE GRAPH THIS##? And institutions. The lack of overall correlation between citation counts and
citation diversity provides evidence that these differing measures track different aspects of usage and that there is
limited common confounding at the global scale.

The Budapest Open Access Initiative, now 20 years old, notes that open access makes possible “ the world-wide electronic
distribution of the peer-reviewed journal literature and completely free and unrestricted access to it by all
scientists, scholars, teachers, students, and other curious minds” providing a public good which will remove “accelerate
research, enrich education, share the learning of the rich with the poor and the poor with the rich, make this
literature as useful as it can be, and lay the foundation for uniting humanity in a common intellectual conversation and
quest for knowledge”.

Efforts to demonstrate the success of this endeavour remain as controversial as the choice of paths towards achieving
open access. The use of citations to capture use of research will always be limited. But data on other forms of usage
remain challenging and partial. By shifting attention from counting citations to assessing the diversity of citing
actors we have demonstrated that existing data can be repurposed to analyse different goals. In doing so we have
demonstrated that even for the narrow form of usage that citation from research outputs represents, open access outputs
are being used by a wider diversity of actors, whether we analyse those actors by institution, country, region or field.

More broadly diversity measures in general offer a new view over existing data providing potential insights that are not
offered by simple counts. As a potential insight into where the benefits of open access are being seen and a guide to
improving our policy implementation for wider access this offers many opportunities in addressing “…the task of removing
the barriers to open access and building a future in which research and education in every part of the world are that
much more free to flourish”.

# References


