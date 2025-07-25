

class PlayerBoard:
    def __init__(self, board: list[list[int]] = None) -> None:
        # We allow for a premade board, mostly for testing
        self.board = board or [[0] * 3] * 3

    def get_row_score(self, i: int) -> int:
        total_score = 0
        #roll_ct = [self.board[i].count(num) for num in range(1,7)]
        for die_roll in range(1,7):
            roll_ct = self.board[i].count(die_roll)
            # Score contributed by a die roll is the sum of those rolls * the number of rolls
            roll_score = roll_ct * (roll_ct * die_roll)
            total_score += roll_score


        return total_score
    
    def get_total_score(self) -> int:
        total_score = 0
        for row in range(3):
            total_score += self.get_row_score(row)

        return total_score


a = PlayerBoard()

print(a.board)
print(a.get_total_score())