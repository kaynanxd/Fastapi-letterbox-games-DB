
--CRUD COMPLETO DE USUÁRIO

-- 1. CREATE
INSERT INTO users (username, email, password, admin) 
VALUES ('bia', 'bia@bia.com', '123456', 0);


-- 2. READ:
SELECT * FROM users WHERE username = 'bia@bia.com';


-- 3. UPDATE:
UPDATE users 
SET email = 'guy@gmail.com' 
WHERE id = 3;

SELECT * FROM users WHERE id = 1;


-- 4. DELETE:

DELETE FROM users WHERE id = 1;

SELECT * FROM users WHERE id = 1;


-- Jogos

--READ
SELECT 
    j.id_jogo,
    j.titulo, 
    j.nota_metacritic,
    d.mercado_principal AS tipo_dev
FROM jogos j
JOIN desenvolvedoras d ON j.id_desenvolvedor = d.id_empresa
WHERE j.titulo LIKE '%resident%';


-- CREATE
INSERT INTO watchlist_jogo (id_watchlist, id_jogo) 
VALUES (1, __);

SELECT w.nome, j.titulo 
FROM watchlist_jogo wj
JOIN watchlists w ON wj.id_watchlist = w.id_watchlist
JOIN jogos j ON wj.id_jogo = j.id_jogo
WHERE w.id_watchlist = 1;


-- 7 AVALIAR O JOGO
INSERT INTO avaliacoes (nota, comentario, id_jogo, id_user) 
VALUES (8, 'gostei bastante', 1, 1);


-- 8. CONSULTAR MINHAS REVIEWS

SELECT 
    u.username, 
    j.titulo, 
    a.nota, 
    a.comentario 
FROM avaliacoes a
JOIN users u ON a.id_user = u.id
JOIN jogos j ON a.id_jogo = j.id_jogo
WHERE u.id = 1;