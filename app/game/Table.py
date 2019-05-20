import pygame
from app.game.Piece import *
from typing import List, Tuple


class GameTable(object):
    def __init__(self, image_file, location):
        self.tabuleiro: List[List[Piece]] = [[Piece(PieceValue.BLANK, PieceColor.BLANK) for x in range(Table.COLUMNS.value)]
                                             for y in range(Table.ROWS.value)]
        self.image: pygame.image = pygame.image.load(image_file)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def __str__(self):
        string = ""
        for row in self.tabuleiro:
            for cell in row:
                string += "|" + cell.toString() + "|"
            string += "\n"
        return string

    # função que retorna todos as peças agrupadas em uma matriz (cada linha é um conjunto de peças)
    def get_groups(self) -> List[List[Piece]]:
        # variavel que vai conter o resultado final
        result: List[List[Piece]] = []


        for i in range(len(self.tabuleiro)):
            # variavel temporaria para obter um grupo de peças que estão lado a lado
            tempGroups: List[Piece] = []
            for j in range(len(self.tabuleiro[i])):
                # se a peça analisada não tem valor vazio, adiciona a tempGroups
                if self.tabuleiro[i][j].value.value != PieceValue.BLANK:
                    tempGroups.append(self.tabuleiro[i][j])
                # caso contrario, se tempGroups não for vazio, adiciona ao retorno e esvazia tempGroups
                else:
                    if len(tempGroups) > 0:
                        result.append(tempGroups)
                    tempGroups = []
        return result

    def validity(self) -> bool:
        # obtem todas as peças que estão lado a lado em arrays separados
        groups = self.get_groups()

        # para cada grupo de peças
        for i in groups:
            # se o tamanho do grupo for menor que 3, então o tabuleiro não é valido
            if len(i) < 3:
                return False

            # sao pegos 2 peças diferentes de joker para verificar se o grupo é uma sequencia ou trinca/quadra
            refValue = -1
            for j in i:
                # se j for diferente de joker e refValue ainda for -1, pega o valor de j e coloca em refValue
                if j.value.value != PieceValue.JOKER.value and refValue == -1:
                    refValue = j.value.value
                    continue
                # se j for diferente de joker e refValue não for -1,
                # então encontrou 2 peças com valores diferentes de joker
                if j.value.value != PieceValue.JOKER.value:
                    # se refValue e j tiverem o mesmo valor, então é uma trinca/quadra
                    # se refValue e j não tiverem o mesmo valor, então é uma sequencia
                    if refValue != j.value.value:
                        refValue = -1
                    break
            # checagem de trinca/quadra
            if refValue != -1:
                colors: List[PieceColor] = [PieceColor.YELLOW, PieceColor.BLACK, PieceColor.BLUE, PieceColor.RED]
                # se o tamanho do grupo for maior que 4, então o grupo é invalido
                if len(i) > 4:
                    return False
                for j in i:
                    # se o valor de J for diferente de refValue e diferente de joker, então o grupo não é válido
                    if j.value.value != refValue and j.value.value != PieceValue.JOKER.value:
                        return False
                    else:
                        if j.color in colors:
                            for color in range(len(colors)):
                                if j.color == colors[color]:
                                    colors.pop(color)
                                    break
                            continue
                        if j.color == PieceColor.JOKER:
                            continue
                        return False

            else:
                # Guarda a cor que deve ser igual para todas as peças em uma variavel
                refColor = i[0].color
                # verificação de sequencia
                for j in i:
                    # se o valor de refValue for -1 (primeira iteração)
                    # ou for igual a joker(caso a primeira peça do grupo seja um joker)
                    # atualiza o valor de refValue
                    if refValue == -1 or refValue == PieceValue.JOKER.value:
                        refValue = j.value.value
                    # caso contrario, verifica se o valor de J é igual a refValue -1 ou igual a Joker
                    else:
                        if (j.value.value - 1) == refValue or j.value.value == PieceValue.JOKER.value:
                            # se j tem a mesma cor que refColor ou é um joker
                            if j.color == refColor or j.color == PieceColor.JOKER:
                                refValue += 1
                        else:
                            return False
            return True

    def collidePiece(self, piece: Piece) -> Tuple[int, int]:
        # Se algum píxel da peça colidiu com algum pixel do tabuleiro:
        if self.rect.colliderect(piece.rect):
            # 0,0 do grid do tabuleiro
            baseCoord = (self.rect.x, self.rect.y)

            # x,y do centro da peça
            pieceCoord = piece.rect.center

            # Se o centro da peça estiver fora do grid, retorna pra mão do jogador
            if pieceCoord[1] > self.rect.y + self.rect.height \
                    or pieceCoord[0] > self.rect.x + self.rect.width \
                    or pieceCoord[1] < self.rect.y \
                    or pieceCoord[0] < self.rect.x:
                return -1, -1

            # Tamanho de um slot no tabuleiro ; O  tabuleiro é do tamanho 24 x 8
            height = self.rect.height / Table.ROWS.value
            width = self.rect.width / Table.COLUMNS.value

            # Índice da matriz onde a peça tentará encaixar
            relativeX = int(pieceCoord[0] - baseCoord[0]) // width
            relativeY = int(pieceCoord[1] - baseCoord[1]) // height

            # Verifica se o indice e valido e se nao ha nenhuma peca nessa casa do tabuleiro
            if relativeX < Table.COLUMNS.value and relativeY < Table.ROWS.value:
                # Se ele tentar mover uma peca para uma casa  ja preenchida
                if self.tabuleiro[int(relativeY)][int(relativeX)].value.value != -1:
                    # Se a peca que ele tentar mover for dele, cancela o movimento
                    if self.tabuleiro[int(relativeY)][int(relativeX)].whereAt == PieceLocale.HAND:
                        # Se moveu a peca para a mesma casa
                        if self.tabuleiro[int(relativeY)][int(relativeX)] == piece:
                            return relativeX * width + baseCoord[0], relativeY * height + baseCoord[1]
                        # Se nao, volta pra mao

                    return -1, -1
                else:
                    for i in range(Table.ROWS.value):
                        for j in range(Table.COLUMNS.value):
                            # Se a peca esta em alguma outra posicao no tabuleiro, move ela
                            if self.tabuleiro[i][j] == piece:
                                self.tabuleiro[i][j] = Piece(PieceValue.BLANK, PieceColor.BLANK)
                            self.tabuleiro[int(relativeY)][int(relativeX)] = piece

            relativeX = relativeX * width + baseCoord[0]
            relativeY = relativeY * height + baseCoord[1]

            return relativeX, relativeY
        return -1, -1