import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [board, setBoard] = useState([]);
  const [selected, setSelected] = useState(null);
  const [turn, setTurn] = useState("W");

  const [legalMoves, setLegalMoves] = useState([]);
  const [gameOver, setGameOver] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/start`).then((res) => {
      setBoard(res.data.board);
      setTurn(res.data.turn);
    });
  }, []);

  const handleClick = (r, c) => {
    if (gameOver) return;

    if (!selected) {
      const clicked = board[r][c];
      if (clicked && isWhitePiece(clicked) && turn === "W") {
        setSelected([r, c]);
        axios
          .post(`${process.env.REACT_APP_API_URL}/legal-moves`, { r: [r, c] })
          .then((res) => {
            setLegalMoves(res.data.moves);
          });
      }
    } else {
      const [r1, c1] = selected;
      axios
        .post(`${process.env.REACT_APP_API_URL}/move`, { r1, c1, r2: r, c2: c })
        .then((res) => {
          setBoard(res.data.board);
          setTurn(res.data.turn);
          setGameOver(res.data.gameOver);
          setSelected(null);
          setLegalMoves([]);

          if (res.data.turn === "B" && !res.data.gameOver) {
            setTimeout(() => {
              axios
                .post(`${process.env.REACT_APP_API_URL}/ai-move`)
                .then((res2) => {
                  setBoard(res2.data.board);
                  setTurn(res2.data.turn);
                  setGameOver(res2.data.gameOver);
                });
            }, 400);
          }
        })
        .catch(() => {
          setError("Invalid move! Try a legal one.");
          setTimeout(() => setError(null), 3000);
          setSelected(null);
          setLegalMoves([]);
        });
    }
  };

  const isWhitePiece = (symbol) => {
    return ["♔", "♕", "♖", "♗", "♘", "♙"].includes(symbol);
  };

  return (
    <div className="wrapper">
      <h1>Welcome to Deepthi's chess</h1>
      <button
        onClick={() => {
          axios.get(`${process.env.REACT_APP_API_URL}/start`).then((res) => {
            setBoard(res.data.board);
            setTurn(res.data.turn);
            setGameOver(null);
            setSelected(null);
            setLegalMoves([]);
          });
        }}
        className="reset-button"
      >
        Reset Game
      </button>
      {error && <div className="error-toast">{error}</div>}

      <div className="board">
        {/* overlay */}
        <div className={`overlay ${gameOver ? "active" : ""}`}>
          {gameOver && (
            <div className={`${turn === "W" ? "game-over" : "game-win"}`}>
              {gameOver === "checkmate"
                ? turn === "W"
                  ? "You lost! 💀"
                  : "You won! 🎉"
                : "Stalemate! It's a draw 🤝"}
            </div>
          )}
        </div>
        {board.map((row, rIdx) =>
          row.map((cell, cIdx) => (
            <div
              key={`${rIdx}-${cIdx}`}
              className={`cell ${(rIdx + cIdx) % 2 === 0 ? "light" : "dark"} ${
                legalMoves.some(([lr, lc]) => lr === rIdx && lc === cIdx)
                  ? // ||
                    // (selected?.length > 0 &&
                    //   selected[0] === rIdx &&
                    //   selected[1] === cIdx)
                    "highlight"
                  : ""
              }`}
              onClick={() => handleClick(rIdx, cIdx)}
            >
              {cell !== "." && (
                <span
                  className={`${
                    isWhitePiece(cell) ? "white-piece" : "black-piece"
                  } ${
                    selected?.length > 0 &&
                    selected[0] === rIdx &&
                    selected[1] === cIdx
                      ? "selected-piece"
                      : ""
                  }`}
                >
                  {cell}
                </span>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
