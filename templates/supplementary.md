{% import "report_macros.md" as helper with context %}
{% include "report_css.html" %}

<!-- Title Page -->
<pdf:nexttemplate name="titlepage">
<p class="subtitle">SUPPLEMENTARY FIGURES</p>
<p class="titlemeta"><br>DATE: {{ helper.created_at()|upper }}</p>


<!-- switch page templates -->
<pdf:nexttemplate name="report">

<pdf:nextpage>
# Data and variables
The graphical outputs presented in this supplementary include only papers with two or more citations. Citing entities 
(author affiliations on citing papers) are grouped by Institutions, Countries, Subregions, Regions and Fields. Two 
different diversity measures are used to
represent the level of diversity in citing entities, i.e., the Gini-Simpson index and the Shannon index. Data from 2010
to 2019 (both inclusive) as publication years are presented.


<pdf:nextpage>
# Section A: Comparing diversity index scores across citation groups
In these figures, papers are split into groups by citation counts. Within each citation group, papers are further 
divided into OA and non-OA papers. A diversity measure is calculated based on citing entities for each paper and 
boxplot constructed for each group.

The first set of these is based on the Gini-Simpson index and institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_GiniSim_Institutions_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_GiniSim_Countries_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and Subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_GiniSim_Subregions_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and Regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_GiniSim_Regions_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and Fields as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_GiniSim_Fields_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}


The next set is based on the Shannon index and institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_Shannon_Institutions_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_Shannon_Countries_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and Subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_Shannon_Subregions_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and Regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_Shannon_Regions_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and Fields as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_cit_group_Shannon_Fields_{}.png" %} <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}


<pdf:nextpage>
# Section B: Comparing diversity index scores across OA groupings
In the following figures, the levels of diversity in papers (as per citing entity) of different OA groups are compared.

The first set of these is based on the Gini-Simpson index and institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_GiniSim_Institutions_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_GiniSim_Countries_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and Subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_GiniSim_Subregions_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and Regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_GiniSim_Regions_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and Fields as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_GiniSim_Fields_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}


The next set is based on the Shannon index and institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_Shannon_Institutions_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_Shannon_Countries_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and Subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_Shannon_Subregions_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and Regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_Shannon_Regions_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and Fields as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_div_by_oa_group_Shannon_Fields_{}.png" %} <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_div_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}



<pdf:nextpage>
# Section C: Comparing number of unique citing entities across citation groups
The number of unique citing entities is counted for each paper and compared across citation groups.

The first set of these is based on Institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_cit_group_Institutions_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on Countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_cit_group_Countries_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on Subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_cit_group_Subregions_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on Regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_cit_group_Regions_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Fields as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_cit_group_Fields_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_cit_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}




<pdf:nextpage>
# Section D: Comparing number of unique citing entities across OA groups
The number of unique citing entities is counted for each paper and compared across OA groups.

The first set of these is based on Institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_oa_group_Institutions_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on Countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_oa_group_Countries_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on Subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_oa_group_Subregions_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on Regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_oa_group_Regions_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Fields as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "box_uniq_cit_by_oa_group_Fields_{}.png" %} <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_boxplot_uniq_cit_by_oa_group.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}



<pdf:nextpage>
# Section E: Tracking diversity scores against citation counts

In the following figures, quartiles of diversity scores are tracked against citation counts. This is plotted for 
various combinations of diversity measure, citing entity and publication year. Results with Fields as citing entity are 
excluded, as no meaningful results are produced due to very small numbers.

The first set of these is based on the Gini-Simpson index and institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "line_div_vs_cit_count_GiniSim_Institutions_{}.png" %} <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "line_div_vs_cit_count_GiniSim_Countries_{}.png" %} <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and Subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "line_div_vs_cit_count_GiniSim_Subregions_{}.png" %} <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Gini-Simpson index and Regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "line_div_vs_cit_count_GiniSim_Regions_{}.png" %} <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "line_div_vs_cit_count_Shannon_Institutions_{}.png" %} <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "line_div_vs_cit_count_Shannon_Countries_{}.png" %} <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and Subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "line_div_vs_cit_count_Shannon_Subregions_{}.png" %} <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index and Regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "line_div_vs_cit_count_Shannon_Regions_{}.png" %} <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_line_div_vs_cit_count.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}



<pdf:nextpage>
# Section F: Tracking mean and median diversity scores over publication years

In the following figures, mean and median diversity scores are tracked over ten years. This is plotted for 
various combinations of diversity measure and citing entity.

The first set of these is based on the Gini-Simpson index:
{% for group in ['Institutions','Countries','Subregions','Regions','Fields'] %}
{% set filename = "bar_div_vs_year_GiniSim_{}_mean.png" %} <img 
src={{ create_bar_div_vs_year.files[filename.format(group)].cache_filepath }} width="300" /> {%
set filename = "bar_div_vs_year_GiniSim_{}_median.png" %} <img 
src={{ create_bar_div_vs_year.files[filename.format(group)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index:
{% for group in ['Institutions','Countries','Subregions','Regions','Fields'] %}
{% set filename = "bar_div_vs_year_Shannon_{}_mean.png" %} <img 
src={{ create_bar_div_vs_year.files[filename.format(group)].cache_filepath }} width="300" /> {%
set filename = "bar_div_vs_year_Shannon_{}_median.png" %} <img 
src={{ create_bar_div_vs_year.files[filename.format(group)].cache_filepath }} width="300" />
{% endfor %}


<pdf:nextpage>
# Section G: Overall DOI and citation counts

The following figures present various summary statistics related to our data.
<img 
src={{ create_bar_doi_count_combined.files['bar_doi_count_combined.png'].cache_filepath }} width="300" /><img 
src={{ create_bar_doi_count_by_oa.files['bar_doi_count_by_oa.png'].cache_filepath }} width="300" />

<img 
src={{ create_bar_cit_count_by_oa.files['bar_cit_count_by_oa_mean.png'].cache_filepath }} width="300" /><img 
src={{ create_bar_cit_count_by_oa.files['bar_cit_count_by_oa_median.png'].cache_filepath }} width="300" />


<pdf:nextpage>
# Section H: Counting unique citing entities

The following figures track the mean and median numbers of citing entities over time and compares them across
different OA groups.
{% for group in ['Institutions','Countries','Subregions','Regions','Fields'] %}
{% set filename = "bar_uniq_cit_count_{}_mean.png" %} <img 
src={{ create_bar_uniq_cit_count.files[filename.format(group)].cache_filepath }} width="300" /> {%
set filename = "bar_uniq_cit_count_{}_median.png" %} <img 
src={{ create_bar_uniq_cit_count.files[filename.format(group)].cache_filepath }} width="300" />
{% endfor %}

