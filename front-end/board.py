import pygame
import random
from enum import Enum

CELL_SIZE = 100
PIECE_IMAGE_SIZE = (CELL_SIZE, CELL_SIZE)
BOARD_SIZE = (3, 5)


class PieceColor(Enum):
    WHITE = 1
    BLACK = 2


def getPyGameColor(pcolor: PieceColor):
    match pcolor:
        case PieceColor.WHITE:
            return pygame.Color(200, 200, 200)
        case PieceColor.BLACK:
            return pygame.Color(50, 50, 50)
        case _:
            pass


def color2str(pcolor: PieceColor) -> str:
    match pcolor:
        case PieceColor.WHITE:
            return "w"
        case PieceColor.BLACK:
            return "b"
        case _:
            pass


def isValidCell(py: int, px: int) -> bool:
    return py >= 0 and py < BOARD_SIZE[1] and px >= 0 and px < BOARD_SIZE[0]


def isSameColors(first: PieceColor, second: PieceColor) -> bool:
    return first == second


def getOppositeColor(col: PieceColor) -> PieceColor:
    match col:
        case PieceColor.WHITE:
            return PieceColor.BLACK
        case PieceColor.BLACK:
            return PieceColor.WHITE
        case _:
            pass


class Piece:
    def __init__(self):
        raise NotImplementedError("Unimplemented piece")

    def getMoves(self, position: list, currCell: tuple) -> list:
        raise NotImplementedError("Unimplemented piece")

    def draw(self, display, pos: tuple):
        (py, px) = pos
        display.blit(self.image, (px * CELL_SIZE, py * CELL_SIZE))


# cell without piece
class EmptyCell(Piece):
    def __init__(self):
        pass

    def draw(self, display, pos: tuple):
        pass


class Pawn(Piece):
    def __init__(self, color: PieceColor):
        self.color = color
        strColor = color2str(color)
        image = pygame.image.load(f"sprites/{strColor}P.png")
        self.image = pygame.transform.scale(image, PIECE_IMAGE_SIZE)

    def getMoves(self, position: list, currCell: tuple) -> list:
        (py, px) = currCell
        direction = self.getDirection()

        res = list()

        # push move
        new_py = py + direction
        if isinstance(position[new_py][px], EmptyCell):
            res.append((new_py, px))

        # take moves
        for new_py, new_px in [(py + direction, px + 1), (py + direction, px - 1)]:
            if not isValidCell(new_py, new_px):
                continue
            if isinstance(position[new_py][new_px], EmptyCell):
                continue
            if isSameColors(self.color, position[new_py][new_px].color):
                continue

            res.append((new_py, new_px))

        return res

    def getDirection(self) -> int:
        if self.color == PieceColor.WHITE:
            return 1
        else:
            return -1

    # Useless for 3x5 version
    @staticmethod
    def isInitPosition(cell: tuple, direction: int) -> bool:
        print(cell)
        (py, px) = cell
        if direction == 1:
            return py == 1
        else:
            return py == (BOARD_SIZE[1] - 2)


class King(Piece):
    def __init__(self, color: PieceColor):
        self.color = color
        strColor = color2str(color)
        image = pygame.image.load(f"sprites/{strColor}K.png")
        self.image = pygame.transform.scale(image, PIECE_IMAGE_SIZE)


class Knight(Piece):
    def __init__(self, color: PieceColor):
        self.color = color
        strColor = color2str(color)
        image = pygame.image.load(f"sprites/{strColor}N.png")
        self.image = pygame.transform.scale(image, PIECE_IMAGE_SIZE)


class Bishop(Piece):
    def __init__(self, color: PieceColor):
        self.color = color
        strColor = color2str(color)
        image = pygame.image.load(f"sprites/{strColor}B.png")
        self.image = pygame.transform.scale(image, PIECE_IMAGE_SIZE)


pieceImgs = [
    [
        pygame.image.load(f"sprites/wK.png"),
        pygame.image.load(f"sprites/wP.png"),
        pygame.image.load(f"sprites/wN.png"),
        pygame.image.load(f"sprites/wB.png"),
    ],
    [
        pygame.image.load(f"sprites/bK.png"),
        pygame.image.load(f"sprites/bP.png"),
        pygame.image.load(f"sprites/bN.png"),
        pygame.image.load(f"sprites/bB.png"),
    ],
]


class DicePannel:
    def __init__(self):
        # 'Dice' button
        smallfont = pygame.font.SysFont("Corbel", 35)
        self.text = smallfont.render("Dice", True, "white")
        self.rect = pygame.Rect((375, 450, 53, 25))

        # rolled dices
        self.values = [0, 0]

        # rolled dices images
        self.images = [pieceImgs[1][0], pieceImgs[0][0]]

    def draw(self, display):
        # draw button
        pygame.draw.rect(display, (123, 123, 123), self.rect)
        display.blit(self.text, self.rect)

        i = 0
        for img in self.images:
            display.blit(img, (360, 250 + i * 100))
            i += 1

    def clicked(self, mx: int, my: int):
        return self.rect.collidepoint((mx, my))

    def roll(self):
        print("Roll!")
        for i in range(len(self.values)):
            self.values[i] = random.randint(0, 3)
            self.images[i] = pieceImgs[i][self.values[i]]

    def getRoll(self) -> list:
        return self.values


class StateMachine:
    def __init__(self, sideToMove: PieceColor):
        self.sideToMove = sideToMove
        self.state = 1  # 0 -- choose piece
        # 1 -- move

    def choose(self):
        print("Choose")
        match self.state:
            case 0:
                self.state = 1
            case 1:
                self.state = 0
            case _:
                raise NotImplementedError("Unimplemented state")

    def move(self):
        print("Move")
        match self.state:
            case 0:
                self.state = 1
            case 1:
                self.state = 0
            case _:
                raise NotImplementedError("Unimplemented state")

        self.sideToMove = getOppositeColor(self.sideToMove)

    def isStartMove(self) -> bool:
        return self.state == 1

    def isChoose(self) -> bool:
        return self.state == 0


class Board:
    def __init__(self):
        # to simplyfy development we use board 3x5
        self.position =
            [[ King(PieceColor.WHITE), Knight(PieceColor.WHITE), Bishop(PieceColor.WHITE)],
            [  Pawn(PieceColor.WHITE), Pawn(PieceColor.WHITE),   Pawn(PieceColor.WHITE)],
            [  EmptyCell(),            EmptyCell(),              EmptyCell()],
            [  Pawn(PieceColor.BLACK), Pawn(PieceColor.BLACK),   Pawn(PieceColor.BLACK)],
            [  King(PieceColor.BLACK), Knight(PieceColor.BLACK), Bishop(PieceColor.BLACK),]
        ]

        self.dice = DicePannel()

        self.currPieceCoord = ()
        self.validMoves = []

        self.state = StateMachine(PieceColor.WHITE)

    def handleClick(self, mx: int, my: int):
        print(f"Wow! You clicked to ({mx}, {my})")

        if cell := self.coord2cell(mx, my):
            self.handleClickToCell(cell)

        if self.dice.clicked(mx, my):
            self.dice.roll()
            return

    def handleDiceButton(self):
        print("Handle dice button")

    def movePiece(self, oldCoord: tuple, newCoord: tuple):
        (oy, ox) = oldCoord
        (ny, nx) = newCoord
        assert isValidCell(oy, ox) and isValidCell(ny, nx)

        piece = self.position[oy][ox]
        assert not isinstance(piece, EmptyCell)

        self.position[oy][ox] = EmptyCell()

        # handle pawn promotion
        if isinstance(piece, Pawn) and (ny == 0 or ny == (BOARD_SIZE[1] - 1)):
            # TODO handle transformation
            piece = Bishop(piece.color)

        self.position[ny][nx] = piece

    def handleClickToCell(self, coord: tuple):
        (py, px) = coord

        if self.state.isStartMove():
            if isinstance(self.position[py][px], EmptyCell):
                return

            piece = self.position[py][px]
            if not isSameColors(self.state.sideToMove, piece.color):
                return

            moves = piece.getMoves(self.position, coord)
            self.validMoves = moves
            self.currPieceCoord = coord

            self.state.choose()
        elif self.state.isChoose():
            if coord not in self.validMoves:
                return

            self.movePiece(self.currPieceCoord, coord)

            # clear valid moves
            self.validMoves = []
            currPieceCoord = ()

            self.state.move()
        else:
            raise NotImplementedError("Unimplemented state")

    @staticmethod
    def coord2cell(x: int, y: int) -> tuple:
        py = int(y // CELL_SIZE)
        px = int(x // CELL_SIZE)

        if py <= BOARD_SIZE[1] - 1 and px <= BOARD_SIZE[0] - 1:
            return (py, px)
        else:
            return None

    def getButtonCollision(self, x: int, y: int) -> Piece:
        return None

    def draw(self, display):
        # Draw button

        for py in range(len(self.position)):
            for px in range(len(self.position[py])):
                # Draw cell
                self.drawBoardCell(display, (py, px))
                # Draw piece
                piece = self.position[py][px]
                piece.draw(display, (py, px))

        self.drawValidMoves(display)

        self.dice.draw(display)

    # TODO: replace with board.png
    def drawBoardCell(self, display, pos: tuple()):
        (py, px) = pos
        if (py + px) % 2 == 0:
            color = pygame.Color(200, 200, 200)
        else:
            color = pygame.Color(100, 100, 100)

        pygame.draw.rect(
            display,
            color,
            pygame.Rect(px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

    def drawValidMoves(self, display):
        if len(self.validMoves) == 0:
            return

        for py, px in self.validMoves:
            pygame.draw.circle(
                display,
                (12, 143, 44),
                ((px + 1 / 2) * CELL_SIZE, (py + 1 / 2) * CELL_SIZE),
                15,
            )

    def isCheckmate(self):
        return False
