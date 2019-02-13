%include "include\macros.inc"	
%include "include\2dad.inc"

extern	_GetStdHandle@4
extern	_WriteFile@20
extern	_ExitProcess@4
extern	_ReadFile@20
extern	_GetLastError@0

SECTION	.text

    global	_main	; PE Entry


vm_entry:
    push ebp
    mov ebp, esp
    sub esp, 4
    xor eax, eax
    INDDES_MOV 0x00FB, 0x0008
    MADD 0x00FB, 0x003C
    MOV 0x0049, 0x0059
    INDDES_MOV 0x00FB, 0x0049
    MADD 0x00FB, 0x008D
    MOV 0x009A, 0x00AA
    INDDES_MOV 0x00FB, 0x009A
    MADD 0x00FB, 0x00DE
    jmp lbl_00FC

    lbl_00EB:
    SUB 0x00FB, 0x00F1
    jmp end


    lbl_00FC:

    MOV 0x00FF, 0x00FB
    ADD3 0x0117, 0x00FF , 0x0113
    INDSRC_MOV 0x010F, 0x0117
    ADD3 0x0150, 0x00FF, 0x014C
    INDSRC_MOV 0x0148, 0x0150
    MOV 0x0185, 0x010F
    INDSRC_MOV 0x01AD, 0x185

    lbl_01D2:
    MOV 0x0185, 0x010F
    INDSRC_MOV 0x0181, 0x185
    MOV 0x0211, 0x0181
    SUBJG 0x0211, 0x148, lbl_020B

    lbl_0208:
    ; lbl_0208-020B: JMP lbl_0212
    jmp lbl_0212
    
    
    lbl_020B:
    ; lbl_020B-020E: XOR lbl_0000, lbl_0000
    ; lbl_020E-0211: JMP lbl_04C2
    jmp lbl_04C2

    lbl_0212:
    ; lbl_0211-0212: db C2, E0
    ; lbl_0212-0218: MADD lbl_0185, lbl_0181
    MADD 0x0185, 0x0181
    ; lbl_0218-0224: MOV lbl_022A, lbl_0185
    ; lbl_0224-0230: MOV lbl_0189, lbl_0E6F
    INDSRC_MOV 0x0189, 0x0185
    ; lbl_0230-023C: MOV lbl_0254, lbl_0189
    ; lbl_023C-0245: SUB lbl_0254, lbl_018D; JA lbl_0248
    MOV 0x0254, 0x0189
    SUBJG 0x0254, 0x018D, lbl_0248

    lbl_0245:
    ; lbl_0245-0248: JMP lbl_024E
    jmp lbl_024E

    lbl_0248:
    ; lbl_0248-024E: CMP lbl_0254, 0; JZ lbl_0251
    CMPJZ 0x0254, lbl_0251

    lbl_024E:
    ; lbl_024E-0251: JMP lbl_0255
    jmp lbl_0255

    lbl_0251:
    ; lbl_0251-0254: JMP lbl_04C2
    jmp lbl_04C2

    lbl_0255:
    ; lbl_0254-0255: db 00, 00
    ; lbl_0255-025E: MMOV lbl_0279, lbl_00FB
    ; lbl_025E-026A: MOV lbl_027A, lbl_00FB
    ; lbl_026A-0276: MOV lbl_0280, lbl_00FB
    ; lbl_0276-0282: MOV lbl_00F8, lbl_010F
    INDDES_MOV 0x00FB, 0x010F
    ; lbl_0282-0285: XOR lbl_0000, lbl_0000
    ; lbl_0285-0288: JMP lbl_0289

    MADD 0x00FB, 0x0288
    MOV 0x_0295, 0x_02A5
    INDDES_MOV 0x00FB, 0x_0295
    MADD 0x_00FB, 0x_02D9
    ; lbl_02E0-02E3: XOR lbl_0000, lbl_0000
    ; lbl_02E3-02E6: JMP lbl_0520
    jmp lbl_0520

    lbl_02E6:
    ; lbl_02E6-02E7: db EC, 02
    ; lbl_02E7-02E8: db FB, 00
    ; lbl_02E8-02EB: XOR lbl_0000, lbl_0000
    ; lbl_02EB-02EC: db ED, 02
    SUB 0x00FB, 0x02EC
    ADD3 0x0185, 0x019D, 0x010F
    ; lbl_02FF-030B: MOV lbl_0311, lbl_0185
    ; lbl_030B-0317: MOV lbl_01A1, lbl_07FC
    INDSRC_MOV 0x01A1, 0x0185
    ; lbl_0317-0323: MOV lbl_0338, lbl_01A1
    MOV 0x0338, 0x01A1
    ; lbl_0323-032C: SUB lbl_0338, lbl_01A5; JA lbl_032F
    SUBJG 0x0338, 0x01A5, lbl_032F

    lbl_032C:
    ; lbl_032C-032F: JMP lbl_0335
    jmp lbl_0335

    lbl_032F:
    ; lbl_032F-0335: CMP lbl_0338, 0; JZ lbl_0339
    CMPJZ 0x0338, lbl_0339

    lbl_0335:
    ; lbl_0335-0338: JMP lbl_03E2
    jmp lbl_03E2

    lbl_0339:
    ; lbl_0338-0339: db FF, FF
    ; lbl_0339-0342: MMOV lbl_035D, lbl_0185
    ; lbl_0342-034E: MOV lbl_035E, lbl_0185
    ; lbl_034E-035A: MOV lbl_0364, lbl_0185
    ; lbl_035A-0366: MOV lbl_07FC, lbl_01A9
    INDDES_MOV 0x0185, 0x01A9
    ; lbl_0366-0372: MOV lbl_0185, lbl_010F
    MOV 0x0185, 0x010F
    ; lbl_0372-0375: XOR lbl_0000, lbl_0000
    ; lbl_0375-037B: MADD lbl_0185, lbl_0195
    MADD 0x0185, 0x0195
    ; lbl_037B-0387: MOV lbl_038D, lbl_0185
    ; lbl_0387-0393: MOV lbl_01A1, lbl_07FA
    INDSRC_MOV 0x01A1, 0x0185
    ; lbl_0393-039F: MOV lbl_0002, lbl_01A1
    MOV 0x0002, 0x01A1
    ; lbl_039F-03AB: MOV lbl_0004, lbl_03B1
    MOV 0x0004, 0x03B1
    HANDLE_OUTPUT

    INDDES_MOV 0x0185, 0x01A9
    lbl_03E2:
    ; lbl_03DF-03EB: MOV lbl_0185, lbl_010F
    MOV 0x0185, 0x010F
    ; lbl_03EB-03EE: XOR lbl_0000, lbl_0000
    ; lbl_03EE-03F4: MADD lbl_0185, lbl_0199
    MADD 0x0185, 0x0199
    ; lbl_03F4-0400: MOV lbl_0406, lbl_0185
    ; lbl_0400-040C: MOV lbl_01A1, lbl_07FB
    INDSRC_MOV 0x01A1, 0x0185
    ; lbl_040C-0418: MOV lbl_042D, lbl_01A1
    ; lbl_0418-0421: SUB lbl_042D, lbl_01A5; JA lbl_0424
    MOV 0x042D, 0x01A1
    SUBJG 0x042D, 0x01A5, lbl_0424

    lbl_0421:
    ; lbl_0421-0424: JMP lbl_042A
    jmp lbl_042A

    lbl_0424:
    ; lbl_0424-042A: CMP lbl_042D, 0; JZ lbl_042E
    CMPJZ 0x042D, lbl_042E

    lbl_042A:
    ; lbl_042A-042D: JMP lbl_04BF
    jmp lbl_04BF

    lbl_042E:
    ; lbl_042D-042E: db FF, FF
    ; lbl_042E-0437: MMOV lbl_0452, lbl_0185
    ; lbl_0437-0443: MOV lbl_0453, lbl_0185
    ; lbl_0443-044F: MOV lbl_0459, lbl_0185
    ; lbl_044F-045B: MOV lbl_0000, lbl_01A9
    INDDES_MOV 0x0185, 0x01A9
    ; lbl_045B-0467: MOV lbl_0003, lbl_046D
    MOV 0x0003, 0x046D

    MOV 0x01A1, 0x0001
    ; lbl_0477-0483: MOV lbl_0185, lbl_010F
    MOV 0x0185, 0x010F
    ; lbl_0483-0486: XOR lbl_0000, lbl_0000
    ; lbl_0486-048C: MADD lbl_0185, lbl_0191
    MADD 0x0185, 0x0191
    ; lbl_048C-0498: MOV lbl_04B3, lbl_0185
    ; lbl_0498-04A4: MOV lbl_04B4, lbl_0185
    ; lbl_04A4-04B0: MOV lbl_04BA, lbl_0185
    ; lbl_04B0-04BC: MOV lbl_0000, lbl_01A1
    INDDES_MOV 0x0185, 0x01A1
    ; lbl_04BC-04BF: XOR lbl_0000, lbl_0000

    lbl_04BF:
    ; lbl_04BF-04C2: JMP lbl_01D2
    jmp lbl_01D2

    lbl_04C2:
    ; lbl_04C2-04CB: MMOV lbl_0185, lbl_010F
    MOV 0x0185, 0x010F
    ; lbl_04CB-04D7: MOV lbl_04F2, lbl_0185
    ; lbl_04D7-04E3: MOV lbl_04F3, lbl_0185
    ; lbl_04E3-04EF: MOV lbl_04F9, lbl_0185
    ; lbl_04EF-04FB: MOV lbl_07F6, lbl_01AD
    INDDES_MOV 0x0185, 0x01AD

    SUB 0x00FB, 0x0501
    ; lbl_0505-050E: MMOV lbl_0514, lbl_00FB
    ; lbl_050E-051A: MOV lbl_051F, lbl_00F7
    ; lbl_051A-051D: XOR lbl_0000, lbl_0000
    ; lbl_051D-0520: JMP lbl_00EB
    INDJMP2 0x00FB

    lbl_0520:

    MOV 0x0523, 0x00FB


    ADD3 0x053B, 0x0523 , 0x0537
    ; lbl_054E-055A: MOV lbl_0560, lbl_053B
    ; lbl_055A-0566: MOV lbl_0533, lbl_00F8
    INDSRC_MOV 0x0533, 0x053B
    ; lbl_0566-0572: MOV lbl_07F1, lbl_0533
    MOV 0x07F1, 0x0533
    ; lbl_0572-057E: MOV lbl_0584, lbl_07F1
    ; lbl_057E-058A: MOV lbl_07F5, lbl_07F6
    INDSRC_MOV 0x07F5, 0x07F1
    ; lbl_058A-058D: XOR lbl_0000, lbl_0000
    ; lbl_058D-0593: MADD lbl_07F1, lbl_07F5
    MADD 0x07F1, 0x07F5
    ; lbl_0593-059F: MOV lbl_05A5, lbl_07F1
    ; lbl_059F-05AB: MOV lbl_07EF, lbl_0E6C
    INDSRC_MOV 0x07EF, 0x07F1
    ; lbl_05AB-05B7: MOV lbl_05CC, lbl_07EF
    ; lbl_05B7-05C0: SUB lbl_05CC, lbl_07F2; JA lbl_05C3
    MOV 0x05CC, 0x07EF
    SUBJG 0x05CC, 0x07F2, lbl_05C3

    lbl_05C0:
    ; lbl_05C0-05C3: JMP lbl_05C9
    jmp lbl_05C9  

    lbl_05C3:
    ; lbl_05C3-05C9: CMP lbl_05CC, 0; JZ lbl_05CD
    CMPJZ 0x05CC, lbl_05CD

    lbl_05C9:
    ; lbl_05C9-05CC: JMP lbl_0638
    jmp lbl_0638

    lbl_05CD:
    ; lbl_05CC-05CD: db 01, 00
    ; lbl_05CD-05D6: MMOV lbl_07F1, lbl_0533
    MOV 0x07F1, 0x0533

    MADD 0x07F5, 0x05DC
    ; lbl_05E3-05EF: MOV lbl_060A, lbl_07F1
    ; lbl_05EF-05FB: MOV lbl_060B, lbl_07F1
    ; lbl_05FB-0607: MOV lbl_0611, lbl_07F1
    ; lbl_0607-0613: MOV lbl_07F6, lbl_07F5
    INDDES_MOV 0x07F1, 0x07F5

    SUB 0x00FB, 0x0619
    ; lbl_061D-0626: MMOV lbl_062C, lbl_00FB
    MOV 0x062C, 0x00FB
    ; lbl_0626-0632: MOV lbl_0637, lbl_00F9
    ; lbl_0632-0635: XOR lbl_0000, lbl_0000
    ; lbl_0635-0638: JMP lbl_02E6
    INDJMP 0x00F9

    lbl_0638:
    ; lbl_0638-0641: MMOV lbl_07F1, lbl_0533
    ; lbl_0641-0644: XOR lbl_0000, lbl_0000
    ; lbl_0644-0647: JMP lbl_0648
    MOV 0x07F1, 0x0533

    MADD 0x07F1, 0x0647
    ; lbl_064E-065A: MOV lbl_0660, lbl_07F1
    ; lbl_065A-0666: MOV lbl_07EE, lbl_07F7
    INDSRC_MOV 0x07EE, 0x07F1
    ; lbl_0666-0672: MOV lbl_07F1, lbl_0533
    MOV 0x07F1, 0x0533
    ; lbl_0672-0675: XOR lbl_0000, lbl_0000
    ; lbl_0675-067B: MADD lbl_07F1, lbl_07EF
    MADD 0x07F1, 0x07EF
    ; lbl_067B-0687: MOV lbl_068D, lbl_07F1
    ; lbl_0687-0693: MOV lbl_07F0, lbl_07F6
    INDSRC_MOV 0x07F0, 0x07F1
    ; lbl_0693-069F: MOV lbl_07F4, lbl_07F0
    MOV 0x07F4, 0x07F0
    ; lbl_069F-06A2: XOR lbl_0000, lbl_0000
    ; lbl_06A2-06A3: db EE, 07
    ; lbl_06A3-06A4: db F4, 07
    ; lbl_06A4-06A5: db 00, 00
    SUB 0x7F4, 0x7EE
    ; lbl_06A5-06AE: MMOV lbl_07EE, lbl_07F4
    MOV 0x07EE, 0x07F4
    ; lbl_06AE-06BA: MOV lbl_07F1, lbl_0533
    MOV 0x07F1, 0x0533

    MADD 0x07F1, 0x06C0
    ; lbl_06C7-06D3: MOV lbl_06EE, lbl_07F1
    ; lbl_06D3-06DF: MOV lbl_06EF, lbl_07F1
    ; lbl_06DF-06EB: MOV lbl_06F5, lbl_07F1
    ; lbl_06EB-06F7: MOV lbl_07F7, lbl_07EE
    INDDES_MOV 0x07F1, 0x07EE
    ; lbl_06F7-0703: MOV lbl_071B, lbl_07EF
    MOV 0x071B, 0x07EF
    ; lbl_0703-070C: SUB lbl_071B, lbl_07F3; JA lbl_070F
    SUBJG 0x071B, 0x07F3, lbl_070F

    lbl_070C:
    ; lbl_070C-070F: JMP lbl_0715
    jmp lbl_0715

    lbl_070F:
    ; lbl_070F-0715: CMP lbl_071B, 0; JZ lbl_0718
    CMPJZ 0x071B, lbl_0718

    lbl_0715:
    ; lbl_0715-0718: JMP lbl_071C
    jmp lbl_071C


    lbl_0718:
    ; BUGFIX: LOOKS STRANGE
    ; lbl_0718-071B: JMP lbl_0761
    jmp lbl_0761

    lbl_071C:
    ; lbl_071B-071C: db FE, FF
    ; lbl_071C-072E: ADD lbl_07F1, lbl_07EF + lbl_0533
    ADD3 0x07F1, 0x07EF , 0x0533
    ; lbl_072E-073A: MOV lbl_0755, lbl_07F1
    ; lbl_073A-0746: MOV lbl_0756, lbl_07F1
    ; lbl_0746-0752: MOV lbl_075C, lbl_07F1
    ; lbl_0752-075E: MOV lbl_07F6, lbl_07EE
    INDDES_MOV 0x07F1, 0x07EE
    lbl_0761:
    ; lbl_075E-076A: MOV lbl_0770, lbl_0533
    ; lbl_076A-0776: MOV lbl_07F5, lbl_07F6
    INDSRC_MOV 0x07F5, 0x0533
    ; lbl_0776-0779: XOR lbl_0000, lbl_0000
    ; lbl_0779-077A: db EE, 07
    ; lbl_077A-077B: db 00, 00
    ; lbl_077B-077C: db 7F, 07
    xor eax, eax
    cmp ax, word [variables + 0x7EE * 2]
    jle lbl_077F

    lbl_077C:
    ; lbl_077C-077F: JMP lbl_0782
    jmp lbl_0782

    lbl_077F:
    ; lbl_077F-0782: JMP lbl_078F
    jmp lbl_078F

    lbl_0782:
    ; lbl_0782-0785: JMP lbl_0786
    jmp lbl_0786

    lbl_0786:
    ; lbl_0785-0786: db 01, 00
    ; lbl_0786-078C: MADD lbl_07F5, lbl_0785
    ; lbl_078C-078F: XOR lbl_0000, lbl_0000
    MADD 0x07F5, 0x0785

    lbl_078F:

    MADD 0x07F5, 0x0792
    ; lbl_0799-07A5: MOV lbl_07C0, lbl_0533
    ; lbl_07A5-07B1: MOV lbl_07C1, lbl_0533
    ; lbl_07B1-07BD: MOV lbl_07C7, lbl_0533
    ; lbl_07BD-07C9: MOV lbl_07F6, lbl_07F5
    INDDES_MOV 0x0533, 0x07F5

    SUB 0x00FB, 0x07CF
    ; lbl_07D3-07DC: MMOV lbl_07E2, lbl_00FB
    MOV 0x07E2, 0x00FB
    ; lbl_07DC-07E8: MOV lbl_07ED, lbl_00F9
    ; lbl_07E8-07EB: XOR lbl_0000, lbl_0000
    ; lbl_07EB-07EE: JMP lbl_02E6
    INDJMP 0x00F9


    end:
    leave
    ret
_main:
    pusha
    popa
    call vm_entry
    push 0
    call	_ExitProcess@4

SECTION .data
variables:
    TODAD

strHello: db "Hello world", 0
strHell0.len equ $ - strHello
strError: db "An error happend...", 0
strError.len equ $ - strError