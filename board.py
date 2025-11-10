LIGHT_GREEN = "\033[92m"
GREEN = "\033[32m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def drawBoard(players, cBoard):
    def a(pos):
        for p in players:
            if pos == p[4]:
                if len(str(pos)) > 1:
                    return " " + str(p[2])
                return str(p[2])
        return str(pos)

    if cBoard == "snake":
        board = [
            [( "                                                                                                    @@", LIGHT_GREEN)],
            [( "                                                                                                    @@", LIGHT_GREEN)],
            [( "                                                                                                    @@", LIGHT_GREEN)],
            [( "                                                                                                    @@@@@@@", LIGHT_GREEN)],
            [( "                                                                                                   @@", LIGHT_GREEN)],
            [( "                                                                                        @@@@@@@@@@@@", LIGHT_GREEN)],
            [( "                                                                                 @@@@@@@@@     -@@@", LIGHT_GREEN)],
            [( "                                                                               @@@                @", LIGHT_GREEN)],
            [( "                         @@@@@@@@@@@@@@@+                                    :@@                  @@", LIGHT_GREEN)],
            [( "                    @@@@@@  @        @ @@@@@@                                @@      @@@          @@", LIGHT_GREEN)],
            [( "                 @@@@        @  ", LIGHT_GREEN), (a(34), RED), ("  @      @ @@@@%                           @@     @@            @@", LIGHT_GREEN)],
            [( "               @@@   @@   ", LIGHT_GREEN), (a(33), RED), ("  @    @  ", LIGHT_GREEN), (a(35), RED), ("   @     @@@@@                       @@             @     @@", LIGHT_GREEN)],
            [( "             @@        @@@    @    @      @@      @  @@@@@                   @@            @@     @", LIGHT_GREEN)],
            [( "           @@@ @@   ", LIGHT_GREEN), (a(32), RED), ("    @    @  @       @  ", LIGHT_GREEN), (a(36), RED), ("   @      @@@@@               @     ", LIGHT_GREEN), (a(43), RED), ("     @@     @@", LIGHT_GREEN)],
            [( "          @@     @@@       @@@@@@@@@@@-  @       @  ", LIGHT_GREEN), (a(37), RED), ("  @    @@@@@@@@     @@@                   @@", LIGHT_GREEN)],
            [( "         @@    ", LIGHT_GREEN), (a(31), RED), ("   @  @@@@            @@@@@   @@      @     @     @ @@@@@   @@               @@@", LIGHT_GREEN)],
            [( "         @@@@@@      @@@                   @@@@       @ ", LIGHT_GREEN), (a(38), RED), ("  @     @   @   @    @      @@@@@@@@@", LIGHT_GREEN)],
            [( "        @@     @@@@ @@                         @@@+  @     @  ", LIGHT_GREEN), (a(39), RED), (" @    @   @     @    @@", LIGHT_GREEN)],
            [( "        @.  ", LIGHT_GREEN), (a(30), RED), ("     @@:                            @@@@    @     @ ", LIGHT_GREEN), (a(40), RED), ("  @    @ ", LIGHT_GREEN), (a(42), RED), ("  @  @@", LIGHT_GREEN)],
            [( "        @       @@@ @@                               @@@@@     @     @  ", LIGHT_GREEN), (a(41), RED), ("  @     @@@", LIGHT_GREEN)],
            [( "        @@   @@@     #@@                                 @@@@ @      @      @   @@@", LIGHT_GREEN)],
            [( "         @@@@       @  @@@@                                  @@@@@@  @       @@@@", LIGHT_GREEN)],
            [( "         @@    ", LIGHT_GREEN), (a(29), RED), ("  @      @@@@@                                   @@@@@@@@@@@", LIGHT_GREEN)],
            [( "          @@      @       @   @@@@@", LIGHT_GREEN)],
            [( "           @@=   @   ", LIGHT_GREEN), (a(28), RED), ("   @      @@@@@@@@", LIGHT_GREEN)],
            [( "            @@@  @       @      @      @@@@@@@@", LIGHT_GREEN)],
            [( "              @@@        @  ", LIGHT_GREEN), (a(27), RED), ("  @      @    @@@@@@@@@@@", LIGHT_GREEN)],
            [( "                @@@@    @      @@  ", LIGHT_GREEN), (a(26), RED), ("  @      @     @@@@@@@@@@@@", LIGHT_GREEN)],
            [( "                   @@@@ @      @      @@      @       @     @@@@@@@@@@@@@", LIGHT_GREEN)],
            [( "                      @@@@@    @      @   ", LIGHT_GREEN), (a(25), RED), (" @@       @      @        @@@@@@@@", LIGHT_GREEN)],
            [( "                          @@@@@       @      @   ", LIGHT_GREEN), (a(24), RED), ("  @       @       @       @@@@@", LIGHT_GREEN)],
            [( "                              @@@@@@  @      @       @  ", LIGHT_GREEN), (a(23), RED), ("  @   ", LIGHT_GREEN), (a(22), RED), ("  @       @     @@@", LIGHT_GREEN)],
            [( "                                    @@@@@@@  @       @      @       @  ", LIGHT_GREEN), (a(21), RED), ("  @         @@@", LIGHT_GREEN)],
            [( "                                           @@@@@@@@@@@@     @      @      @   ", LIGHT_GREEN), (a(20), RED), ("   @@  @@@", LIGHT_GREEN)],
            [( "                                                       @@@@@@@@@@@@@     @       @@      @@", LIGHT_GREEN)],
            [( "                  @@@@@@@@@@@@@@@                                   @@@@@@     @@   ", LIGHT_GREEN), (a(19), RED), ("    @@", LIGHT_GREEN)],
            [( "               @@@        @      @@@@@                                   @@@@ @          @ @@", LIGHT_GREEN)],
            [( "              @@@     ", LIGHT_GREEN), (a(6), RED), ("   @     @     @@@@                                  @@@      @@@@   @@", LIGHT_GREEN)],
            [( "             @@  @@@     @  ", LIGHT_GREEN), (a(7), RED), ("  @      @  .@@@:                                @@ @@@@        @", LIGHT_GREEN)],
            [( "             @@     @@@  @     @  ", LIGHT_GREEN), (a(8), RED), ("  @     @ @@@@                              @@            @", LIGHT_GREEN)],
            [( "            .@   ", LIGHT_GREEN), (a(5), RED), ("     @ @    @     @  ", LIGHT_GREEN), (a(9), RED), ("  @     @@@@                           @@     ", LIGHT_GREEN), (a(18), RED), ("     @", LIGHT_GREEN)],
            [( "            %@      @@@ @@@@@@@@   @     @ ", LIGHT_GREEN), (a(10), RED), ("  @    @@@@                       @@@           @", LIGHT_GREEN)],
            [( "            +@  @@@@   @@@      @@@@.   @     @      @  @@@@@                @@@  @@        @@", LIGHT_GREEN)],
            [( "             @@@       #@           @@@@    @@  ", LIGHT_GREEN), (a(11), RED), ("  @     @ .@@@@@@@@@@@@@@@@@@     @@@    @@", LIGHT_GREEN)],
            [( "             @@    ", LIGHT_GREEN), (a(4), RED), ("   @@@              @@@@       @ ", LIGHT_GREEN), (a(12), RED), ("  @      @    @    @    @       @@ @@", LIGHT_GREEN)],
            [( "              @@     @@  @@                @@@@   @     @  ", LIGHT_GREEN), (a(13), RED), ("  @     @     @    @  ", LIGHT_GREEN), (a(17), RED), ("    @@", LIGHT_GREEN)],
            [( "               @@ @@@@    @@@@                @@@@@    @      @  ", LIGHT_GREEN), (a(14), RED), ("  @ ", LIGHT_GREEN), (a(15), RED), ("  @ ", LIGHT_GREEN), (a(16), RED), ("  @     @@@", LIGHT_GREEN)],
            [( "                @@@    ", LIGHT_GREEN), (a(3), RED), ("     @@@@                 @@@@@@     @      @      @      @  @@@@", LIGHT_GREEN)],
            [( "                  @@       @@   @@@@                 %@@@@@  @      @       @      @@@@", LIGHT_GREEN)],
            [( "                    @@@  @@   ", LIGHT_GREEN), (a(2), RED), ("   @@@@@@                  @@@@@@@%   @        @@@@@@", LIGHT_GREEN)],
            [( "                      @@@@       @@@   @@                       @@@@@@@@@@@@@@@", LIGHT_GREEN)],
            [( "                         @@@@  @@@   ", LIGHT_GREEN), (a(1), RED), ("  @@@", LIGHT_GREEN)],
            [( "                            @@@@@         @@", LIGHT_GREEN)],
            [( "                                 @@@@@    @@", LIGHT_GREEN)],
            [( "                                      @@@@@", LIGHT_GREEN)],
        ]
    elif cBoard == "neo":
        board = [
            [("                                                    @                                                     ", YELLOW)],
            [("                                                   @ @                                                    ", YELLOW)],
            [("                                                  @   @                                                   ", YELLOW)],
            [("                                                 @     @                                                  ", YELLOW)],
            [("                                           @@@@@@  " + CYAN + str(a(45)) + YELLOW + "   @@@@@@                                            ", YELLOW)],
            [("                                             @@@@       @@@@                                              ", YELLOW)],
            [("                                                 @  @  @                                                  ", YELLOW)],
            [("                                                @  @ @  @                                                 ", YELLOW)],
            [("                                               @  @   @  @                                                ", YELLOW)],
            [("                                              @   @   @   @                                               ", YELLOW)],
            [("                                   @@@       @   @     @   @        @@@                                   ", YELLOW)],
            [("                              @@@@@   @@@@   @  @  " + CYAN + str(a(44)) + YELLOW + "   @  @   @@@@@  @@@@@@                              ", YELLOW)],
            [("                           @@@            @@@@ @    @    @ @@@@             @@                            ", YELLOW)],
            [("                         @@     " + CYAN + str(a(32)) + YELLOW + "  @@@@@@@@@  @   @ @   @  @@@@@@@@@  " + CYAN + str(a(43)) + YELLOW + "     @@                          ", YELLOW)],
            [("                        @    " + CYAN + str(a(31)) + YELLOW + "   @@         @@   @   @   @@         @@   " + CYAN + str(a(42)) + YELLOW + "    @                         ", YELLOW)],
            [("                       @         @   @@@@@@@      @   @     @@@@@@@   @         @                        ", YELLOW)],
            [("                       @       @@  @@       @@@  @     @  @@@       @@  @@       @                        ", YELLOW)],
            [("                       @  " + CYAN + str(a(30)) + YELLOW + "  @   @    " + CYAN + str(a(33)) + YELLOW + "      @@       @@      " + CYAN + str(a(39)) + YELLOW + "    @   @  " + CYAN + str(a(41)) + YELLOW + "  @                        ", YELLOW)],
            [("                       @      @   @                                   @   @      @                        ", YELLOW)],
            [("                       @      @   @    " + CYAN + str(a(34)) + YELLOW + "                       " + CYAN + str(a(38)) + YELLOW + "    @   @      @                        ", YELLOW)],
            [("                       @  " + CYAN + str(a(29)) + YELLOW + "  @   @        " + CYAN + str(a(35)) + YELLOW + "      " + CYAN + str(a(36)) + YELLOW + "       " + CYAN + str(a(37)) + YELLOW + "        @   @  " + CYAN + str(a(40)) + YELLOW + "  @                        ", YELLOW)],
            [("                        @     @    @                                  @   @     @                         ", YELLOW)],
            [("                         @@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@                          ", YELLOW)],
            [("               @@@                                                                                        ", YELLOW)],
            [("               @  @@     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      @@@@@                ", YELLOW)],
            [("                @   @@   @                          " + CYAN + str(a(28)) + YELLOW + "                        @    @@    @                ", YELLOW)],
            [("                @    @   @     " + CYAN + str(a(10)) + YELLOW + "    " + CYAN + str(a(11)) + YELLOW + "    " + CYAN + str(a(12)) + YELLOW + "   " + CYAN + str(a(13)) + YELLOW + "      " + CYAN + str(a(14)) + YELLOW + "   " + CYAN + str(a(15)) + YELLOW + "   " + CYAN + str(a(16)) + YELLOW + "   " + CYAN + str(a(17)) + YELLOW + "     @    @    @                 ", YELLOW)],
            [("                @    @   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @    @                 ", YELLOW)],
            [("                 @@  @                                                             @  @@                  ", YELLOW)],
            [("                   @@ @ " + RED + "  @@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@ " + YELLOW + "  @@@                    ", YELLOW)],
            [("                     @@ " + RED + "  @     " + CYAN + str(a(9)) + RED + "     @   @         " + CYAN + str(a(27)) + RED + "         @   @    " + CYAN + str(a(18)) + RED + "    @ " + YELLOW + "  @@                      ", YELLOW)],
            [("           @@@@@@@   @@  " + RED + " @           @   @                   @   @           @ " + YELLOW + "  @@   @@@@@@@            ", YELLOW)],
            [("             @@   @@ @ @ " + RED + " @     " + CYAN + str(a(8)) + RED + "      @   @@       " + CYAN + str(a(26)) + RED + "       @   @     " + CYAN + str(a(19)) + RED + "     @ " + YELLOW + " @ @ @@   @@              ", YELLOW)],
            [("               @@@@@@@ @  " + RED + " @            @    @@@          @@@    @           @  " + YELLOW + " @ @@@@@@@                ", YELLOW)],
            [("                      @ @ " + RED + " @      " + CYAN + str(a(7)) + RED + "      @      @@@@@@@@@@     @@     " + CYAN + str(a(20)) + RED + "     @ " + YELLOW + " @ @                       ", YELLOW)],
            [("                       @ @ " + RED + " @@            @@@               @@@             @ " + YELLOW + "  @ @                       ", YELLOW)],
            [("                       @ @  " + RED + "  @     " + CYAN + str(a(6)) + RED + "        @@@         @@@       " + CYAN + str(a(21)) + RED + "      @ " + YELLOW + "  @ @                        ", YELLOW)],
            [("                        @ @@ " + RED + " @@                @@@@@@@@@                @@ " + YELLOW + "  @ @                         ", YELLOW)],
            [("                         @  @  " + RED + " @      " + CYAN + str(a(5)) + RED + "                        " + CYAN + str(a(22)) + RED + "      @  " + YELLOW + " @@ @                          ", YELLOW)],
            [("               @@@@@@@@@@    @@ " + RED + " @@@       " + CYAN + str(a(4)) + RED + "       " + CYAN + str(a(25)) + RED + "      " + CYAN + str(a(23)) + RED + "        @@@  " + YELLOW + " @    @@@@@@@@@@                ", YELLOW)],
            [("                 @@@@@@@@@@@@  @  " + RED + "  @@          " + CYAN + str(a(3)) + RED + "      " + CYAN + str(a(24)) + RED + "          @@  " + YELLOW + "  @@ @@@@@@@@@@@@                  ", YELLOW)],
            [("                             @@ @@@  " + RED + " @@@@          " + CYAN + str(a(2)) + RED + "          @@@@  " + YELLOW + "  @@  @                              ", YELLOW)],
            [("                               @@  @@   " + RED + "  @@@@@@@@     @@@@@@@@   " + YELLOW + "  @@@  @@                               ", YELLOW)],
            [("                                 @@  @@@    " + RED + "      @@@@@     " + YELLOW + "     @@@  @@@                                 ", YELLOW)],
            [("                                   @    @@@@@               @@@@@    @                                    ", YELLOW)],
            [("                              @@@@@  @@@@@   @@@@@@@@@@@@@@@   @@@@@  @@@@@                               ", YELLOW)],
            [("                            @@@@@ @@@     @@@@@@         @@@@@@     @@@ @@@@@                             ", YELLOW)],
            [("                                 @              @   " + CYAN + str(a(1)) + YELLOW + "   @              @                                  ", YELLOW)],
            [("                                                 @     @                                                  ", YELLOW)],
            [("                                                  @   @                                                   ", YELLOW)],
            [("                                                  @   @                                                   ", YELLOW)],
            [("                                                  @   @                                                   ", YELLOW)],
            [("                                                   @ @                                                    ", YELLOW)],
            [("                                                    @                                                     ", YELLOW)],
            [("                                                    @                                                     ", YELLOW)],
        ]

    colored_board = ""
    for line in board:
        for segment, color in line:
            colored_board += color + segment
        colored_board += RESET + "\n"
    board = colored_board
    
    return board