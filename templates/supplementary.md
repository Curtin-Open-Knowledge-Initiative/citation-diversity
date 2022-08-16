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
The graphical outputs presented in this supplementary include only papers with two or more citations. Two 
different diversity measures are used to
represent the level of diversity in citing entities, i.e., the Gini-Simpson index and the Shannon index. Data from 2010
to 2019 (both inclusive) as publication years are presented. Diversity measures are calculated based on grouping 
all possible links between the cited paper and institutional affiliations of citing papers into bins as defined by the citing 
entities, i.e., Institutions, Countries, Subregions, Regions and Fields. We present various findings in terms of both 
means and medians, as both have their advantages and disadvantages in dealing with outliers, high number of repeat 
observations, etc.


<pdf:nextpage>
# Section A: Summary statistics for the overall data

The following figures present various summary statistics for our overall data. The top-left figure shows the 
overall number of paper (with DOIs) that are included in our study. These are grouped into their respective publication 
year as per Crossref metadata records. The top-right figure shows the yearly comparison between the amount of OA versus non-OA 
papers. There is a clear increase in the proportion of OA papers over the ten-year period. The bottom two figures 
depict the comparisons of mean and median, respectively, number of citations received by papers across different OA 
categories. There is a clear and consistent signal of OA papers receiving more citations when looking at the whole data 
set overall.
<img 
src={{ create_bar_doi_count_combined.files["bar_doi_count_combined.png"].cache_filepath }} width="300" /><img 
src={{ create_bar_doi_count_by_oa.files["bar_doi_count_by_oa.png"].cache_filepath }} width="300" />

<img 
src={{ create_bar_cit_count_by_oa.files["bar_cit_count_by_oa_mean.png"].cache_filepath }} width="300" /><img 
src={{ create_bar_cit_count_by_oa.files["bar_cit_count_by_oa_median.png"].cache_filepath }} width="300" />


<pdf:nextpage>
# Section B: Number of unique citing entities over publication years
The following figures track the mean and median numbers of unique citing entities over time and compares them across
different OA categories. For example, to calculate the number of unique citing countries for a particular paper, 
we count the number of (unique) countries for which its citing papers are affiliated to. The main point of interest 
here is that OA papers garners more unique citing entities almost consistently over time. Furthermore, papers that are 
Green OA garners the highest number of unique citing entities. We do note however that papers published Gold OA 
are also likely to be published Green OA. This means these papers potentially gets the benefits of both routes of OA. 
We also note that flat pattern for the median number of unique regions is the result of low number of possible regions, 
and a similar pattern is shown for the median number of citing fields due to most citations occurring within-field for 
a large portion of papers that have low citation counts.
{% for group in ["Institutions","Countries","Subregions","Fields", "Regions"] %}
{% set filename = "bar_uniq_cit_count_{}_mean.png" %} <img 
src={{ create_bar_uniq_cit_count.files[filename.format(group)].cache_filepath }} width="300" /> {% 
set filename = "bar_uniq_cit_count_{}_median.png" %} <img 
src={{ create_bar_uniq_cit_count.files[filename.format(group)].cache_filepath }} width="300" />
{% endfor %}


<pdf:nextpage>
# Section C: Boxplot of number of unique citing entities across OA groups
This section extends the comparison of unique citing entities to their respective distributions, as represented by box plots. 
To ensure robust comparisons, we sample 10,000 papers independently from each OA category as per citing entity grouping and 
year of publication. The quartiles of number of unique citing entities are shown together with potential outliers in each OA 
category. The general pattern observed is that OA papers attract higher number of unique citing entities, which is 
signalled both by the distributional differences and many more outliers in the upper tail. Again, it is noted that this 
general pattern can be diluted by the low number of regions in the regional comparisons. For the cases of institutional 
entities, the very high numbers of upper outliers skew the figures but the general pattern applies.

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
# Section D: Boxplot of number of unique citing entities across citation groups
In this section, we split the papers into groups depending on citation numbers and by OA/non-OA status. The sample of 
papers includes 2,000 OA papers and 2,000 non-OA papers from each citation group (i.e., 56,000 papers in total), 
as per citing entity group and publication 
year. The number of unique citing entities is counted for each paper and compared across citation groups. This is to check whether the 
OA advantage observed in the previous sections remain consistent across the levels of citation. As expected, the number 
of unique citing entities may increase with the number of citations. However, the OA advantage also seems to 
remain in place irrespective of the level of citation. Again, we note that the level of effect of the OA advantage can 
be less obvious when the total numbers of potential counts are low. The performance of OA papers appears to be at least 
as good, or better, than the non-OA papers.

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
# Section E: Citation diversity scores over publication years
In this section, we present the summary results of the diversity scores for papers in the various OA categories. Here, 
we include all papers in our study. In the following figures, mean and median diversity scores are tracked over ten years. This is plotted for 
various combinations of diversity measure and citing entity. Throughout the different measures across different 
citing entity grouping, we find OA papers to score higher in diversity. This is also consistently observed for all years 
included in the analysis. Green OA seems to lead in the diversity scores, which is also consistent with earlier 
comparisons on numbers of unique citing entities.

The first set of these is based on the Gini-Simpson index:
{% for group in ['Institutions','Countries','Subregions','Regions','Fields'] %}
{% set filename = 'bar_div_vs_year_GiniSim_{}_mean.png' %} <img 
src={{ create_bar_div_vs_year.files[filename.format(group)].cache_filepath }} width="300" /> {%
set filename1 = "bar_div_vs_year_GiniSim_{}_median.png" %} <img 
src={{ create_bar_div_vs_year.files[filename1.format(group)].cache_filepath }} width="300" />
{% endfor %}

The next set is based on the Shannon index:
{% for group in ["Institutions","Countries","Subregions","Regions", "Fields"] %}
{% set filename = "bar_div_vs_year_Shannon_{}_mean.png" %} <img 
src={{ create_bar_div_vs_year.files[filename.format(group)].cache_filepath }} width="300" /> {%
set filename = "bar_div_vs_year_Shannon_{}_median.png" %} <img 
src={{ create_bar_div_vs_year.files[filename.format(group)].cache_filepath }} width="300" />
{% endfor %}


<pdf:nextpage>
# Section F: Boxplot of citation diversity scores across OA groups
In the following figures, the distributions of diversity scores of papers (as per citing entity grouping) of different 
OA categories are compared. Random samples of 10,000 papers from each OA category is used in this comparison. The skewness 
towards the lower tails in the case of Gini-Simpson index scores is driven by 
the high number of papers that receives 
low number of citations (hence low diversity scores). In line with earlier findings, OA papers produce higher diversity 
scores. Again, it is interesting to note the raised distribution of Green OA compared to other categories. The non-OA 
category consistently have a longer lower tail in the Gini-Simpson scores, while Green OA papers often have the shortest 
lower tail. For the Shannon index, a parallel observation can be made with non-OA papers producing 
shorter upper tails. We note again the small number effect on some figures.

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
# Section G: Boxplot of citation diversity scores across citation groups
In these figures, papers are split into groups by citation counts. Similar to the earlier section on comparing citation groups, 
2,000 OA papers and 2,000 non-OA papers are sampled from each citation group. A diversity score is calculated based on 
citing entities for each paper and boxplot constructed for each OA category within each group. Each figure below represent 
the findings for each citing entity group and each publication year. Not unexpectedly the increase in citation count may 
correlate with slightly higher diversity scores for both diversity measures (i.e., higher likelihood of different sighting entities). The 
general pattern that OA papers scoring higher in diversity remains consistent through citation groups, citing entity groups, 
publication years, and across diversity measures.

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
# Section H: Citation diversity scores over citation counts
In the following figures, quartiles of diversity scores are tracked against citation counts for the complete data set. Instead 
of sampling papers by citation groups in the previous section, we include all papers in the study in the following analysis and 
all citation counts (not groups). This is plotted for various combinations of diversity measure, citing entity and publication year. 
Results with Fields as citing entity are excluded, as no meaningful results are produced due to very small numbers. 
The aim is to further explore potential relationships between diversity scores and citation counts. Interestingly, the mild 
positive relationship between diversity scores and citation counts observed in the lower end of the spectrum (which is consistent with 
the previous section) seems to fade away as we move towards papers with very high citations. Hence, in most cases, 
diversity scores are not completely driven by citation counts.

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
# Section I: OA citation advantage for subregions using average citation ratios
This section explores the OA citation advantage in terms of how much more citations OA papers garner, on average, 
over time. The average citation ratio (i.e., percentage ratio in average citation) is calculated as the average number 
of citations to OA papers, divided by the average number of citations to non-OA papers, and times by one hundred. For 
papers affiliated to a given subregion, this percentage is calculated for all inward citations from each subregion, for 
each of the ten-year period. A value above 100% indicates the set of OA papers attracts more citations than the corresponding 
set of non-OA papers, from a specific subregion in that year.

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Eastern Asia.png"].cache_filepath }} width="300" 
/> <img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Southern Asia.png"].cache_filepath }} width="300" 
/> 

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Western Asia.png"].cache_filepath }} width="300" 
/> <img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_South-eastern Asia.png"].cache_filepath }} width="300" 
/> 

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Central Asia.png"].cache_filepath }} width="300" 
/> <img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Southern Europe.png"].cache_filepath }} width="300" 
/> 

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Eastern Europe.png"].cache_filepath }} width="300" 
/> <img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Western Europe.png"].cache_filepath }} width="300" 
/> 

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Northern Europe.png"].cache_filepath }} width="300" 
/> <img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Latin America and the Caribbean.png"].cache_filepath }} width="300" 
/> 

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Northern America.png"].cache_filepath }} width="300" 
/> <img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Australia and New Zealand.png"].cache_filepath }} width="300" 
/> 

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Melanesia.png"].cache_filepath }} width="300" 
/> <img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Polynesia.png"].cache_filepath }} width="300" 
/> 

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Micronesia.png"].cache_filepath }} width="300" 
/> <img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Northern Africa.png"].cache_filepath }} width="300" 
/> 

<img 
src={{ create_line_compare_cit_subregions.files["line_compare_cit_count_subregions_for_Sub-Saharan Africa.png"].cache_filepath }} width="300" 
/> 


<pdf:nextpage>
# Section J: OA citation advantage for regions using average citation ratios
Continuing from the previous section, the corresponding results for regions are presented here. Similar to the previous section,
there appears to be something peculiar with papers affiliated to Asia and Asian subregions. This is potentially the result 
of several factors. First, our data's coverage of the Chinese language publications are relatively low as a result of 
using only Crossref DOIs. Secondly, Asia-affiliated papers in our data show a lower level of OA as compared to other regions.

<img 
src={{ create_line_compare_cit_regions.files["line_compare_cit_count_regions_for_Asia.png"].cache_filepath }} width="300" 
/><img 
src={{ create_line_compare_cit_regions.files["line_compare_cit_count_regions_for_Europe.png"].cache_filepath }} width="300" 
/>

<img 
src={{ create_line_compare_cit_regions.files["line_compare_cit_count_regions_for_Americas.png"].cache_filepath }} width="300" 
/><img 
src={{ create_line_compare_cit_regions.files["line_compare_cit_count_regions_for_Oceania.png"].cache_filepath }} width="300" 
/>

<img 
src={{ create_line_compare_cit_regions.files["line_compare_cit_count_regions_for_Africa.png"].cache_filepath }} width="300" 
/>


<pdf:nextpage>
# Section K: Percentage change in total citations to subregions
In this section we take an alternative look at where citations are coming from. Total citation numbers are used to 
calculate the percentage changes, i.e., total citations to OA papers minus total citations to non-OA papers, then divided 
by total citations to non-OA papers, and multiplied by one hundred. We note that the levels of OA 
are lower in earlier years as compared to more recent years and this has an effect on the total citation counts. As the level 
of OA becomes more comparable with the proportion of non-OA papers (more recent years), the effect of OA becomes far more 
clear. While the general trend is that most subregions benefits from received increased citations, there are subregions 
that benefits more than others, i.e., Northern America and Western Europe. However, there are also signals that some 
traditionally disadvantaged subregions benefiting greatly from OA, such as Sub-Saharan Africa.

For papers affiliated to Eastern Asia:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Eastern Asia_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Southern Asia:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Southern Asia_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Western Asia:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Western Asia_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to South-eastern Asia:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_South-eastern Asia_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Central Asia:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Central Asia_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Southern Europe:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Southern Europe_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Eastern Europe:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Eastern Europe_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Western Europe:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Western Europe_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Northern Europe:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Northern Europe_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Latin America and the Caribbean:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Latin America and the Caribbean_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Northern America:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Northern America_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Australia and New Zealand:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Australia and New Zealand_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Melanesia:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Melanesia_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Polynesia:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Polynesia_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Micronesia:

<img 
src={{ create_bar_compare_cit_subregions.files["bar_compare_cit_subregions_for_Micronesia_2010.png"].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files["bar_compare_cit_subregions_for_Micronesia_2013.png"].cache_filepath }} width="300" />

<img 
src={{ create_bar_compare_cit_subregions.files["bar_compare_cit_subregions_for_Micronesia_2017.png"].cache_filepath }} width="300" />

For papers affiliated to Northern Africa:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Northern Africa_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Sub-Saharan Africa:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_subregions_for_Sub-Saharan Africa_{}.png" %} <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_subregions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}


<pdf:nextpage>
# Section L: Percentage change in total citations to regions
Continuing from the previous section, we present parallel results for regions below.

For papers affiliated to Asia:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_regions_for_Asia_{}.png" %} <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Europe:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_regions_for_Europe_{}.png" %} <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Americas:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_regions_for_Americas_{}.png" %} <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Oceania:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_regions_for_Oceania_{}.png" %} <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

For papers affiliated to Africa:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "bar_compare_cit_regions_for_Africa_{}.png" %} <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_bar_compare_cit_regions.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}


<pdf:nextpage>
# Section M: Citation diversity scores across fields of study
This section explores the OA effect on citation diversity as per field of study. For each field of study (as defined by 
the MAG Level 0 fields), we track the mean and median Shannon and Gini-Simpson scores for the four OA categories, as 
per citing actor.

For Gini-Simpson scores on citing institutions:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Institutions_GiniSim_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Institutions_GiniSim_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Shannon scores on citing institutions:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Institutions_Shannon_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Institutions_Shannon_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Gini-Simpson scores on citing countries:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Countries_GiniSim_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Countries_GiniSim_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Shannon scores on citing countries:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Countries_Shannon_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Countries_Shannon_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Gini-Simpson scores on citing subregions:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Subregions_GiniSim_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Subregions_GiniSim_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Shannon scores on citing subregions:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Subregions_Shannon_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Subregions_Shannon_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Gini-Simpson scores on citing regions:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Regions_GiniSim_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Regions_GiniSim_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Shannon scores on citing regions:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Regions_Shannon_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Regions_Shannon_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Gini-Simpson scores on citing fields:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Fields_GiniSim_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Fields_GiniSim_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}

For Shannon scores on citing fields:
{% for field in ["Art", "Biology", "Business", "Chemistry", "Computer science", "Economics", "Engineering", 
"Environmental science", "Geography", "Geology", "History", "Materials science", "Mathematics", "Medicine", 
"Philosophy", "Physics", "Political science", "Psychology", "Sociology"] %}
{% set filename = "line_div_by_field_{}_Fields_Shannon_mean.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" /> {%
set filename = "line_div_by_field_{}_Fields_Shannon_median.png" %} <img 
src={{ create_line_div_by_field.files[filename.format(field)].cache_filepath }} width="300" />
{% endfor %}


<pdf:nextpage>
# Section N: Density estimation of citation diversity scores
We apply kernel density estimation to citation diversity scores for each year, citing actors, and diversity measure. 
These are paired with the corresponding histograms. Samples used contain 10,000 OA papers and 10,000 non-OA papers for
each publication year. These graphs provide overviews of the distributions of citation 
diversity scores. The clusters around zero, and around 0.5 for Gini-Simpson index and around 0.6 for Shannon index, 
are results of portions of low-citation papers. The most important signal from these graphs is the consistently better 
performance of the OA papers. This can be seen from the upward shifts of the distributions, decreases of proportions 
of papers with low scores (including the cluster around zero), and the heavier upper tails.

The first set of these is based on the Gini-Simpson index and institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_GiniSim_Institutions_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Gini-Simpson index and countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_GiniSim_Countries_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Gini-Simpson index and subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_GiniSim_Subregions_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Gini-Simpson index and regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_GiniSim_Regions_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Gini-Simpson index and fields as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_GiniSim_Fields_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Shannon index and institutions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_Shannon_Institutions_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Shannon index and countries as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_Shannon_Countries_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Shannon index and subregions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_Shannon_Subregions_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Shannon index and regions as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_Shannon_Regions_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}

The first set of these is based on the Shannon index and fields as citing entities:
{% for year in [2010,2012,2014,2016,2018] %}
{% set filename = "kde_dist_on_cit_div_Shannon_Fields_{}.png" %} <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year)].cache_filepath }} width="300" /> <img 
src={{ create_kde_dist_on_cit_div.files[filename.format(year+1)].cache_filepath }} width="300" />
{% endfor %}




