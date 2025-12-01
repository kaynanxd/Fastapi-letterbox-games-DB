
INSERT INTO users (username, email, password, admin) VALUES 
('admin_kaynan', 'kaynan@admin.com', '123456', 1),
('usuario_demo', 'demo@email.com', '123456', 0);


INSERT INTO empresas (nome, tipo_empresa, pais_origem) VALUES ('Capcom', 'desenvolvedora', 'Japão');
INSERT INTO desenvolvedoras (id_empresa, mercado_principal) VALUES (1, 'Global');

INSERT INTO empresas (nome, tipo_empresa, pais_origem) VALUES ('Nintendo', 'publicadora', 'Japão');
INSERT INTO publicadoras (id_empresa, mercado_principal) VALUES (2, 'Consoles');

INSERT INTO empresas (nome, tipo_empresa, pais_origem) VALUES ('FromSoftware', 'desenvolvedora', 'Japão');
INSERT INTO desenvolvedoras (id_empresa, mercado_principal) VALUES (3, 'Hardcore Games');


INSERT INTO jogos (titulo, descricao, nota_metacritic, id_desenvolvedor, id_publicadora) VALUES 
('Resident Evil 4', 'Survival Horror', 93, 1, 2),
('Zelda BOTW', 'Aventura', 97, 1, 2), 
('Elden Ring', 'RPG Ação', 96, 3, 2);


INSERT INTO generos (nome_genero) VALUES ('Survival Horror'), ('Aventura'), ('RPG');
INSERT INTO plataformas (nome) VALUES ('PC'), ('PS5'), ('Switch');


INSERT INTO jogo_plataformas VALUES (1, 2, '2023-03-24'); 
INSERT INTO jogo_genero VALUES (1, 1); 


INSERT INTO watchlists (id_user, nome) VALUES (2, 'Lista de Férias');
INSERT INTO watchlist_jogo (id_watchlist, id_jogo) VALUES (1, 1); 


INSERT INTO avaliacoes (nota, comentario, id_jogo, id_user) VALUES 
(10.0, 'Jogo Perfeito!', 1, 2);