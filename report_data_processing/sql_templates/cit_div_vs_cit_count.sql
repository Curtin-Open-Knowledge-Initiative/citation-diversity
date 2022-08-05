DECLARE y INT64 DEFAULT 2019;

WITH
  data_perc AS (
      SELECT
        is_oa,
        CitationCount,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0) OVER(PARTITION BY CitationCount) AS CitingInstitutions_GiniSim_perc0,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.25) OVER(PARTITION BY CitationCount) AS CitingInstitutions_GiniSim_perc25,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY CitationCount) AS CitingInstitutions_GiniSim_perc50,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,0.75) OVER(PARTITION BY CitationCount) AS CitingInstitutions_GiniSim_perc75,
        PERCENTILE_CONT(CitingInstitutions_GiniSim,1) OVER(PARTITION BY CitationCount) AS CitingInstitutions_GiniSim_perc100,

        PERCENTILE_CONT(CitingCountries_GiniSim,0) OVER(PARTITION BY CitationCount) AS CitingCountries_GiniSim_perc0,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.25) OVER(PARTITION BY CitationCount) AS CitingCountries_GiniSim_perc25,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY CitationCount) AS CitingCountries_GiniSim_perc50,
        PERCENTILE_CONT(CitingCountries_GiniSim,0.75) OVER(PARTITION BY CitationCount) AS CitingCountries_GiniSim_perc75,
        PERCENTILE_CONT(CitingCountries_GiniSim,1) OVER(PARTITION BY CitationCount) AS CitingCountries_GiniSim_perc100,

        PERCENTILE_CONT(CitingSubregions_GiniSim,0) OVER(PARTITION BY CitationCount) AS CitingSubregions_GiniSim_perc0,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.25) OVER(PARTITION BY CitationCount) AS CitingSubregions_GiniSim_perc25,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY CitationCount) AS CitingSubregions_GiniSim_perc50,
        PERCENTILE_CONT(CitingSubregions_GiniSim,0.75) OVER(PARTITION BY CitationCount) AS CitingSubregions_GiniSim_perc75,
        PERCENTILE_CONT(CitingSubregions_GiniSim,1) OVER(PARTITION BY CitationCount) AS CitingSubregions_GiniSim_perc100,

        PERCENTILE_CONT(CitingRegions_GiniSim,0) OVER(PARTITION BY CitationCount) AS CitingRegions_GiniSim_perc0,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.25) OVER(PARTITION BY CitationCount) AS CitingRegions_GiniSim_perc25,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY CitationCount) AS CitingRegions_GiniSim_perc50,
        PERCENTILE_CONT(CitingRegions_GiniSim,0.75) OVER(PARTITION BY CitationCount) AS CitingRegions_GiniSim_perc75,
        PERCENTILE_CONT(CitingRegions_GiniSim,1) OVER(PARTITION BY CitationCount) AS CitingRegions_GiniSim_perc100,

        PERCENTILE_CONT(CitingInstitutions_Shannon,0) OVER(PARTITION BY CitationCount) AS CitingInstitutions_Shannon_perc0,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.25) OVER(PARTITION BY CitationCount) AS CitingInstitutions_Shannon_perc25,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY CitationCount) AS CitingInstitutions_Shannon_perc50,
        PERCENTILE_CONT(CitingInstitutions_Shannon,0.75) OVER(PARTITION BY CitationCount) AS CitingInstitutions_Shannon_perc75,
        PERCENTILE_CONT(CitingInstitutions_Shannon,1) OVER(PARTITION BY CitationCount) AS CitingInstitutions_Shannon_perc100,

        PERCENTILE_CONT(CitingCountries_Shannon,0) OVER(PARTITION BY CitationCount) AS CitingCountries_Shannon_perc0,
        PERCENTILE_CONT(CitingCountries_Shannon,0.25) OVER(PARTITION BY CitationCount) AS CitingCountries_Shannon_perc25,
        PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY CitationCount) AS CitingCountries_Shannon_perc50,
        PERCENTILE_CONT(CitingCountries_Shannon,0.75) OVER(PARTITION BY CitationCount) AS CitingCountries_Shannon_perc75,
        PERCENTILE_CONT(CitingCountries_Shannon,1) OVER(PARTITION BY CitationCount) AS CitingCountries_Shannon_perc100,

        PERCENTILE_CONT(CitingSubregions_Shannon,0) OVER(PARTITION BY CitationCount) AS CitingSubregions_Shannon_perc0,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.25) OVER(PARTITION BY CitationCount) AS CitingSubregions_Shannon_perc25,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY CitationCount) AS CitingSubregions_Shannon_perc50,
        PERCENTILE_CONT(CitingSubregions_Shannon,0.75) OVER(PARTITION BY CitationCount) AS CitingSubregions_Shannon_perc75,
        PERCENTILE_CONT(CitingSubregions_Shannon,1) OVER(PARTITION BY CitationCount) AS CitingSubregions_Shannon_perc100,

        PERCENTILE_CONT(CitingRegions_Shannon,0) OVER(PARTITION BY CitationCount) AS CitingRegions_Shannon_perc0,
        PERCENTILE_CONT(CitingRegions_Shannon,0.25) OVER(PARTITION BY CitationCount) AS CitingRegions_Shannon_perc25,
        PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY CitationCount) AS CitingRegions_Shannon_perc50,
        PERCENTILE_CONT(CitingRegions_Shannon,0.75) OVER(PARTITION BY CitationCount) AS CitingRegions_Shannon_perc75,
        PERCENTILE_CONT(CitingRegions_Shannon,1) OVER(PARTITION BY CitationCount) AS CitingRegions_Shannon_perc100
      FROM
        `coki-scratch-space.citation_diversity_analysis.citation_diversity_global`
      WHERE
        (CitationCount >= 2) AND (year=y) AND (is_oa IS NOT NULL)
  )
SELECT
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
GROUP BY CitationCount
ORDER BY CitationCount

