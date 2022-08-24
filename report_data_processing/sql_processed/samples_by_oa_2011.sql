/*
## Summary
Generates samples of outputs across OA categories for a given year

## Description
Creates a table, for a given publication year, that contains samples of DOIs, with their corresponding:
- numbers of unique citing groups;
- GiniSim scores by citing groups;
- Shannon scores by citing groups.
The DOIs are randomly sampled for each OA category, with 10,000 outputs per category.

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://coki-scratch-space.citation_diversity_analysis.citation_diversity_global

## Creates
file samples_by_oa_2011.csv

*/

WITH
  sample_oa AS (
      (SELECT
        doi,
        TRUE AS s_oa
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount>=2 AND year=2011 AND is_oa=TRUE )
      ORDER BY FARM_FINGERPRINT(CONCAT(doi,'1'))
      LIMIT 10000)
  ),
  sample_noa AS (
      (SELECT
        doi,
        TRUE AS s_noa,
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount>=2 AND year=2011 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(CONCAT(doi,'2'))
      LIMIT 10000)
  ),
  sample_gold AS (
      (SELECT
        doi,
        TRUE AS s_gold,
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount>=2 AND year=2011 AND gold=TRUE )
      ORDER BY FARM_FINGERPRINT(CONCAT(doi,'3'))
      LIMIT 10000)
  ),
  sample_green AS (
      (SELECT
        doi,
        TRUE AS s_green,
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount>=2 AND year=2011 AND green=TRUE )
      ORDER BY FARM_FINGERPRINT(CONCAT(doi,'4'))
      LIMIT 10000)
  )
SELECT
  doi,
  year,
  s_oa,
  s_noa,
  s_gold,
  s_green,
  CitationCount,
  CitingInstitutions_count_uniq,
  CitingCountries_count_uniq,
  CitingSubregions_count_uniq,
  CitingRegions_count_uniq,
  CitingFields_count_uniq,
  CitingInstitutions_GiniSim,
  CitingCountries_GiniSim,
  CitingSubregions_GiniSim,
  CitingRegions_GiniSim,
  CitingFields_GiniSim,
  CitingInstitutions_Shannon,
  CitingCountries_Shannon,
  CitingSubregions_Shannon,
  CitingRegions_Shannon,
  CitingFields_Shannon
FROM (sample_oa FULL JOIN sample_noa USING(doi)
                FULL JOIN sample_gold USING (doi)
                FULL JOIN sample_green USING(doi))
  LEFT JOIN `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` USING(doi)

