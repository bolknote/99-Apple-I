            .ORG    00280h
            .CPU    6502

ECHO        =       $FFEF
PRBYTE      =       $FFDC
PRHEX       =       $FFE5
MONITOR     =       $FF1F

            SED
            LDA     #$99
LOOP_:
            PHA
            JSR     BOTTLES
            JSR     B_OF_T_WALL
            LDX     #(ENDPASSSTR - STRS - 2) ; ", "
            LDY     #2
            JSR     PRINT
            PLA
            PHA
            JSR     BOTTLES
            JSR     OF_BEER
            JSR     DOT_CR
            JSR     TAKE_ONE_DOWN
            PLA

            SEC
            SBC     #1

            PHA
            JSR     BOTTLES
            JSR     B_OF_T_WALL

            JSR     DOT_CR

            PLA

            CMP     #0
            BNE     LOOP_

            JSR     NO_MORE

            JMP     MONITOR

PRINTNUMBER:         ; in A, use A
            CMP     #$F
            BCS     $+5
            JMP     PRHEX
            JMP     PRBYTE


PRINT_PSTR:          ; in X - offset, use A, Y
            LDY     (STRS),X
            INX
PRINT:               ; in X (offset), Y (len), use A
            LDA     (STRS),X
            JSR     ECHO
            INX
            DEY
            BNE     PRINT
            RTS


BOTTLES:             ; in A, use X, Y
            CMP     #0
            BEQ     NO_
            PHA
            JSR     PRINTNUMBER
            LDX     #3 ; skips len+"NO"
            LDY     #8 ; length of " BOTTLES"
            PLA
            CMP     #1
            BNE     NO_ONE_
            DEY      ; 7 - lenght of " BOTTLE"
NO_ONE_:
            JMP     PRINT

NO_:
            LDX     #0
            JMP     PRINT_PSTR

B_OF_T_WALL:         ; use X, Y, A
            LDX     #(BEERONTHEWALLSTR - STRS)
            JMP     PRINT_PSTR

OF_BEER:             ; use X, Y, A
            LDX     #(BEERONTHEWALLSTR - STRS + 1) ; skips len
            LDY     #8 ; length of " OF BEER"
            JMP     PRINT

DOT_CR:              ; use X, Y, A
            LDX     #(END - STRS - 2) ; "." + CR
            LDY     #2
            JMP     PRINT

TAKE_ONE_DOWN:       ; use X, Y, A
            LDX     #(PASSSTR - STRS)
            JMP     PRINT_PSTR

NO_MORE:             ; use X, Y, A
            LDX     #(ENDSTR - STRS)
            JMP     PRINT_PSTR

STRS:
            .PSTR   "NO BOTTLES"
BEERONTHEWALLSTR:
            .PSTR   " OF BEER ON THE WALL"
PASSSTR:
            .PSTR   "TAKE ONE DOWN AND PASS IT AROUND, "
ENDPASSSTR:

ENDSTR:
            DB      128,"NO MORE BOTTLES OF BEER ON THE WALL, NO MORE BOTTLES OF BEER.",$8D
            DB      "GO TO THE STORE AND BUY SOME MORE, 99 BOTTLES OF BEER ON THE WALL.",$8D
END: