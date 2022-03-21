# Change Log
Arquivo para documentação das mudanças realizadas ao longo do projeto. O formato desse arquivo é baseado no [Keep a Changelog](http://keepachangelog.com/)
e o presente projeto adota o [Semantic Versioning](http://semver.org/).

## [0.9.0] - 2021-11-17
- [COT-400](https://ecoanalytics.atlassian.net/browse/COT-400)
### Adicionado
- Sobrescrito a função `image_downloaded` do objeto `ImagesPipeline` para garantir a persistência de apenas imagens que ainda não estão salvas no storage.

## [0.8.0] - 2021-11-14
### [COT-308](https://ecoanalytics.atlassian.net/browse/COT-308)
#### Adicionado
- Adicionado `ItemCountMonitor` a suite de monitores.
- Adicionado `Shop2GNikeFemaleSpider` e `Shop2GNikeMaleSpider`
#### Removido
- Removido `SkuValidationMonitor` a suite de monitores.

## [0.7.3] - 2021-10-30
### [COT-295](https://ecoanalytics.atlassian.net/browse/COT-295)
#### Adicionado
- Adicionado tratamento de erro a função `parse_sku`.

## [0.7.2] - 2021-10-29
### [COT-292](https://ecoanalytics.atlassian.net/browse/COT-292)
#### Adicionado
- Adicionado tratamento de erro a função `parse_product_labels`.

## [0.7.1] - 2021-10-11
### [COT-234](https://ecoanalytics.atlassian.net/browse/COT-234)
#### Alterado
- Alterado a atribuição de `reference_first_image`.

## [0.7.0] - 2021-10-10
### [COT-205](https://ecoanalytics.atlassian.net/browse/COT-205)
#### Adicionado
- Adicionado a feature `reference_first_image` ao objeto `Shop2GetherItem`. 
- Adicionado a configuração `IMAGES_THUMBS` para salvar imagens no padrão 400x400.

## [0.6.0] - 2021-10-05
### [COT-156](https://ecoanalytics.atlassian.net/browse/COT-166)
#### Alterado
- Rollback do tipo de dado de `price` de `float` para `string`.

## [0.5.0] - 2021-10-04
### [COT-156](https://ecoanalytics.atlassian.net/browse/COT-156)
#### Adicionado
- Adicionado camada de monitoramento via [sentry](https://sentry.io/) ao projeto.
#### Alterado
- Alterado função `parse_sku` para contemplar novos padrões de sku nas páginas. 

## [0.4.0] - 2021-10-03
### [COT-144](https://ecoanalytics.atlassian.net/browse/COT-144)
#### Adicionado
- Adicionado camada de monitoramento via [spidermon](https://github.com/scrapinghub/spidermon) ao projeto.
- Envio de mensagem ao Discord em caso de url de produto sem sku.