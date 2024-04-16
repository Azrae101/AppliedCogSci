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

// NEW CLASS

class HTMLGrid {
  constructor(grid, sel) {
    this.grid = grid;
    this.el = document.querySelector(sel);
    this.setupBoard();
  }
  setupBoard() {
    this.grid.getBoardWithActiveShape().forEach((row) => {
      const rowDiv = document.createElement("div");
      rowDiv.className = "row";
      row.forEach(() => {
        const squareDiv = document.createElement("div");
        squareDiv.className = "square";
        rowDiv.appendChild(squareDiv);
      });
      this.el.appendChild(rowDiv);
    });
  }

  render() {
    this.grid.getBoardWithActiveShape().forEach((row, i) => {
      row.forEach((square, j) => {
        const squareDiv = this.el.children[i].children[j];
        squareDiv.style.backgroundColor = square.color || "";
      });
    });
  }
}

// NEW CLASS

class Shape {
constructor(definition, color) {
    this.x = 0;
    this.y = 0;
    this.color = color;
    this.definition = definition;
    this.resetDimensions();
    if (Math.random() > .5) this.mirror();
}

mirror() {
    const dims = Array(this.height).fill("").map(() => Array(this.width).fill(false))
    for (let i = this.width - 1; i >= 0; i--) {
        for (let j = 0; j < this.height; j++) {
            dims[j][this.width - 1 - i] = this.definition[j][i]
        }
    }
    this.definition = dims
    this.resetDimensions();
}

resetDimensions() {
    this.width = this.definition[0] ? this.definition[0].length : 1;
    this.height = this.definition.length;
}

static square(color) {
    return new Shape(
        Array(2)
            .fill("")
            .map((x) => Array(2).fill(true)),
        color
    );
}

static letterL(color) {
    const arr = Array(3)
        .fill("")
        .map((x) => Array(2).fill(""));
    arr[2][0] = arr[2][1] = arr[1][0] = arr[0][0] = true;
    return new Shape(arr, color);
}

static stick(color) {
    return new Shape(Array(4).fill([true]), color);
}

static singleHump(color) {
    const arr = Array(3)
        .fill("")
        .map((x) => Array(2).fill(false));
    arr[0][0] = arr[1][0] = arr[2][0] = arr[1][1] = true;
    return new Shape(arr, color);
}

static letterN(color) {
    const arr = Array(3)
        .fill("")
        .map((x) => Array(2).fill(false));
    arr[0][0] = arr[1][0] = arr[1][1] = arr[2][1] = true;
    return new Shape(arr, color);
}

static random() {
    const randomColor = () => Math.ceil(Math.random() * 255);
    const shapes = ["letterN", "stick", "singleHump", "letterL", "square"];
    const shape = shapes[Math.floor(Math.random() * shapes.length)];
    const color = `rgb(${randomColor()}, ${randomColor()}, ${randomColor()})`;
    return this[shape](color);
}
}


// New class

class Tetris {
  constructor() {
    this.grid = new Grid();
    this.screen = new HTMLGrid(this.grid, "#grid");
    this.previewGrid = new Grid(4, 4);
    this.previewSection = new HTMLGrid(this.previewGrid, "#preview");
    this.TICK_TIME = 300;
    this.gameOver = false;
    this.lines = 0;
    this.isPaused = false;
    this.updatePoints();

    // document.addEventListener("keydown", (e) => this.handleKeypress(e));
    // document
    //   .getElementById("restart")
    //   .addEventListener("click", (e) => this.restart(e));
    // document.getElementById("pause").addEventListener("click", (e) => {
    //   this.isPaused = !this.isPaused;
    // });

    this.render();
    this.setupPreview();
    this.addPiece();

    this.tick();
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
    this.setupPreview();
    this.addPiece();
  }

  setupPreview() {
    this.previewShape = Shape.random();
    this.updatePreview();
  }

  addPiece() {
    this.currentShape = this.previewShape;
    this.previewShape = Shape.random();
    this.updatePreview();
    this.grid.setActiveShape(this.currentShape);
  }

  updatePreview() {
    this.previewGrid.fullReset();
    this.previewGrid.addShapeToGrid(this.previewShape);
    this.previewSection.render();
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

const game = new Tetris();
