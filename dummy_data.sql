INSERT INTO 
    recsys.recsysweb_item (name, description, image)
VALUES (
    'Toy Story 4',
    'A classic 3D animation movie.',
    'https://m.media-amazon.com/images/M/MV5BYjY5MTYwMDYtNDk4OS00NmE1LWI2ZjItY2Q5ZmVmNTU4NTAyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_FMjpg_UY759_.jp'
);


SELECT 
	*
FROM
	(SELECT it.id as item_id, i.user_id as user_id, i.rating as rating FROM recsys.recsysweb_item AS it LEFT JOIN recsys.recsysweb_interaction AS i ON it.id  =  i.item_id) as r

ORDER BY r.rating DESC