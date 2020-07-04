# 章节结构思考————不定性
书的章节结构符合人们的学习习惯会让学习的过程变的顺畅，但是在写作过程中，必然不能一步到位，而是一个不断调整、整合的过程，因此增加了这个部分，来思考这个问题。


```mermaid
erDiagram
    USDAM-py ||--o{ geospatial-data : place 
    ORDER ||--|{ LINE-ITEM : contains
    USDAM-py }|..|{ DELIVERY-ADDRESS : uses
    data ||--|{ POI : Baidu
    POI ||--|{ geospatial-data : get-data
    POI ||--|{ single-classificaiton : crawler
    POI ||--|{ multiple-classificaiton : crawler
    single-classificaiton ||--|{ geospatial-data : geo
    USDAM-py }|..|{ descriptive-statistics : knowledge-point
```



