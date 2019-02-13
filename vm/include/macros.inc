

%ifndef __MACROS_INC__
%define __MACROS_INC__

BUFFER_INPUT_LENGTH equ 0x20
STD_INPUT_HANDLE    equ -10
STD_OUTPUT_HANDLE   equ -11

%macro WRITE_MESSAGE 2
	push	STD_OUTPUT_HANDLE
	call	_GetStdHandle@4
	mov	ebx, eax    

	; WriteFile( hstdOut, message, length(message), &bytes, 0);
	push	0	; lpOverlapped
	mov eax, ebp
    sub eax, 4
	push	eax	; Number of bytes written
	mov	eax, %2
	push	eax	; Number of bytes to write
	mov	eax, %1
	push	eax	; buffer
	push	ebx	; file handle
	call	_WriteFile@20
%endmacro

; INDDES_MOV lbl_00F8, lbl_0008
%macro INDDES_MOV 2
    mov ax, [variables + %2 * 2]
	movzx ebx, word [variables + %1 * 2]
    mov [variables + ebx * 2], ax
%endmacro

%macro INDSRC_MOV 2
    movzx ebx, word [variables + %2 * 2]
    mov ax, [variables + ebx * 2]
    mov [variables + %1 * 2], ax
%endmacro

%macro MOV 2
    mov ax, [variables + %2 * 2]
    mov [variables + %1 * 2], ax
%endmacro

%macro MADD 2
    mov ax, [variables + %2 * 2]
    add [variables + %1 * 2], ax
%endmacro

%macro SUB 2
    mov ax, [variables + %2 * 2]
    sub [variables + %1 * 2], ax
%endmacro

%macro SUBJG 3
    mov ax, [variables + %2 * 2]
    sub [variables + %1 * 2], ax
    cmp word [variables + %1 * 2], 0
    jbe %3
%endmacro

%macro CMPJZ 2
    cmp word [variables + %1 * 2], 0
    jz %2
%endmacro

%macro INDJMP 1
    jmp lbl_02E6
    ; mov ax, word [variables + %1 * 2]
    ; cmp ax, 0x2e6
    ; jz lbl_02E6
    ; WRITE_MESSAGE strError, strError.len
    ; mov eax, cr4
    ; leave
    ; ret
%endmacro

%macro INDJMP2 1
    jmp lbl_00EB
    ; movzx ebx, word [variables + %1 * 2]
    ; mov ax, word [variables + ebx * 2]
    ; cmp ax, 0xeb
    ; jz lbl_00EB
    ; WRITE_MESSAGE strError, strError.len
    ; mov eax, cr4
    ; leave
    ; ret
%endmacro

%macro ADD3 3
    mov ax, [variables + %2 * 2]
    mov [variables + %1 * 2], ax
    mov ax, [variables + %3 * 2]
    add [variables + %1 * 2], ax
%endmacro

%macro JA 1
    ja %1
%endmacro

%macro HANDLE_OUTPUT 0
    lea esi, [variables + 0x4]
    WRITE_MESSAGE esi, 1
    mov word [variables + 0x2*2], 0
    mov word [variables + 0x4*2], 0
%endmacro
%endif