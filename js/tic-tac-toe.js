/*
 * Tic Tac Toe
 *
 * An AI-driven Tic Tac Toe game in HTML/JavaScript/CSS.
 *
 * @author: Vasanth Krishnamoorthy, Marco Tompitak
 *
 * Adapted from https://github.com/vasanthk/tic-tac-toe-js
 */

var N_SIZE = 3,
    EMPTY = " ",
    boxes = [],
    turn = "X",
    score,
    moves,
    game_active = true;

/*
 * Initializes the Tic Tac Toe board and starts the game.
 */
function init() {
    var board = document.createElement('table');
    board.setAttribute("border", 1);
    board.setAttribute("cellspacing", 0);

    var identifier = 1;
    for (var i = 0; i < N_SIZE; i++) {
        var row = document.createElement('tr');
        board.appendChild(row);
        for (var j = 0; j < N_SIZE; j++) {
            var cell = document.createElement('td');
            cell.class = 'square'
            cell.name = i * N_SIZE + j
            cell.setAttribute('height', 120);
            cell.setAttribute('width', 120);
            cell.setAttribute('align', 'center');
            cell.setAttribute('valign', 'center');
            cell.classList.add('col' + j, 'row' + i);
            if (i == j) {
                cell.classList.add('diagonal0');
            }
            if (j == N_SIZE - i - 1) {
                cell.classList.add('diagonal1');
            }
            cell.identifier = identifier;
            cell.addEventListener("click", set);
            row.appendChild(cell);
            boxes.push(cell);
            identifier += identifier;
        }
    }

    document.getElementById("tictactoe").appendChild(board);
    startNewGame();
}

/*
 * New game
 */
function startNewGame() {
    score = {
        "X": 0,
        "O": 0
    };
    moves = 0;
    turn = "X";
    boxes.forEach(function(square) {
        square.innerHTML = EMPTY;
    });
    document.getElementById('turn').textContent = "You are Player X";
    game_active = true;
}

/*
 * Check if a win or not
 */
function win(clicked) {
    // Get all cell classes
    var memberOf = clicked.className.split(/\s+/);
    for (var i = 0; i < memberOf.length; i++) {
        var testClass = '.' + memberOf[i];
        var items = contains('#tictactoe ' + testClass, turn);
        // winning condition: turn == N_SIZE
        if (items.length == N_SIZE) {
            return true;
        }
    }
    return false;
}

function contains(selector, text) {
    var elements = document.querySelectorAll(selector);
    return [].filter.call(elements, function(element) {
        return RegExp(text).test(element.textContent);
    });
}

/*
 * Sets clicked square and also updates the turn.
 */
function set() {
    if (this.innerHTML !== EMPTY || !game_active) {
        return;
    }
    this.innerHTML = turn;
    moves += 1;
    score[turn] += this.identifier;
    if (win(this)) {
        document.getElementById('turn').textContent = 'Player ' + turn + ' wins!';
        game_active = false;
    } else if (moves === N_SIZE * N_SIZE) {
        document.getElementById('turn').textContent = "It's a draw!";
        game_active = false;
    }
    turn = turn === "X" ? "O" : "X";
    if (turn == "O") {
        ai_move = ai_moves[boardhash()];
        boxes[ai_move].click();
    }
}

/*
 * Calculate the string representation of the current status of the board
 */
function boardhash() {
    status = '';
    for (const c of boxes) {
        status += c.innerHTML;
    }
    return status;
}

init();