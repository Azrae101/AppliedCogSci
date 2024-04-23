
function generateRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

const list_of_display = ["Question A", "Question B", "Question C", "Question D"];

  class Grid {
 
  constructor(width = 10, height = 20) {
      this.width = width;
      this.height = height;
      this.board = null;
      this.activeShape = null;
      this.fullReset();
    }

    fullReset() {
      this.activeShape = null;
      this.resetGrid();
    }
  
    resetGrid() {
      this.board = Array.from({ length: this.height }, () =>
        Array(this.width).fill("")
      );
    }
  
    setActiveShape(shape) {
      shape.x = Math.max(Math.floor(Math.random() * 10) - shape.width, 0);
      shape.y = -shape.height - 1;
      this.activeShape = shape;
    }
  
    detectTetris() {
      var badRows = [];
      for (let i = this.board.length - 1; i >= 0; i--) {
        if (this.board[i].every((x) => x)) {
          badRows.push(i);
        }
      }
      if (badRows.length) {
        badRows.forEach((i) => {
          this.board.splice(i, 1);
          this.board.unshift(Array(this.width).fill(false));
        });
        return true;
      }
      return false;
    }
  
    getBoardWithActiveShape() {
      const grid = Array(this.height)
        .fill("")
        .map((a, i) => [...this.board[i]]);
  
      if (this.activeShape && !this.activeShape.collided) {
        this.addShapeToGrid(this.activeShape, grid);
      }
  
      this.highlightActiveColumns(this.activeShape, grid);
  
      return grid;
    }
  
    highlightActiveColumns(shape, grid) {
      if (!shape) return;
      for (let j = shape.x; j < shape.x + shape.width; j++) {
        for (let i = 0; i < grid.length; i++) {
          if (!grid[i][j]) {
            grid[i][j] = { color: "#333" };
          } else if (grid[i][j] !== shape) {
            break;
          }
        }
      }
    }
  
    // permanently add any shape to the grid
    addShapeToGrid(shape, grid = this.board) {
      if (!shape) return;
      shape.definition.forEach((row, i) => {
        row.forEach((sqr, j) => {
          let [nx, ny] = [shape.x + j, shape.y + i];
          if (ny < 0) return;
          if (sqr) grid[ny][nx] = shape;
        });
      });
    }
  
    handleCollision() {
      this.activeShape.collided = true;
      if (this.activeShape.collided) {
        this.addShapeToGrid(this.activeShape);
      }
    }
  
    willCollide(shape, [x, y]) {
      // hits the bottom
      if (shape.height + y > this.height) {
        return true;
      }
  
      // hits the left wall or the right wall
      if (x < 0 || x > this.width - shape.width) return true;
  
      // hits another shape out there somewhere
      for (let i = 0; i < shape.height; i++) {
        for (let j = 0; j < shape.width; j++) {
          if (!shape.definition[i][j]) continue;
          const [ny, nx] = [y + i, x + j];
          if (ny < 0) continue;
          const match = this.board[ny][nx];
          if (match && match !== shape) {
            if (ny === 0) return "end";
            return true;
          }
        }
      }
  
      // loop over each point in the shape
      return false;
    }
  }

  class HTMLGrid {
    constructor(grid, sel) {
        this.grid = grid;
        this.el = document.querySelector(sel);
        this.setupBoard();
    }

    setupBoard() {
        const canvasWidth = 50; // Desired canvas width in em
        const squareWidth = this.el.offsetWidth / this.grid.width; // Calculate the width of each square based on the current width of the grid

        this.el.style.width = canvasWidth + "em"; // Set the width of the canvas

        this.grid.getBoardWithActiveShape().forEach((row, i) => {
            const rowDiv = document.createElement("div");
            rowDiv.className = "row";
            row.forEach((square, j) => {
                const squareDiv = document.createElement("div");
                squareDiv.className = "square";
                squareDiv.style.width = squareWidth + "px"; // Set the width of each square dynamically
                squareDiv.style.height = squareWidth + "px"; // Set the height of each square dynamically
                if (square) {
                    squareDiv.style.backgroundColor = square.color || "";
                    squareDiv.style.border = "1px solid transparent"; // Initially, set border to transparent
                    if (square.highlighted) {
                        squareDiv.style.border = "1px solid black"; // Add border when highlighted
                    }
                    const text = document.createElement("p"); // Create a paragraph element for the text
                    const randomIndex = Math.floor(Math.random() * questions.length); // Generate a random index for questions array
                    text.innerText = questions[randomIndex].question; // Set text content to a random question
                    squareDiv.appendChild(text); // Append text to the square

                    // Add event listener to check answer when clicked
                    squareDiv.addEventListener("click", () => {
                        const userAnswer = prompt("Answer the question: " + questions[randomIndex].question);
                        const correctAnswer = questions[randomIndex].answer;
                        if (userAnswer && userAnswer.toLowerCase() === correctAnswer.toLowerCase()) {
                            alert("Correct!");
                            fetchNextQuestion(); // Fetch the next question if the answer is correct
                        } else {
                            alert("Incorrect. Try again!");
                        }
                    });
                }
                rowDiv.appendChild(squareDiv);
            });
            this.el.appendChild(rowDiv);
        });
    }

    render() {
        const grid = this.grid.getBoardWithActiveShape();
        for (let i = 0; i < grid.length; i++) {
            const row = grid[i];
            for (let j = 0; j < row.length; j++) {
                const square = row[j];
                const squareDiv = this.el.children[i].children[j];
                if (square) {
                    squareDiv.style.backgroundColor = square.color || "";
                    squareDiv.style.border = "1px solid transparent"; // Initially, set border to transparent
                    if (square.highlighted) {
                        squareDiv.style.border = "1px solid black"; // Add border when highlighted
                    }
                } else {
                    squareDiv.style.backgroundColor = "";
                    squareDiv.style.border = ""; // Remove border if no shape
                }
            }
        }
    }
}

  class Shape {
    constructor(definition, color) {
      this.x = 0;
      this.y = 0;
      this.color = color;
      this.definition = definition;
      this.resetDimensions();
      if (Math.random() > 0.5) this.mirror();
    }
  
    mirror() {
      const dims = Array(this.height)
        .fill("")
        .map(() => Array(this.width).fill(false));
      for (let i = this.width - 1; i >= 0; i--) {
        for (let j = 0; j < this.height; j++) {
          dims[j][this.width - 1 - i] = this.definition[j][i];
        }
      }
      this.definition = dims;
      this.resetDimensions();
    }
  
    resetDimensions() {
      this.width = this.definition[0] ? this.definition[0].length : 1;
      this.height = this.definition.length;
    }
  
    static square(color) {
      return new Shape(
        [
          [true, true],
          [true, true],
        ],
        color
      );
    }
  
    static rect3x2(color) {
      return new Shape(
        [
          [true, true, true],
          [true, true, true],
        ],
        color
      );
    }
  
    static rect4x2(color) {
      return new Shape(
        [
          [true, true, true, true],
          [true, true, true, true],
        ],
        color
      );
    }
  
    static rect5x2(color) {
      return new Shape(
        [
          [true, true, true, true, true],
          [true, true, true, true, true],
        ],
        color
      );
    }
  
    static random() {
      const colors = [generateRandomColor(), generateRandomColor(), generateRandomColor(), generateRandomColor(), generateRandomColor()];
      const shapes = ["rect3x2", "rect4x2", "rect5x2", "square"];
      const shape = shapes[Math.floor(Math.random() * shapes.length)];
      const color = colors[Math.floor(Math.random() * colors.length)];
      return this[shape](color);
  }
}
  
  class Tetris {
    constructor() {
      this.grid = new Grid();
      this.screen = new HTMLGrid(this.grid, "#grid");
      this.TICK_TIME = 100; // FALL TIME!!!
      this.gameOver = false;
      this.lines = 0;
      this.isPaused = false;
      this.updatePoints();
  
      this.render();
      this.addPiece();
  
      this.tick();

        document.getElementById("userInput").addEventListener("keydown", function(event) {
          if (event.key === "Enter") {
              event.preventDefault(); // Prevent the default Enter key behavior (e.g., submitting a form)
              this.value = ""; // Reset the input field value
          }
      });

    }

    restart() {
      this.isPaused = false;
      this.lines = 0;
      this.grid.fullReset();
      if (this.gameOver) {
        document.getElementById("gameMessage").classList.add("hidden");
        this.gameOver = false;
        this.tick();
      }
      this.updatePoints();
      this.addPiece();
    }
  
    addPiece() {
      this.currentShape = Shape.random();
      this.grid.setActiveShape(this.currentShape);
    }
  
    render() {
      this.screen.render();
      requestAnimationFrame(() => this.render());
    }
  
    tick() {
      if (!this.isPaused) {
        if (this.gameOver) {
          document.getElementById("gameMessage").classList.remove("hidden");
          return;
        }
        if (this.currentShape.collided) {
          this.addPiece();
        } else {
          this.movePieceDown();
        }
        if (this.grid.detectTetris()) {
          this.lines += 1;
          this.updatePoints();
        }
      }
      setTimeout(() => this.tick(), this.TICK_TIME);
    }
  
    updatePoints() {
      const lines = document.getElementById("lines");
      lines.innerHTML = this.lines;
    }
  
    movePieceDown() {
      const shape = this.currentShape;
      const crash = this.grid.willCollide(shape, [shape.x, shape.y + 1]);
      if (crash) {
        if (crash === "end") {
          this.gameOver = true;
        }
        this.grid.handleCollision();
      } else {
        shape.y += 1;
      }
    }
  }

  let questions = [
    {"question": "Question 1", "answer": "1"},
    {"question": "Question 2", "answer": "2"},
    {"question": "Question 3", "answer": "3"},
    {"question": "Question 4", "answer": "4"}
  ];

  const game = new Tetris();  
  