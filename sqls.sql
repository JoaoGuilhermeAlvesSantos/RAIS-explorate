SELECT 
  COALESCE(id_municipio, 'TOTAL') AS municipio,
  COUNT(*) AS total_vinculos
FROM `basedosdados.br_me_rais.microdados_vinculos` 
WHERE ano = 2023 
  AND cnae_2_subclasse LIKE '0155501' 
  AND vinculo_ativo_3112 = "1"
GROUP BY ROLLUP(id_municipio)
ORDER BY total_vinculos DESC

SELECT 
  COALESCE(id_municipio, 'TOTAL') AS municipio,
  COUNT(*) AS total_vinculos
FROM `basedosdados.br_me_rais.microdados_vinculos` 
WHERE ano = 2023 
  AND cnae_2_subclasse LIKE '0155502' 
  AND vinculo_ativo_3112 = "1"
GROUP BY ROLLUP(id_municipio)
ORDER BY total_vinculos DESC

SELECT 
  COALESCE(id_municipio, 'TOTAL') AS municipio,
  COUNT(*) AS total_vinculos
FROM `basedosdados.br_me_rais.microdados_vinculos` 
WHERE ano = 2023 
  AND cnae_2_subclasse LIKE '0155503' 
  AND vinculo_ativo_3112 = "1"
GROUP BY ROLLUP(id_municipio)
ORDER BY total_vinculos DESC

SELECT 
  COALESCE(id_municipio, 'TOTAL') AS municipio,
  COUNT(*) AS total_vinculos
FROM `basedosdados.br_me_rais.microdados_vinculos` 
WHERE ano = 2023 
  AND cnae_2_subclasse LIKE '0155504' 
  AND vinculo_ativo_3112 = "1"
GROUP BY ROLLUP(id_municipio)
ORDER BY total_vinculos DESC

SELECT 
  COALESCE(id_municipio, 'TOTAL') AS municipio,
  COUNT(*) AS total_vinculos
FROM `basedosdados.br_me_rais.microdados_vinculos` 
WHERE ano = 2023 
  AND cnae_2_subclasse LIKE '0155505' 
  AND vinculo_ativo_3112 = "1"
GROUP BY ROLLUP(id_municipio)
ORDER BY total_vinculos DESC