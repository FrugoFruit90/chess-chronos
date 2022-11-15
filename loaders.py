from typing import Generator, TextIO, Callable

import chess.pgn
from chess.pgn import ResultT, BaseVisitor, GameBuilder


def pgn_game_generator(pgn_file: TextIO, visitor: Callable[[], BaseVisitor[ResultT]] = GameBuilder) -> \
        Generator[chess.pgn.Game, None, None]:
    while True:
        next_game = chess.pgn.read_game(pgn_file, Visitor=visitor)
        if not next_game:
            break
        yield next_game
