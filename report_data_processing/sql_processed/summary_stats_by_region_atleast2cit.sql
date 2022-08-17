/*
## Summary

CHANGE THIS

## Description

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://coki-scratch-space.karl.citation_diversity_global

## Creates
file summary_stats_by_region_atleast2cit.csv

*/

WITH
  datatemp1 AS (
    SELECT
      region.name AS region_cited,
      year,
      is_oa,
      ARRAY_CONCAT_AGG(CitingRegions_table) AS CitingRegions_table_temp,
      COUNT(doi) AS count_doi
    FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global`, UNNEST(regions) AS region
    WHERE (CitationCount >= 2) AND (region.name IS NOT NULL) AND (year IS NOT NULL) AND (is_oa IS NOT NULL)
    GROUP BY region.name, year, is_oa
  ),
  datatemp2 AS (
    SELECT
      * EXCEPT(CitingRegions_table_temp),
    ARRAY(SELECT AS STRUCT name, SUM(count) AS total FROM UNNEST(CitingRegions_table_temp) AS X GROUP BY name) AS CitingRegions_table_all
  FROM datatemp1
  )
SELECT
  region_cited,
  year,
  is_oa,
  count_doi,
  X.name AS region_citing,
  X.total AS region_citing_count
FROM datatemp2, UNNEST(CitingRegions_table_all) AS X