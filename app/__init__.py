import os

os.environ['background'] = 'resources/static/game_background.png'
os.environ['draw_unlock'] = 'resources/buttons/comprar_mais.png'
os.environ['draw_lock'] = 'resources/buttons/comprar_mais_lock.png'
os.environ['backgound_grid'] = 'resources/static/game_background_grid.png'
os.environ['end_turn'] = 'resources/buttons/end_turn.png'

from app.game.Game import *

game_state = 2
qntd_jogos = 1
close_game = False
game_list = []
for i in range(qntd_jogos):
    if close_game:
        break
    jogo = Game()
    jogo.add_player('G', 0)
    # jogo.add_player('SG', 1)
    end_game = False
    mouse_offset = (0, 0)
    tile_moving = -1
    for k in range(14):
        for player in jogo.players:
            player.doneMeld = False
            player.draw(jogo.deck)
            jogo.reset_player_tiles_position(player)
            player.sort_hand_rep()
    while not end_game and not close_game:
        is_moving_piece = False
        for player in jogo.players:
            if close_game or end_game:
                break
            jogo.turn_display = jogo.turn_display_font.render("Vez de: " + player.name, False, (0, 0, 0))
            jogo.update_frame(player)
            pygame.display.update()
            jogo.buttons.button_reset_pos()
            has_moved = 0
            end_turn = False
            tabuleiro_atual = [[single for single in table] for table in jogo.table.tabuleiro]
            player_pieces_placed = []
            while not end_game and not close_game and not end_turn:
                if not player.IA:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            close_game = True
                            break
                        jogo.update_on_hover(pygame.mouse.get_pos())
                        player.sort_hand_rep()
                        if event.type == pygame.MOUSEBUTTONDOWN and jogo.buttons.drawButtnRect.collidepoint(
                                pygame.mouse.get_pos()):
                            # Permite comprar caso o jogador não tenha posto peça, ou o tabuleiro não esteja válido
                            # ou o jogador não tenha feito o initial_meld
                            if not player_pieces_placed or not jogo.table.validity() or not player.doneMeld:
                                player.draw(jogo.deck)
                                jogo.table.rollback(player, tabuleiro_atual)
                                jogo.reset_player_tiles_position(player)
                                jogo.table.tabuleiro = tabuleiro_atual
                                end_turn = True
                                break
                        if event.type == pygame.MOUSEBUTTONDOWN and jogo.buttons.validadeTurnRect.collidepoint(
                                pygame.mouse.get_pos()):
                            # Verificando se já foi realizado o initial_meld. Se não, roda a função para
                            # verificar a pontuação
                            if not player.doneMeld:
                                player.doneMeld = True if player.initial_meld(player_pieces_placed, jogo.table.get_groups()) >= 30 else False

                            # Somente permite passar de turno (sem comprar) caso o tabuleiro esteja válido
                            # tenha sido feito o initial_meld e se ele tiver jogado peça
                            if jogo.table.validity() and player_pieces_placed and player.doneMeld:
                                jogo.table.clear_hand(player)
                                jogo.reset_player_tiles_position(player)
                                end_turn = True
                                break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if not is_moving_piece:
                                for i in range(len(player.hand)):
                                    if player.hand[i].rect.collidepoint(pygame.mouse.get_pos()):
                                        is_moving_piece = True
                                        mouse_offset = (pygame.mouse.get_pos()[0] - player.hand[i].rect.x,
                                                        pygame.mouse.get_pos()[1] - player.hand[i].rect.y)
                                        tile_moving = i
                                        #Se a peca selecionada estiver no tabuleiro, guardar local onde esta caso o jogador tente coloca la num local invalido
                                        if player.hand[tile_moving].whereAt == PieceLocale.TABLE:
                                            last_x = player.hand[tile_moving].rect.x
                                            last_y = player.hand[tile_moving].rect.y
                            if not is_moving_piece:
                                found = False
                                for line_tab in range(len(jogo.table.tabuleiro)):
                                    if found:
                                        break
                                    for col_tab in range(len(jogo.table.tabuleiro[line_tab])):
                                        tab = jogo.table.tabuleiro[line_tab][col_tab]
                                        if tab.value != PieceValue.BLANK and tab.rect.collidepoint(pygame.mouse.get_pos()):
                                            is_moving_piece = True
                                            mouse_offset = (pygame.mouse.get_pos()[0] - tab.rect.x,
                                                            pygame.mouse.get_pos()[1] - tab.rect.y)
                                            tile_moving = [line_tab, col_tab]
                                            last_x = tab.rect.x
                                            last_y = tab.rect.y
                                            found = True
                                            break

                        # Quando solta o pressionar do mouse
                        if event.type == pygame.MOUSEBUTTONUP:
                            if type(tile_moving) is int or type(tile_moving) is str:
                                # Se verdade, significa que o clique foi em cima de uma peca, entao essa peca pode ter sido movida
                                if is_moving_piece:
                                    x, y = jogo.table.collidePiece(player.hand[tile_moving])
                                    if x == -1:
                                        # Retorna la a posicao inicial somente se ela nao tiver passado pelo tabuleiro ainda
                                        if player.hand[tile_moving].whereAt == PieceLocale.HAND:
                                            player.hand[tile_moving].rect.x, player.hand[tile_moving].rect.y = player.hand[tile_moving].originalPlace
                                        else:
                                            player.hand[tile_moving].rect.x = last_x
                                            player.hand[tile_moving].rect.y = last_y
                                    else:
                                        player.hand[tile_moving].rect.x = x
                                        player.hand[tile_moving].rect.y = y
                                        player_pieces_placed.append(player.hand[tile_moving])
                                    tile_moving = -1
                                    is_moving_piece = False
                                    mouse_offset = (0, 0)
                            else:
                                if is_moving_piece:
                                    piece = jogo.table.tabuleiro[tile_moving[0]][tile_moving[1]]
                                    x, y = jogo.table.collidePiece(piece)
                                    if x == -1:
                                        # Retorna la a posicao inicial somente se ela nao tiver passado pelo tabuleiro ainda
                                        piece.rect.x = last_x
                                        piece.rect.y = last_y
                                    else:
                                        piece.rect.x = x
                                        piece.rect.y = y
                                        # player_pieces_placed.append(player.hand[tile_moving])
                                    tile_moving = -1
                                    is_moving_piece = False
                                    mouse_offset = (0, 0)
                    if is_moving_piece and (type(tile_moving) is int or type(tile_moving) is str):
                        player.hand[tile_moving].rect.x = pygame.mouse.get_pos()[0] - mouse_offset[0]
                        player.hand[tile_moving].rect.y = pygame.mouse.get_pos()[1] - mouse_offset[1]
                    elif is_moving_piece:
                        jogo.table.tabuleiro[tile_moving[0]][tile_moving[1]].rect.x = pygame.mouse.get_pos()[0] - mouse_offset[0]
                        jogo.table.tabuleiro[tile_moving[0]][tile_moving[1]].rect.y = pygame.mouse.get_pos()[1] - mouse_offset[1]
                # Ignora o evento de clique enquanto nao estiver na vez do jogador, para evitar crash
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            for i in range(len(player.hand)):
                                if player.hand[i].rect.collidepoint(pygame.mouse.get_pos()):
                                    continue
                    pygame.time.wait(1000)
                    end_turn = True
                jogo.update_frame(player)
                pygame.display.update()
                jogo.buttons.button_reset_pos()
    game_list.append(jogo)  # TODO salvar tudo em algum arquivo quando já tiver pontuação etc
    if close_game:
        exit(0)
