/*
## Summary
Generates annually the quartile diversity scores as per citation count

## Description
Creates a table that lists, for each publication year and each citation count, the quartiles in:
- GiniSim scores by citing groups;
- Shannon scores by citing groups.

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://{citation_diversity_table}

## Creates
file cit_div_vs_cit_count.csv

*/

WITH
  data_perc AS (
      SELECT
        year,
        CitationCount,

        PERCENTILE_CONT(CitingInstitutions_GiniSim,0) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_GiniSim_perc0,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.25) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_GiniSim_perc25,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_GiniSim_perc50,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.75) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_GiniSim_perc75,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,1) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_GiniSim_perc100,

        PERCENTILE_CONT(CitingCountries_GiniSim,0) OVER(PARTITION BY CitationCount, year) AS CitingCountries_GiniSim_perc0,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.25) OVER(PARTITION BY CitationCount, year) AS CitingCountries_GiniSim_perc25,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY CitationCount, year) AS CitingCountries_GiniSim_perc50,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.75) OVER(PARTITION BY CitationCount, year) AS CitingCountries_GiniSim_perc75,
        PERCENTILE_CONT(CitingCountries_GiniSim,1) OVER(PARTITION BY CitationCount, year) AS CitingCountries_GiniSim_perc100,

        PERCENTILE_CONT(CitingSubregions_GiniSim,0) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_GiniSim_perc0,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.25) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_GiniSim_perc25,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_GiniSim_perc50,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.75) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_GiniSim_perc75,
        PERCENTILE_CONT(CitingSubregions_GiniSim,1) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_GiniSim_perc100,

        PERCENTILE_CONT(CitingRegions_GiniSim,0) OVER(PARTITION BY CitationCount, year) AS CitingRegions_GiniSim_perc0,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.25) OVER(PARTITION BY CitationCount, year) AS CitingRegions_GiniSim_perc25,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY CitationCount, year) AS CitingRegions_GiniSim_perc50,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.75) OVER(PARTITION BY CitationCount, year) AS CitingRegions_GiniSim_perc75,
        PERCENTILE_CONT(CitingRegions_GiniSim,1) OVER(PARTITION BY CitationCount, year) AS CitingRegions_GiniSim_perc100,

        PERCENTILE_CONT(CitingInstitutions_Shannon,0) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_Shannon_perc0,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.25) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_Shannon_perc25,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_Shannon_perc50,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.75) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_Shannon_perc75,
        PERCENTILE_CONT(CitingInstitutions_Shannon,1) OVER(PARTITION BY CitationCount, year) AS CitingInstitutions_Shannon_perc100,

        PERCENTILE_CONT(CitingCountries_Shannon,0) OVER(PARTITION BY CitationCount, year) AS CitingCountries_Shannon_perc0,
        PERCENTILE_CONT(CitingCountries_Shannon,0.25) OVER(PARTITION BY CitationCount, year) AS CitingCountries_Shannon_perc25,
        PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY CitationCount, year) AS CitingCountries_Shannon_perc50,
        PERCENTILE_CONT(CitingCountries_Shannon,0.75) OVER(PARTITION BY CitationCount, year) AS CitingCountries_Shannon_perc75,
        PERCENTILE_CONT(CitingCountries_Shannon,1) OVER(PARTITION BY CitationCount, year) AS CitingCountries_Shannon_perc100,

        PERCENTILE_CONT(CitingSubregions_Shannon,0) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_Shannon_perc0,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.25) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_Shannon_perc25,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_Shannon_perc50,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.75) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_Shannon_perc75,
        PERCENTILE_CONT(CitingSubregions_Shannon,1) OVER(PARTITION BY CitationCount, year) AS CitingSubregions_Shannon_perc100,

        PERCENTILE_CONT(CitingRegions_Shannon,0) OVER(PARTITION BY CitationCount, year) AS CitingRegions_Shannon_perc0,
        PERCENTILE_CONT(CitingRegions_Shannon,0.25) OVER(PARTITION BY CitationCount, year) AS CitingRegions_Shannon_perc25,
        PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY CitationCount, year) AS CitingRegions_Shannon_perc50,
        PERCENTILE_CONT(CitingRegions_Shannon,0.75) OVER(PARTITION BY CitationCount, year) AS CitingRegions_Shannon_perc75,
        PERCENTILE_CONT(CitingRegions_Shannon,1) OVER(PARTITION BY CitationCount, year) AS CitingRegions_Shannon_perc100
      FROM
        `{citation_diversity_table}`
      WHERE
        (CitationCount >= 2) AND (is_oa IS NOT NULL)
  )
SELECT
  year,
  CitationCount,

  ANY_VALUE(CitingInstitutions_GiniSim_perc0) AS CitingInstitutions_GiniSim_perc0,
  ANY_VALUE(CitingInstitutions_GiniSim_perc25) AS CitingInstitutions_GiniSim_perc25,
  ANY_VALUE(CitingInstitutions_GiniSim_perc50) AS CitingInstitutions_GiniSim_perc50,
  ANY_VALUE(CitingInstitutions_GiniSim_perc75) AS CitingInstitutions_GiniSim_perc75,
  ANY_VALUE(CitingInstitutions_GiniSim_perc100) AS CitingInstitutions_GiniSim_perc100,

  ANY_VALUE(CitingCountries_GiniSim_perc0) AS CitingCountries_GiniSim_perc0,
  ANY_VALUE(CitingCountries_GiniSim_perc25) AS CitingCountries_GiniSim_perc25,
  ANY_VALUE(CitingCountries_GiniSim_perc50) AS CitingCountries_GiniSim_perc50,
  ANY_VALUE(CitingCountries_GiniSim_perc75) AS CitingCountries_GiniSim_perc75,
  ANY_VALUE(CitingCountries_GiniSim_perc100) AS CitingCountries_GiniSim_perc100,

  ANY_VALUE(CitingSubregions_GiniSim_perc0) AS CitingSubregions_GiniSim_perc0,
  ANY_VALUE(CitingSubregions_GiniSim_perc25) AS CitingSubregions_GiniSim_perc25,
  ANY_VALUE(CitingSubregions_GiniSim_perc50) AS CitingSubregions_GiniSim_perc50,
  ANY_VALUE(CitingSubregions_GiniSim_perc75) AS CitingSubregions_GiniSim_perc75,
  ANY_VALUE(CitingSubregions_GiniSim_perc100) AS CitingSubregions_GiniSim_perc100,

  ANY_VALUE(CitingRegions_GiniSim_perc0) AS CitingRegions_GiniSim_perc0,
  ANY_VALUE(CitingRegions_GiniSim_perc25) AS CitingRegions_GiniSim_perc25,
  ANY_VALUE(CitingRegions_GiniSim_perc50) AS CitingRegions_GiniSim_perc50,
  ANY_VALUE(CitingRegions_GiniSim_perc75) AS CitingRegions_GiniSim_perc75,
  ANY_VALUE(CitingRegions_GiniSim_perc100) AS CitingRegions_GiniSim_perc100,

  ANY_VALUE(CitingInstitutions_Shannon_perc0) AS CitingInstitutions_Shannon_perc0,
  ANY_VALUE(CitingInstitutions_Shannon_perc25) AS CitingInstitutions_Shannon_perc25,
  ANY_VALUE(CitingInstitutions_Shannon_perc50) AS CitingInstitutions_Shannon_perc50,
  ANY_VALUE(CitingInstitutions_Shannon_perc75) AS CitingInstitutions_Shannon_perc75,
  ANY_VALUE(CitingInstitutions_Shannon_perc100) AS CitingInstitutions_Shannon_perc100,

  ANY_VALUE(CitingCountries_Shannon_perc0) AS CitingCountries_Shannon_perc0,
  ANY_VALUE(CitingCountries_Shannon_perc25) AS CitingCountries_Shannon_perc25,
  ANY_VALUE(CitingCountries_Shannon_perc50) AS CitingCountries_Shannon_perc50,
  ANY_VALUE(CitingCountries_Shannon_perc75) AS CitingCountries_Shannon_perc75,
  ANY_VALUE(CitingCountries_Shannon_perc100) AS CitingCountries_Shannon_perc100,

  ANY_VALUE(CitingSubregions_Shannon_perc0) AS CitingSubregions_Shannon_perc0,
  ANY_VALUE(CitingSubregions_Shannon_perc25) AS CitingSubregions_Shannon_perc25,
  ANY_VALUE(CitingSubregions_Shannon_perc50) AS CitingSubregions_Shannon_perc50,
  ANY_VALUE(CitingSubregions_Shannon_perc75) AS CitingSubregions_Shannon_perc75,
  ANY_VALUE(CitingSubregions_Shannon_perc100) AS CitingSubregions_Shannon_perc100,

  ANY_VALUE(CitingRegions_Shannon_perc0) AS CitingRegions_Shannon_perc0,
  ANY_VALUE(CitingRegions_Shannon_perc25) AS CitingRegions_Shannon_perc25,
  ANY_VALUE(CitingRegions_Shannon_perc50) AS CitingRegions_Shannon_perc50,
  ANY_VALUE(CitingRegions_Shannon_perc75) AS CitingRegions_Shannon_perc75,
  ANY_VALUE(CitingRegions_Shannon_perc100) AS CitingRegions_Shannon_perc100

FROM
  data_perc
GROUP BY year, CitationCount
ORDER BY year, CitationCount
