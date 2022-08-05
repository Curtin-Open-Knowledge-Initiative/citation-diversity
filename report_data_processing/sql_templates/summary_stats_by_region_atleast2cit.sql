#main
WITH
  datatemp1 AS (
    SELECT
      doi,
      year,
      is_oa,
      region.name AS region,
      CitingRegions_name,
      CitingRegions_table,
      CitingRegions_count_uniq,
      CitingRegions_GiniSim,
      CitingRegions_Shannon,
      PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY region.name, year, is_oa) AS CitingRegions_count_uniq_median,
      PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY region.name, year, is_oa) AS CitingRegions_GiniSim_median,
      PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY region.name, year, is_oa) AS CitingRegions_Shannon_median
    FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global`, UNNEST(regions) AS region
    WHERE CitationCount >= 2
  ),
  datatemp2 AS (
    SELECT
      region,
      year,
      is_oa,
      ARRAY_CONCAT_AGG(CitingRegions_table) AS CitingRegions_table_temp,
      AVG(CitingRegions_count_uniq) AS count_uniq_mean,
      ANY_VALUE(CitingRegions_count_uniq_median) AS count_uniq_median,
      AVG(CitingRegions_GiniSim) AS GiniSim_mean,
      ANY_VALUE(CitingRegions_GiniSim_median) AS GiniSim_median,
      AVG(CitingRegions_Shannon) AS Shannon_mean,
      ANY_VALUE(CitingRegions_Shannon_median) AS Shannon_median,
      COUNT(doi) AS count_doi
    FROM datatemp1
    WHERE (region IS NOT NULL) AND (year IS NOT NULL) AND (is_oa IS NOT NULL)
    GROUP BY region, year, is_oa
  )
SELECT
  * EXCEPT(CitingRegions_table_temp),
  ARRAY(SELECT AS STRUCT name, SUM(count) AS total FROM UNNEST(CitingRegions_table_temp) AS X GROUP BY name) AS CitingRegions_table_all
FROM datatemp2
