/*
## Summary

Creates the main DOI level citation diversity table to be deployed to BigQuery

## Description

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://{citation_diversity_table}

## Creates
file summary_stats_by_year_all_papers.json

*/

WITH
  DataTemp1 AS(
    SELECT *
    FROM `{citation_diversity_table}`
    WHERE year>={first_year} AND year<={last_year} AND is_oa IS NOT NULL
  ),
  DataTemp2 AS(
    SELECT
      *,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, is_oa) AS oa_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, gold) AS gold_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, green) AS green_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, green_only) AS green_only_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, bronze) AS bronze_cc_median
    FROM DataTemp1
  )
SELECT
  year,
  COUNT(doi) as doi_count,
  COUNT(IF(is_oa=TRUE, doi, NULL)) as oa_count,
  COUNT(IF(is_oa=FALSE, doi, NULL)) as noa_count,
  COUNT(IF(gold=TRUE, doi, NULL)) as gold_count,
  COUNT(IF(green=TRUE, doi, NULL)) as green_count,
  COUNT(IF(green_only=TRUE, doi, NULL)) as green_only_count,
  COUNT(IF(hybrid=TRUE, doi, NULL)) as hybrid_count,
  COUNT(IF(bronze=TRUE, doi, NULL)) as bronze_count,
  AVG(IF(is_oa=TRUE , CitationCount, NULL)) as oa_cc_mean,
  ANY_VALUE(IF(is_oa=TRUE,oa_cc_median,NULL)) as oa_cc_median,
  AVG(IF(is_oa=FALSE, CitationCount, NULL)) as noa_cc_mean,
  ANY_VALUE(IF(is_oa=FALSE,oa_cc_median,NULL)) as noa_cc_median,
  AVG(IF(gold=TRUE , CitationCount, NULL)) as gold_cc_mean,
  ANY_VALUE(IF(gold=TRUE,gold_cc_median,NULL)) as gold_cc_median,
  AVG(IF(green=TRUE , CitationCount, NULL)) as green_cc_mean,
  ANY_VALUE(IF(green=TRUE,green_cc_median,NULL)) as green_cc_median,
  AVG(IF(green_only=TRUE , CitationCount, NULL)) as green_only_cc_mean,
  ANY_VALUE(IF(green_only=TRUE,green_only_cc_median,NULL)) as green_only_cc_median,
  AVG(IF(hybrid=TRUE , CitationCount, NULL)) as hybrid_cc_mean,
  ANY_VALUE(IF(hybrid=TRUE,hybrid_cc_median,NULL)) as hybrid_cc_median,
  AVG(IF(bronze=TRUE , CitationCount, NULL)) as bronze_cc_mean,
  ANY_VALUE(IF(bronze=TRUE,bronze_cc_median,NULL)) as bronze_cc_median
FROM  DataTemp2
GROUP BY year
ORDER BY year ASC