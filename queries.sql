select d.* from dogs_database.D_description as d, dogs_database.D_description_finder as f
where ((d.ID = f.ID or f.ID is null)
and (d.NAME = f.NAME or f.NAME is null)
and (d.BREED_PRIMARY  = f.BREED_PRIMARY  or f.BREED_PRIMARY  is null)
and (d.BREED_SECONDARY = f.BREED_SECONDARY or f.BREED_SECONDARY is null)
and (d.BREED_MIXED = f.BREED_MIXED or f.BREED_MIXED is null)
and (d.COLOR = f.COLOR or f.COLOR is null)
and (d.AGE = f.AGE or f.AGE is null)
and (d.SEX = f.SEX or f.SEX is null)
and (d.DIMENSION = f.DIMENSION or f.DIMENSION is null)
and (d.COAT = f.COAT or f.COAT is null)
and (d.HOUSE_TRAINED = f.HOUSE_TRAINED or f.HOUSE_TRAINED is null)
and (d.FIXED = f.FIXED or f.FIXED is null)
and (d.SPECIAL_NEEDS = f.SPECIAL_NEEDS or f.SPECIAL_NEEDS is null)
and (d.SHOTS_CURRENT = f.SHOTS_CURRENT or f.SHOTS_CURRENT is null)
and (d.ENV_CHILDREN = f.ENV_CHILDREN or f.ENV_CHILDREN is null)
and (d.ENV_DOGS = f.ENV_DOGS or f.ENV_DOGS is null)
and (d.ENV_CATS = f.ENV_CATS or f.ENV_CATS is null)
and (d.CITY = f.CITY or f.CITY is null)
and (d.STATE = f.STATE or f.STATE is null)
and (d.ZIP = f.ZIP or f.ZIP is null)
and (d.COUNTRY = f.COUNTRY or f.COUNTRY is null));

select d.* from dogs_database.D_description as d join dogs_database.D_travel on d.ID = D_travel.ID, dogs_database.D_description_finder as f
where ((d.ID = f.ID or f.ID is null)
and (d.NAME = f.NAME or f.NAME is null)
and (d.BREED_PRIMARY  = f.BREED_PRIMARY  or f.BREED_PRIMARY  is null)
and (d.BREED_SECONDARY = f.BREED_SECONDARY or f.BREED_SECONDARY is null)
and (d.BREED_MIXED = f.BREED_MIXED or f.BREED_MIXED is null)
and (d.COLOR = f.COLOR or f.COLOR is null)
and (d.AGE = f.AGE or f.AGE is null)
and (d.SEX = f.SEX or f.SEX is null)
and (d.DIMENSION = f.DIMENSION or f.DIMENSION is null)
and (d.COAT = f.COAT or f.COAT is null)
and (d.HOUSE_TRAINED = f.HOUSE_TRAINED or f.HOUSE_TRAINED is null)
and (d.FIXED = f.FIXED or f.FIXED is null)
and (d.SPECIAL_NEEDS = f.SPECIAL_NEEDS or f.SPECIAL_NEEDS is null)
and (d.SHOTS_CURRENT = f.SHOTS_CURRENT or f.SHOTS_CURRENT is null)
and (d.ENV_CHILDREN = f.ENV_CHILDREN or f.ENV_CHILDREN is null)
and (d.ENV_DOGS = f.ENV_DOGS or f.ENV_DOGS is null)
and (d.ENV_CATS = f.ENV_CATS or f.ENV_CATS is null)
and (d.CITY = f.CITY or f.CITY is null)
and (d.STATE = f.STATE or f.STATE is null)
and (d.ZIP = f.ZIP or f.ZIP is null)
and (d.COUNTRY = f.COUNTRY or f.COUNTRY is null)
and dogs_database.d_travel.STILL_THERE = 1);

select d.* from dogs_database.D_description as d join dogs_database.D_travel on d.ID = D_travel.ID, dogs_database.D_description_finder as f
where ((d.ID = f.ID or f.ID is null)
and (d.NAME = f.NAME or f.NAME is null)
and (d.BREED_PRIMARY  = f.BREED_PRIMARY  or f.BREED_PRIMARY  is null)
and (d.BREED_SECONDARY = f.BREED_SECONDARY or f.BREED_SECONDARY is null)
and (d.BREED_MIXED = f.BREED_MIXED or f.BREED_MIXED is null)
and (d.COLOR = f.COLOR or f.COLOR is null)
and (d.AGE = f.AGE or f.AGE is null)
and (d.SEX = f.SEX or f.SEX is null)
and (d.DIMENSION = f.DIMENSION or f.DIMENSION is null)
and (d.COAT = f.COAT or f.COAT is null)
and (d.HOUSE_TRAINED = f.HOUSE_TRAINED or f.HOUSE_TRAINED is null)
and (d.FIXED = f.FIXED or f.FIXED is null)
and (d.SPECIAL_NEEDS = f.SPECIAL_NEEDS or f.SPECIAL_NEEDS is null)
and (d.SHOTS_CURRENT = f.SHOTS_CURRENT or f.SHOTS_CURRENT is null)
and (d.ENV_CHILDREN = f.ENV_CHILDREN or f.ENV_CHILDREN is null)
and (d.ENV_DOGS = f.ENV_DOGS or f.ENV_DOGS is null)
and (d.ENV_CATS = f.ENV_CATS or f.ENV_CATS is null)
and (d.CITY = f.CITY or f.CITY is null)
and (d.STATE = f.STATE or f.STATE is null)
and (d.ZIP = f.ZIP or f.ZIP is null)
and (d.COUNTRY = f.COUNTRY or f.COUNTRY is null)
and dogs_database.d_travel.STILL_THERE = 0);

select count(*) from dogs_database.D_description join dogs_database.D_travel on D_description.ID = D_travel.ID
where D_description.AGE  = 'Young' and D_travel.FOUND = 'Albuquerque';

select city, count(*) from dogs_database.D_description
group by city order by count(*) desc;

select * from dogs_database.D_description
where D_description.name like '%Felix%';

select sum(EXPORTED), sum(IMPORTED) from dogs_database.d_moves_by_location
where d_moves_by_location.INSIDE_US = True;

select id from dogs_database.d_travel
where d_travel.found = 'Fort Valley'
and d_travel.id in (select id from dogs_database.d_description where d_description.name = 'Snoopy')
    
