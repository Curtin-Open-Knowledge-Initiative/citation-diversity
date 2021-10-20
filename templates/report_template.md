{% import "report_macros.md" as helper with context %}
{% include "report_css.html" %}

<!-- Title Page -->
<pdf:nexttemplate name="titlepage">
<pdf:nextpage>

<p class="subtitle">TITLE</p>
<p class="titlemeta"><br>DATE: {{ helper.created_at()|upper }}</p>


<!-- switch page templates -->
<pdf:nexttemplate name="report">

<pdf:nextpage>

# Summary and Abstract

The open access movement aims to remove access barriers to research outputs. 
It is hypothesised that this helps maximise an article’s research impact as a 
result of lowering access restrictions caused by social inequality that 
favours wealthier populations. Citations are often interpreted as a measure 
of impact. Openly accessible articles are said to have increased citation 
counts as compared to their closed counterparts. Yet, quantitative studies 
have shown varied results across research cohorts. The current literature 
lacks simple yet strong evidence to support the positive impact of open 
access on citations. Here we show that open access outputs garner more 
diverse citationships across geographies and disciplines. We perform a 
large-scale study of citing patterns across paired-samples of open access 
outputs versus non-open access outputs using data integrated from multiple 
sources. We found that the open access groups are cited more widely across 
different countries, sub-regions, regions and fields of study. Importantly, 
there are increased citations from populations that traditionally have 
restricted access to closed publications. The results demonstrate a new 
perspective to understanding the citation impact of open access practices. 
It provides a remarkably simple argument in support of open access 
publishing, i.e., it gets cited by more authors from more places.

# Exciting things like data and table

