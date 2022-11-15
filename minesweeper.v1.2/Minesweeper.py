import Engine as game


def main() -> None:
    mineSweeper = game.Engine(10, 10)
    mineSweeper.playGame()
    # mineSweeper.UI.master.mainloop()

if __name__ == "__main__":
    main()
