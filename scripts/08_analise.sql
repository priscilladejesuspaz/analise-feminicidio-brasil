use taxa_feminicidio;
select * from taxa_feminicidio;

-- Filtra valor de feminicidio por estado 
select 
	valor,
    estado, 
    filtro
from taxa_feminicidio
where filtro = "Feminicídios";

-- Média por ano de femínicio por estado 
select 
	valor,
	ano,
	estado
from taxa_feminicidio;

-- Total de feminicios por ano e estado
select 
	avg(valor) as media_total_fem, 
    ano, 
    estado
from taxa_feminicidio
where filtro = "Feminicídios"
group by ano, estado
order by ano desc, media_total_fem desc;

-- Evolução ao longo tempo
select 
	avg(valor) as media_total_fem, 
    ano, 
    estado
from taxa_feminicidio
where filtro = "Feminicídios"
group by ano, estado
order by ano desc, media_total_fem desc;

-- Estados que pioraram 
select 
	max(valor) - min(valor) as variacao,
    estado 
from taxa_feminicidio
where filtro = "Feminicídios"
group by estado 
order by variacao desc; 

-- Estados que melhoraram 
select 
	estado, 
	max(valor) - min(valor) as variacao
from taxa_feminicidio
where filtro = "Feminicídios"
group by estado 
order by variacao asc; 

-- Ranking anual dos estados com maior taxa de feminicídio
select 
	estado, 
    ano,
    avg(valor) as media_feminicidio 
from taxa_feminicidio
where filtro = "Feminicídios" 
group by ano, estado
order by ano desc, media_feminicidio asc;

select distinct
    estado,
    first_value(valor) over(partition by estado order by ano) as primeiro_valor,
    first_value(valor) over(partition by estado order by ano desc) as ultimo_valor
from taxa_feminicidio
where filtro = "Feminicídios";

select
    estado,
    primeiro_valor,
    ultimo_valor,
    round(ultimo_valor - primeiro_valor, 2) as variacao,
    case
        when ultimo_valor - primeiro_valor > 0 then 'Piorou'
        when ultimo_valor - primeiro_valor < 0 then 'Melhorou'
        else 'Estável'
    end as situacao
from (
    select distinct
        estado,
        first_value(valor) over(partition by estado order by ano) as primeiro_valor,
        first_value(valor) over(partition by estado order by ano desc) as ultimo_valor
    from taxa_feminicidio
    where filtro = 'Feminicídios'
) as subquery
order by variacao desc;