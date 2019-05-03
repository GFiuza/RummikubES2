import os
os.environ['background'] = 'resources/static/game_background.png'
os.environ['draw_unlock'] = 'resources/buttons/comprar_mais.png'
os.environ['draw_lock'] = 'resources/buttons/comprar_mais_lock.png'
os.environ['backgound_grid'] = 'resources/static/game_background_grid.png'


from app.game.Game import *
game_state = 2
qntd_jogos = 1
close_game = False
game_list = []
for i in range(qntd_jogos):
    jogo = Game()
    jogo.add_player('Player1', 0)
    end_game = False
    is_moving_piece = False
    mouse_offset = (0, 0)
    tile_moving = -1
    while not end_game and not close_game:
        jogo.deck.drawButtnRect.x = Size.WindowWidth * 0.9
        jogo.deck.drawButtnRect.y = Size.WindowHeight / 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN and jogo.deck.drawButtnRect.collidepoint(
                    pygame.mouse.get_pos()):
                jogo.players[0].draw(jogo.deck)
                jogo.reset_player_tiles_position()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(jogo.players[0].hand)):
                    if jogo.players[0].hand[i].rect.collidepoint(pygame.mouse.get_pos()):
                        is_moving_piece = True
                        mouse_offset = (pygame.mouse.get_pos()[0] - jogo.players[0].hand[i].rect.x,
                                        pygame.mouse.get_pos()[1] - jogo.players[0].hand[i].rect.y)
                        tile_moving = i
                        #Se a peca selecionada estiver no tabuleiro, guardar local onde esta caso o jogador tente coloca la num local invalido
                        if jogo.players[0].hand[tile_moving].whereAt == PieceLocale.TABLE:
                            last_x = jogo.players[0].hand[tile_moving].rect.x
                            last_y = jogo.players[0].hand[tile_moving].rect.y


            # Quando solta o pressionar do mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # Se verdade, significa que o clique foi em cima de uma peca, entao essa peca pode ter sido movida
                if is_moving_piece:
                    x, y = jogo.table.collidePiece(jogo.players[0].hand[tile_moving])
                    if x == -1:
                        # Retorna la a posicao inicial somente se ela nao tiver passado pelo tabuleiro ainda
                        if jogo.players[0].hand[tile_moving].whereAt == PieceLocale.HAND:
                            jogo.players[0].hand[tile_moving].rect.x, jogo.players[0].hand[tile_moving].rect.y = jogo.players[0].hand[tile_moving].originalPlace
                        else:
                            jogo.players[0].hand[tile_moving].rect.x = last_x
                            jogo.players[0].hand[tile_moving].rect.y = last_y
                    else:
                        jogo.players[0].hand[tile_moving].rect.x = x
                        jogo.players[0].hand[tile_moving].rect.y = y
                        jogo.players[0].hand[tile_moving].whereAt = PieceLocale.TABLE
                    tile_moving = -1
                    is_moving_piece = False
                    mouse_offset = (0, 0)
        if is_moving_piece:
            jogo.players[0].hand[tile_moving].rect.x = pygame.mouse.get_pos()[0] - mouse_offset[0]
            jogo.players[0].hand[tile_moving].rect.y = pygame.mouse.get_pos()[1] - mouse_offset[1]
        jogo.update_frame()
        pygame.display.update()
    game_list.append(jogo)      # TODO salvar tudo em algum arquivo quando já tiver pontuação etc
    if close_game:
        exit(0)