/*
## Summary
Generates yearly summary diversity scores for each field of study

## Description
Creates a table that lists, for each field and each publication year, the median and mean:
- numbers of unique citing groups;
- GiniSim scores by citing groups;
- Shannon scores by citing groups;
as per OA category.

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://coki-scratch-space.citation_diversity_analysis.citation_diversity_global

## Creates
file cit_div_by_field.csv

*/

WITH
  data_noa AS (
    SELECT
      field,
      year,
      ANY_VALUE(CitingInstitutions_count_uniq_perc50) AS noa_CitingInstitutions_count_uniq_median,
      AVG(CitingInstitutions_count_uniq) AS noa_CitingInstitutions_count_uniq_mean,
      ANY_VALUE(CitingInstitutions_GiniSim_perc50)AS noa_CitingInstitutions_GiniSim_median,
      AVG(CitingInstitutions_GiniSim) AS noa_CitingInstitutions_GiniSim_mean,
      ANY_VALUE(CitingInstitutions_Shannon_perc50) AS noa_CitingInstitutions_Shannon_median,
      AVG(CitingInstitutions_Shannon) AS noa_CitingInstitutions_Shannon_mean,
      ANY_VALUE(CitingCountries_count_uniq_perc50) AS noa_CitingCountries_count_uniq_median,
      AVG(CitingCountries_count_uniq) AS noa_CitingCountries_count_uniq_mean,
      ANY_VALUE(CitingCountries_GiniSim_perc50)AS noa_CitingCountries_GiniSim_median,
      AVG(CitingCountries_GiniSim) AS noa_CitingCountries_GiniSim_mean,
      ANY_VALUE(CitingCountries_Shannon_perc50) AS noa_CitingCountries_Shannon_median,
      AVG(CitingCountries_Shannon) AS noa_CitingCountries_Shannon_mean,
      ANY_VALUE(CitingSubregions_count_uniq_perc50) AS noa_CitingSubregions_count_uniq_median,
      AVG(CitingSubregions_count_uniq) AS noa_CitingSubregions_count_uniq_mean,
      ANY_VALUE(CitingSubregions_GiniSim_perc50)AS noa_CitingSubregions_GiniSim_median,
      AVG(CitingSubregions_GiniSim) AS noa_CitingSubregions_GiniSim_mean,
      ANY_VALUE(CitingSubregions_Shannon_perc50) AS noa_CitingSubregions_Shannon_median,
      AVG(CitingSubregions_Shannon) AS noa_CitingSubregions_Shannon_mean,
      ANY_VALUE(CitingRegions_count_uniq_perc50) AS noa_CitingRegions_count_uniq_median,
      AVG(CitingRegions_count_uniq) AS noa_CitingRegions_count_uniq_mean,
      ANY_VALUE(CitingRegions_GiniSim_perc50)AS noa_CitingRegions_GiniSim_median,
      AVG(CitingRegions_GiniSim) AS noa_CitingRegions_GiniSim_mean,
      ANY_VALUE(CitingRegions_Shannon_perc50) AS noa_CitingRegions_Shannon_median,
      AVG(CitingRegions_Shannon) AS noa_CitingRegions_Shannon_mean,
      ANY_VALUE(CitingFields_count_uniq_perc50) AS noa_CitingFields_count_uniq_median,
      AVG(CitingFields_count_uniq) AS noa_CitingFields_count_uniq_mean,
      ANY_VALUE(CitingFields_GiniSim_perc50)AS noa_CitingFields_GiniSim_median,
      AVG(CitingFields_GiniSim) AS noa_CitingFields_GiniSim_mean,
      ANY_VALUE(CitingFields_Shannon_perc50) AS noa_CitingFields_Shannon_median,
      AVG(CitingFields_Shannon) AS noa_CitingFields_Shannon_mean
    FROM (
      SELECT
        doi,
        year,
        temp_field.DisplayName as field,
        CitingInstitutions_count_uniq,
        CitingInstitutions_GiniSim,
        CitingInstitutions_Shannon,
        CitingCountries_count_uniq,
        CitingCountries_GiniSim,
        CitingCountries_Shannon,
        CitingSubregions_count_uniq,
        CitingSubregions_GiniSim,
        CitingSubregions_Shannon,
        CitingRegions_count_uniq,
        CitingRegions_GiniSim,
        CitingRegions_Shannon,
        CitingFields_count_uniq,
        CitingFields_GiniSim,
        CitingFields_Shannon,
        PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_count_uniq_perc50,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_GiniSim_perc50,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_Shannon_perc50,
        PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_count_uniq_perc50,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_GiniSim_perc50,
        PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_Shannon_perc50,
        PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_count_uniq_perc50,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_GiniSim_perc50,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_Shannon_perc50,
        PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_count_uniq_perc50,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_GiniSim_perc50,
        PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_Shannon_perc50,
        PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_count_uniq_perc50,
        PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_GiniSim_perc50,
        PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_Shannon_perc50
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount >= 2) AND (is_oa IS false)),
        UNNEST(fields) AS temp_field
    )
    GROUP BY field, year
  ),
  data_oa AS (
    SELECT
      field,
      year,
      ANY_VALUE(CitingInstitutions_count_uniq_perc50) AS oa_CitingInstitutions_count_uniq_median,
      AVG(CitingInstitutions_count_uniq) AS oa_CitingInstitutions_count_uniq_mean,
      ANY_VALUE(CitingInstitutions_GiniSim_perc50)AS oa_CitingInstitutions_GiniSim_median,
      AVG(CitingInstitutions_GiniSim) AS oa_CitingInstitutions_GiniSim_mean,
      ANY_VALUE(CitingInstitutions_Shannon_perc50) AS oa_CitingInstitutions_Shannon_median,
      AVG(CitingInstitutions_Shannon) AS oa_CitingInstitutions_Shannon_mean,
      ANY_VALUE(CitingCountries_count_uniq_perc50) AS oa_CitingCountries_count_uniq_median,
      AVG(CitingCountries_count_uniq) AS oa_CitingCountries_count_uniq_mean,
      ANY_VALUE(CitingCountries_GiniSim_perc50)AS oa_CitingCountries_GiniSim_median,
      AVG(CitingCountries_GiniSim) AS oa_CitingCountries_GiniSim_mean,
      ANY_VALUE(CitingCountries_Shannon_perc50) AS oa_CitingCountries_Shannon_median,
      AVG(CitingCountries_Shannon) AS oa_CitingCountries_Shannon_mean,
      ANY_VALUE(CitingSubregions_count_uniq_perc50) AS oa_CitingSubregions_count_uniq_median,
      AVG(CitingSubregions_count_uniq) AS oa_CitingSubregions_count_uniq_mean,
      ANY_VALUE(CitingSubregions_GiniSim_perc50)AS oa_CitingSubregions_GiniSim_median,
      AVG(CitingSubregions_GiniSim) AS oa_CitingSubregions_GiniSim_mean,
      ANY_VALUE(CitingSubregions_Shannon_perc50) AS oa_CitingSubregions_Shannon_median,
      AVG(CitingSubregions_Shannon) AS oa_CitingSubregions_Shannon_mean,
      ANY_VALUE(CitingRegions_count_uniq_perc50) AS oa_CitingRegions_count_uniq_median,
      AVG(CitingRegions_count_uniq) AS oa_CitingRegions_count_uniq_mean,
      ANY_VALUE(CitingRegions_GiniSim_perc50)AS oa_CitingRegions_GiniSim_median,
      AVG(CitingRegions_GiniSim) AS oa_CitingRegions_GiniSim_mean,
      ANY_VALUE(CitingRegions_Shannon_perc50) AS oa_CitingRegions_Shannon_median,
      AVG(CitingRegions_Shannon) AS oa_CitingRegions_Shannon_mean,
      ANY_VALUE(CitingFields_count_uniq_perc50) AS oa_CitingFields_count_uniq_median,
      AVG(CitingFields_count_uniq) AS oa_CitingFields_count_uniq_mean,
      ANY_VALUE(CitingFields_GiniSim_perc50)AS oa_CitingFields_GiniSim_median,
      AVG(CitingFields_GiniSim) AS oa_CitingFields_GiniSim_mean,
      ANY_VALUE(CitingFields_Shannon_perc50) AS oa_CitingFields_Shannon_median,
      AVG(CitingFields_Shannon) AS oa_CitingFields_Shannon_mean
    FROM (
      SELECT
        doi,
        year,
        temp_field.DisplayName as field,
        CitingInstitutions_count_uniq,
        CitingInstitutions_GiniSim,
        CitingInstitutions_Shannon,
        CitingCountries_count_uniq,
        CitingCountries_GiniSim,
        CitingCountries_Shannon,
        CitingSubregions_count_uniq,
        CitingSubregions_GiniSim,
        CitingSubregions_Shannon,
        CitingRegions_count_uniq,
        CitingRegions_GiniSim,
        CitingRegions_Shannon,
        CitingFields_count_uniq,
        CitingFields_GiniSim,
        CitingFields_Shannon,
        PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_count_uniq_perc50,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_GiniSim_perc50,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_Shannon_perc50,
        PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_count_uniq_perc50,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_GiniSim_perc50,
        PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_Shannon_perc50,
        PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_count_uniq_perc50,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_GiniSim_perc50,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_Shannon_perc50,
        PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_count_uniq_perc50,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_GiniSim_perc50,
        PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_Shannon_perc50,
        PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_count_uniq_perc50,
        PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_GiniSim_perc50,
        PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_Shannon_perc50
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount >= 2) AND (is_oa IS true)),
        UNNEST(fields) AS temp_field
    )
    GROUP BY field, year
  ),
  data_gold AS (
    SELECT
      field,
      year,
      ANY_VALUE(CitingInstitutions_count_uniq_perc50) AS gold_CitingInstitutions_count_uniq_median,
      AVG(CitingInstitutions_count_uniq) AS gold_CitingInstitutions_count_uniq_mean,
      ANY_VALUE(CitingInstitutions_GiniSim_perc50)AS gold_CitingInstitutions_GiniSim_median,
      AVG(CitingInstitutions_GiniSim) AS gold_CitingInstitutions_GiniSim_mean,
      ANY_VALUE(CitingInstitutions_Shannon_perc50) AS gold_CitingInstitutions_Shannon_median,
      AVG(CitingInstitutions_Shannon) AS gold_CitingInstitutions_Shannon_mean,
      ANY_VALUE(CitingCountries_count_uniq_perc50) AS gold_CitingCountries_count_uniq_median,
      AVG(CitingCountries_count_uniq) AS gold_CitingCountries_count_uniq_mean,
      ANY_VALUE(CitingCountries_GiniSim_perc50)AS gold_CitingCountries_GiniSim_median,
      AVG(CitingCountries_GiniSim) AS gold_CitingCountries_GiniSim_mean,
      ANY_VALUE(CitingCountries_Shannon_perc50) AS gold_CitingCountries_Shannon_median,
      AVG(CitingCountries_Shannon) AS gold_CitingCountries_Shannon_mean,
      ANY_VALUE(CitingSubregions_count_uniq_perc50) AS gold_CitingSubregions_count_uniq_median,
      AVG(CitingSubregions_count_uniq) AS gold_CitingSubregions_count_uniq_mean,
      ANY_VALUE(CitingSubregions_GiniSim_perc50)AS gold_CitingSubregions_GiniSim_median,
      AVG(CitingSubregions_GiniSim) AS gold_CitingSubregions_GiniSim_mean,
      ANY_VALUE(CitingSubregions_Shannon_perc50) AS gold_CitingSubregions_Shannon_median,
      AVG(CitingSubregions_Shannon) AS gold_CitingSubregions_Shannon_mean,
      ANY_VALUE(CitingRegions_count_uniq_perc50) AS gold_CitingRegions_count_uniq_median,
      AVG(CitingRegions_count_uniq) AS gold_CitingRegions_count_uniq_mean,
      ANY_VALUE(CitingRegions_GiniSim_perc50)AS gold_CitingRegions_GiniSim_median,
      AVG(CitingRegions_GiniSim) AS gold_CitingRegions_GiniSim_mean,
      ANY_VALUE(CitingRegions_Shannon_perc50) AS gold_CitingRegions_Shannon_median,
      AVG(CitingRegions_Shannon) AS gold_CitingRegions_Shannon_mean,
      ANY_VALUE(CitingFields_count_uniq_perc50) AS gold_CitingFields_count_uniq_median,
      AVG(CitingFields_count_uniq) AS gold_CitingFields_count_uniq_mean,
      ANY_VALUE(CitingFields_GiniSim_perc50)AS gold_CitingFields_GiniSim_median,
      AVG(CitingFields_GiniSim) AS gold_CitingFields_GiniSim_mean,
      ANY_VALUE(CitingFields_Shannon_perc50) AS gold_CitingFields_Shannon_median,
      AVG(CitingFields_Shannon) AS gold_CitingFields_Shannon_mean
    FROM (
      SELECT
        doi,
        year,
        temp_field.DisplayName as field,
        CitingInstitutions_count_uniq,
        CitingInstitutions_GiniSim,
        CitingInstitutions_Shannon,
        CitingCountries_count_uniq,
        CitingCountries_GiniSim,
        CitingCountries_Shannon,
        CitingSubregions_count_uniq,
        CitingSubregions_GiniSim,
        CitingSubregions_Shannon,
        CitingRegions_count_uniq,
        CitingRegions_GiniSim,
        CitingRegions_Shannon,
        CitingFields_count_uniq,
        CitingFields_GiniSim,
        CitingFields_Shannon,
        PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_count_uniq_perc50,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_GiniSim_perc50,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_Shannon_perc50,
        PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_count_uniq_perc50,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_GiniSim_perc50,
        PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_Shannon_perc50,
        PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_count_uniq_perc50,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_GiniSim_perc50,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_Shannon_perc50,
        PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_count_uniq_perc50,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_GiniSim_perc50,
        PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_Shannon_perc50,
        PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_count_uniq_perc50,
        PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_GiniSim_perc50,
        PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_Shannon_perc50
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount >= 2) AND (gold IS true)),
        UNNEST(fields) AS temp_field
    )
    GROUP BY field, year
  ),
  data_green AS (
    SELECT
      field,
      year,
      ANY_VALUE(CitingInstitutions_count_uniq_perc50) AS green_CitingInstitutions_count_uniq_median,
      AVG(CitingInstitutions_count_uniq) AS green_CitingInstitutions_count_uniq_mean,
      ANY_VALUE(CitingInstitutions_GiniSim_perc50)AS green_CitingInstitutions_GiniSim_median,
      AVG(CitingInstitutions_GiniSim) AS green_CitingInstitutions_GiniSim_mean,
      ANY_VALUE(CitingInstitutions_Shannon_perc50) AS green_CitingInstitutions_Shannon_median,
      AVG(CitingInstitutions_Shannon) AS green_CitingInstitutions_Shannon_mean,
      ANY_VALUE(CitingCountries_count_uniq_perc50) AS green_CitingCountries_count_uniq_median,
      AVG(CitingCountries_count_uniq) AS green_CitingCountries_count_uniq_mean,
      ANY_VALUE(CitingCountries_GiniSim_perc50)AS green_CitingCountries_GiniSim_median,
      AVG(CitingCountries_GiniSim) AS green_CitingCountries_GiniSim_mean,
      ANY_VALUE(CitingCountries_Shannon_perc50) AS green_CitingCountries_Shannon_median,
      AVG(CitingCountries_Shannon) AS green_CitingCountries_Shannon_mean,
      ANY_VALUE(CitingSubregions_count_uniq_perc50) AS green_CitingSubregions_count_uniq_median,
      AVG(CitingSubregions_count_uniq) AS green_CitingSubregions_count_uniq_mean,
      ANY_VALUE(CitingSubregions_GiniSim_perc50)AS green_CitingSubregions_GiniSim_median,
      AVG(CitingSubregions_GiniSim) AS green_CitingSubregions_GiniSim_mean,
      ANY_VALUE(CitingSubregions_Shannon_perc50) AS green_CitingSubregions_Shannon_median,
      AVG(CitingSubregions_Shannon) AS green_CitingSubregions_Shannon_mean,
      ANY_VALUE(CitingRegions_count_uniq_perc50) AS green_CitingRegions_count_uniq_median,
      AVG(CitingRegions_count_uniq) AS green_CitingRegions_count_uniq_mean,
      ANY_VALUE(CitingRegions_GiniSim_perc50)AS green_CitingRegions_GiniSim_median,
      AVG(CitingRegions_GiniSim) AS green_CitingRegions_GiniSim_mean,
      ANY_VALUE(CitingRegions_Shannon_perc50) AS green_CitingRegions_Shannon_median,
      AVG(CitingRegions_Shannon) AS green_CitingRegions_Shannon_mean,
      ANY_VALUE(CitingFields_count_uniq_perc50) AS green_CitingFields_count_uniq_median,
      AVG(CitingFields_count_uniq) AS green_CitingFields_count_uniq_mean,
      ANY_VALUE(CitingFields_GiniSim_perc50)AS green_CitingFields_GiniSim_median,
      AVG(CitingFields_GiniSim) AS green_CitingFields_GiniSim_mean,
      ANY_VALUE(CitingFields_Shannon_perc50) AS green_CitingFields_Shannon_median,
      AVG(CitingFields_Shannon) AS green_CitingFields_Shannon_mean
    FROM (
      SELECT
        doi,
        year,
        temp_field.DisplayName as field,
        CitingInstitutions_count_uniq,
        CitingInstitutions_GiniSim,
        CitingInstitutions_Shannon,
        CitingCountries_count_uniq,
        CitingCountries_GiniSim,
        CitingCountries_Shannon,
        CitingSubregions_count_uniq,
        CitingSubregions_GiniSim,
        CitingSubregions_Shannon,
        CitingRegions_count_uniq,
        CitingRegions_GiniSim,
        CitingRegions_Shannon,
        CitingFields_count_uniq,
        CitingFields_GiniSim,
        CitingFields_Shannon,
        PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_count_uniq_perc50,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_GiniSim_perc50,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingInstitutions_Shannon_perc50,
        PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_count_uniq_perc50,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_GiniSim_perc50,
        PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingCountries_Shannon_perc50,
        PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_count_uniq_perc50,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_GiniSim_perc50,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingSubregions_Shannon_perc50,
        PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_count_uniq_perc50,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_GiniSim_perc50,
        PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingRegions_Shannon_perc50,
        PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_count_uniq_perc50,
        PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_GiniSim_perc50,
        PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY temp_field.DisplayName, year) AS CitingFields_Shannon_perc50
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount >= 2) AND (green IS true)),
        UNNEST(fields) AS temp_field
    )
    GROUP BY field, year
  )
SELECT
  *
FROM data_noa
  INNER JOIN data_oa USING(field, year)
  INNER JOIN data_gold USING(field, year)
  INNER JOIN data_green USING(field, year)
ORDER BY
  field, year