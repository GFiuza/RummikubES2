import os
from time import sleep

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
    jogo = Game()
    jogo.add_player('G', 0)
    jogo.add_player('F', 1, True)
    end_game = False
    mouse_offset = (0, 0)
    tile_moving = -1
    for k in range(14):
        for player in jogo.players:
            player.draw(jogo.deck)
            jogo.reset_player_tiles_position(player)
            player.sort_hand_rep()
    while not end_game:
        is_moving_piece = False
        for player in jogo.players:
            jogo.turn_display = jogo.turn_display_font.render("Vez de: " + player.name,
                                                              False, (0, 0, 0))
            jogo.update_frame(player)
            pygame.display.update()
            jogo.buttons.button_reset_pos()
            has_moved = 0
            end_turn = False
            tabuleiro_atual = jogo.table.tabuleiro
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
                            if not player_pieces_placed or not jogo.table.validity():
                                player.draw(jogo.deck)
                                jogo.reset_player_tiles_position(player)
                                jogo.table.tabuleiro = tabuleiro_atual
                                end_turn = True
                                break
                        if event.type == pygame.MOUSEBUTTONDOWN and jogo.buttons.validadeTurnRect.collidepoint(
                                pygame.mouse.get_pos()):
                            if jogo.table.validity() and player_pieces_placed:
                                jogo.table.commit_table(player)
                                jogo.reset_player_tiles_position(player)
                                jogo.table.tabuleiro = tabuleiro_atual
                                end_turn = True
                                break
                        if event.type == pygame.MOUSEBUTTONDOWN:
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

                        # Quando solta o pressionar do mouse
                        if event.type == pygame.MOUSEBUTTONUP:
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
                    if is_moving_piece:
                        player.hand[tile_moving].rect.x = pygame.mouse.get_pos()[0] - mouse_offset[0]
                        player.hand[tile_moving].rect.y = pygame.mouse.get_pos()[1] - mouse_offset[1]
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
