/*
## Summary
Generates samples of outputs across OA and non-OA papers and across citation groups for a given year

## Description
Creates a table, for a given publication year, that contains samples of DOIs, with their corresponding:
- numbers of unique citing groups;
- GiniSim scores by citing groups;
- Shannon scores by citing groups.
The DOIs are randomly sampled for each citation group, with 2000 OA outputs and 2000 non-OA outputs per citation group.

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://coki-scratch-space.citation_diversity_analysis.citation_diversity_global

## Creates
file samples_by_cit_group_and_oa_2015.csv

*/

WITH
  group_2 AS (
      (SELECT
        doi,
        '2' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount=2 AND year=2015 AND is_oa=TRUE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '2' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount=2 AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_3 AS (
      (SELECT
        doi,
        '3' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount=3 AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '3' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount=3 AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_4 AS (
      (SELECT
        doi,
        '4' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount=4 AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '4' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount=4 AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_5_6 AS (
      (SELECT
        doi,
        '5-6' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 5 AND 6) AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '5-6' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 5 AND 6) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_7_9 AS (
      (SELECT
        doi,
        '7-9' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 7 AND 9) AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '7-9' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 7 AND 9) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_10_11 AS (
      (SELECT
        doi,
        '10-11' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 10 AND 11) AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '10-11' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 10 AND 11) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_12_14 AS (
      (SELECT
        doi,
        '12-14' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 12 AND 14) AND year=2015 AND is_oa=TRUE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '12-14' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 12 AND 14) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_15_16 AS (
      (SELECT
        doi,
        '15-16' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 15 AND 16) AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '15-16' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 15 AND 16) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_17_19 AS (
      (SELECT
        doi,
        '17-19' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 17 AND 19) AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '17-19' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 17 AND 19) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_20_23 AS (
      (SELECT
        doi,
        '20-23' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 20 AND 23) AND year=2015 AND is_oa=TRUE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '20-23' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 20 AND 23) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_24_29 AS (
      (SELECT
        doi,
        '24-29' AS cit_group,
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 24 AND 29) AND year=2015 AND is_oa=TRUE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '24-29' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 24 AND 29) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_30_42 AS (
      (SELECT
        doi,
        '30-42' AS cit_group,
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 30 AND 42) AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '30-42' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 30 AND 42) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_43_59 AS (
      (SELECT
        doi,
        '43-59' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 43 AND 59) AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '43-59' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount BETWEEN 43 AND 59) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  group_60_above AS (
      (SELECT
        doi,
        '>=60' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount >= 60) AND year=2015 AND is_oa=TRUE)
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
      UNION ALL
      (SELECT
        doi,
        '>=60' AS cit_group
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE (CitationCount >=60) AND year=2015 AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(doi)
      LIMIT 2000)
  ),
  sample AS (
      SELECT
        doi,
        cit_group
      FROM (SELECT * FROM group_2
      UNION ALL SELECT * FROM group_3
      UNION ALL SELECT * FROM group_4
      UNION ALL SELECT * FROM group_5_6
      UNION ALL SELECT * FROM group_7_9
      UNION ALL SELECT * FROM group_10_11
      UNION ALL SELECT * FROM group_12_14
      UNION ALL SELECT * FROM group_15_16
      UNION ALL SELECT * FROM group_17_19
      UNION ALL SELECT * FROM group_20_23
      UNION ALL SELECT * FROM group_24_29
      UNION ALL SELECT * FROM group_30_42
      UNION ALL SELECT * FROM group_43_59
      UNION ALL SELECT * FROM group_60_above))

SELECT
  doi,
  year,
  is_oa,
  cit_group,
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
FROM sample LEFT JOIN `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` USING(doi)

