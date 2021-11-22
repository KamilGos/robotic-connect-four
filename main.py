import sources.image_processing as imgproc
import sources.connect_four_heuristic as game



if __name__ == "__main__":
    ImgProc = imgproc.ImageProcessing(1)
    ImgProc.initialize()

    playing = True
    while playing:
        winner = game.playGame(ImgProc)
        if winner == game.COMPUTER_PLAYER:
            print("Damn! You lost!")
        elif winner == game.HUMAN_PLAYER:
            print("Congratulations! You won!")
        else:
            print("The board is full. This is a draw!")

        while True:
            try:
                option = input("Do you want to play again? (Y/N)")
            except ValueError:
                print("Please input a correct value. Try again.")
                continue
            if option == 'Y' or option == 'y':
                break
            elif option == 'N' or option == 'n':
                playing = False
                break
            else:
                print("Please enter Y or N.")
