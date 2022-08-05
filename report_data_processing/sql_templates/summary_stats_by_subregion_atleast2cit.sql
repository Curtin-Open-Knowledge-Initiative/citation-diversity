#main
WITH
  datatemp1 AS (
    SELECT
      doi,
      year,
      is_oa,
      subregion.name AS subregion,
      CitingSubregions_name,
      CitingSubregions_table,
      CitingSubregions_count_uniq,
      CitingSubregions_GiniSim,
      CitingSubregions_Shannon,
      PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY subregion.name, year, is_oa) AS CitingSubregions_count_uniq_median,
      PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY subregion.name, year, is_oa) AS CitingSubregions_GiniSim_median,
      PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY subregion.name, year, is_oa) AS CitingSubregions_Shannon_median
    FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global`, UNNEST(subregions) AS subregion
    WHERE CitationCount >= 2
  ),
  datatemp2 AS (
    SELECT
      subregion,
      year,
      is_oa,
      ARRAY_CONCAT_AGG(CitingSubregions_table) AS CitingSubregions_table_temp,
      AVG(CitingSubregions_count_uniq) AS count_uniq_mean,
      ANY_VALUE(CitingSubregions_count_uniq_median) AS count_uniq_median,
      AVG(CitingSubregions_GiniSim) AS GiniSim_mean,
      ANY_VALUE(CitingSubregions_GiniSim_median) AS GiniSim_median,
      AVG(CitingSubregions_Shannon) AS Shannon_mean,
      ANY_VALUE(CitingSubregions_Shannon_median) AS Shannon_median,
      COUNT(doi) AS count_doi
    FROM datatemp1
    WHERE (subregion IS NOT NULL) AND (year IS NOT NULL) AND (is_oa IS NOT NULL)
    GROUP BY subregion, year, is_oa
  )
SELECT
  * EXCEPT(CitingSubregions_table_temp),
  ARRAY(SELECT AS STRUCT name, SUM(count) AS total FROM UNNEST(CitingSubregions_table_temp) AS X GROUP BY name) AS CitingSubregions_table_all
FROM datatemp2
