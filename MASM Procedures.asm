TITLE Practicing Low-Level I/O Procedures     (Proj6_bucienj.asm)

; Author: Jenna Bucien
; Last Modified: 12/05/2021
; OSU email address: bucienj@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: 6                Due Date: 12/05/2021
; Description: Program includes string processing macros that incorporate the 
;		Irvine Library's ReadString and WriteString procedures. Then, uses the 
;		macros in two procedures:
;			- The first procedure ReadVal reads a user's numeric input (can be a positive or 
;			  negative integer) as an ASCII string. If the ASCII string converts to a 
;			  valid SDWORD number, the program stores the value in memory. If the 
;			  string is invalid, an error message is displayed. 
;			- The second procedure WriteVal converts a numeric SDWORD into a digit string and
;			  prints the ASCII string representation of that SDWORD value to the console.
;		Finally, the program tests the macros and procedures by asking the user for 10 valid 
;		numbers. If the number is invalid (cannot be stored as a SDWORD; contains characters 
;		other than 0-9, +, or -; is blank), the program displays an error message and reprompts
;		the user. The program stores the integers as an array. Then it displays these integers,
;		their sum, and their truncated average on the console.

INCLUDE Irvine32.inc

; ----------------------------------------------------------------------------------
; Name: mGetString
; Displays a message prompting the user to enter a string. Then stores the user's keyboard
; input in a memory location.
; Preconditions: uses EDX to store address of prompt and address of string buffer;
;      uses ECX to store buffer size, uses EAX to store number of characters
;	   entered. All registers used are restored.
; Receives: 
;	- promptAddress = address of message prompting the user to enter a string
;	- strBufferAddress = the address of the string buffer
;	- strLength = the length the input string can accomodate
; Returns:
;   - bytesRead = the number of bytes the macro reads (num of characters)
;  ----------------------------------------------------------------------------------
mGetString MACRO promptAddress:REQ, strBufferAddress:REQ, strLength:REQ, bytesRead:REQ
	PUSH	EAX
	PUSH	ECX
	PUSH	EDX
	MOV		EDX, promptAddress
	CALL	WriteString
	MOV		EDX, strBufferAddress
	MOV		ECX, strLength
	CALL	ReadString
	MOV		bytesRead, EAX
	POP		EAX
	POP		ECX
	POP		EDX
ENDM

; ----------------------------------------------------------------------------------
; Name: mDisplayString
; Prints a string stored in a specific memory location.
; Preconditions: uses EDX register (pushed on stack)
; Postconditions:EDX register restored (popped off stack)
; Receives:
;       - stringAddress = the address of the string's memory location
; Returns:
;	    - none
;  ----------------------------------------------------------------------------------
mDisplayString MACRO stringAddress:REQ
	PUSH	EDX
	MOV		EDX, stringAddress
	CALL	WriteString
	POP		EDX
ENDM

; ----------------------------------------------------------------------------------
; Name: mClearString
; Clears a string of its character values by setting all BYTEs to 0.
; Preconditions: uses ESI, ECX, and EBX registers (pushed on stack). String must be 
; declared in data segment.
; Postconditions: ESI, ECX, and EBX register restored (popped off stack)
; Receives:
;       - stringLabel = the string to be cleared
; Returns:
;	    - stringLabel, which now has all of its BYTEs set to 0.
;  ----------------------------------------------------------------------------------
mClearString MACRO stringLabel:REQ
LOCAL _clearLoop
	PUSH    ESI
	PUSH	ECX
	PUSH	EBX
	MOV		ESI, OFFSET stringLabel
	MOV		ECX, LENGTHOF stringLabel
_clearLoop:
	MOV		EBX, 0
	MOV		[ESI], EBX
	ADD		ESI, TYPE stringLabel
	LOOP	_clearLoop
	POP		EBX
	POP		ECX
	POP		ESI
ENDM


ARRAY_SIZE = 10
NEGATIVE_SIGN EQU '-'


.data
	userString				BYTE		1000 DUP(?)
	userStringLength		SDWORD		?
	answerString			BYTE		1000 DUP(?)
	answerStringReversed	BYTE		1000 DUP(?)
	currentNum				SDWORD		0					
	numArray				SDWORD		ARRAY_SIZE DUP (0)
	currentArrayIndex		SDWORD		0
	sum						SDWORD		?
	average					SDWORD		?
	invalid					DWORD		0
	space					BYTE		" ",0
	comma					BYTE		",",0
	programTitle			BYTE		"PROGRAMMING ASSIGNMENT 6: Practicing Low-Level I/O Procedures",13,10,0
	author					BYTE		"Written by: Jenna Bucien",13,10,0
	intro1					BYTE		"Please enter 10 signed decimal integers.",13,10,0
	intro2					BYTE		"Each number needs to be small enough to fit inside a 32 bit register.",13,10,0
	intro3					BYTE		"I will display a list of the integers, their sum, and their average value.",13,10,0
	prompt					BYTE		"Please enter a signed integer:  ",0
	error					BYTE		"ERROR: You did not enter a valid signed integer or your number was too big. Try again.",13,10,0
	numbersTitle			BYTE		"You entered the following numbers:",13,10,0
	sumTitle				BYTE		"The sum of these numbers is:  ",0
	averageTitle			BYTE		"The truncated average of these numbers is:  ",0
	goodbye					BYTE		"Thank you for helping me practice! Goodbye!",13,10,0


.code
main PROC
;   -----------------------------------------------------------------
;	Pass introProc parameters and call introProc.
;   -----------------------------------------------------------------
	PUSH	offset programTitle
	PUSH	offset author
	PUSH    offset intro1	
	PUSH	offset intro2	
	PUSH	offset intro3					
	CALL	introProc
;   -----------------------------------------------------------------
;	Ask user for 10 valid digit strings, so set ECX to 10 (the ARRAY_SIZE).
;   Call ReadVal for each string. If user enters invalid string, call 
;   ReadVal again without decrementing ECX. After each return from ReadVal, 
;   place converted integer into numArray.
;   -----------------------------------------------------------------
	MOV		ECX, ARRAY_SIZE
_getNumbers:
	PUSH    offset prompt
	PUSH    offset userString
	PUSH	offset userStringLength
	PUSH	offset error
	PUSH    offset invalid
	PUSH	offset currentNum
	CALL    readVal
	CMP     invalid, 1						; if invalid = 1, then re-call readVal
	JE		_getNumbers
_movetoArray:		
	PUSH	ECX								; preserve outer loop
	MOV		EAX, currentNum
	MOV		ESI, offset numArray
	MOV		ECX, currentArrayIndex
	CMP		ECX, 0							; if placing 1st integer, don't have to move numArray pointer
	JE		_place
_toCorrectIndex:
	ADD		ESI, TYPE numArray				; otherwise, increment to correct index (next blank SDWORD)
	LOOP	_toCorrectIndex
_place:
	MOV		[ESI], EAX
	INC		currentArrayIndex
	POP		ECX
	MOV		currentNum, 0				    ; reset currentNum
	LOOP	_getNumbers
;   -----------------------------------------------------------------
;	Calculate the sum and the truncated average of the 10 integers
;	located in numArray. Store both results.
;   -----------------------------------------------------------------
	MOV		ESI, offset numArray
	MOV		ECX, lengthof numArray
	DEC		ECX								; only want to loop 9 times
	MOV		EAX, [ESI]						; first num in array
_getSum:
	ADD		ESI, TYPE numArray				; move pointer to next integer
	ADD		EAX, [ESI]
	LOOP	_getSum
	MOV		sum, EAX						; save sum
_getAverage:
	XOR		EDX, EDX
	MOV		EBX, lengthof numArray
	MOV		EAX, sum
	CDQ
	IDIV	EBX
	MOV		average, EAX					; truncated average, so discard remainder
;   -----------------------------------------------------------------
;	Use WriteVal to convert each numArray element back into ASCII string
;   and print to console. WriteVal called for each individual array element, 
;	so it loops 10 types.
;   -----------------------------------------------------------------
	CALL	CrLf
	mDisplayString OFFSET numbersTitle
	MOV		ESI, OFFSET numArray
	MOV		ECX, LENGTHOF numArray
_printArray:
	MOV		EAX, [ESI]
	MOV		currentNum, EAX					; current array element pushed to WriteVal as variable "currentNum"
	PUSH	OFFSET answerStringReversed     
	PUSH	OFFSET answerString
	PUSH	currentNum
	PUSH    NEGATIVE_SIGN
	CALL	WriteVal
	CMP		ECX, 1							; if last integer just printed, don't add comma and space
	JE		_end
	mDisplayString OFFSET comma
	mDisplayString OFFSET space	
	ADD		ESI, TYPE numArray				; move array pointer to next integer
_end:
	mClearString answerString				; clear the answer strings after each WriteVal call to prevent print-out of extra digits 
	mClearString answerStringReversed		; (since ASCII strings are different lengths)
	LOOP	_printArray
	CALL	CrLf
;   -----------------------------------------------------------------
;	Use WriteVal to convert the sum of the integers into an ASCII string
;	and print out string to console.
;   -----------------------------------------------------------------
	mClearString answerString				; clear the answer strings 
	mClearString answerStringReversed
	mDisplayString OFFSET sumTitle
	PUSH	OFFSET answerStringReversed
	PUSH	OFFSET answerString
	PUSH	sum
	PUSH	NEGATIVE_SIGN
	CALL	WriteVal
	CALL	crlf
;   -----------------------------------------------------------------
;	Use WriteVal to convert the average of the integers into an ASCII string
;	and print out string to console.
;   -----------------------------------------------------------------
	mClearString answerString
	mClearString answerStringReversed
	mDisplayString OFFSET averageTitle
	PUSH	OFFSET answerStringReversed
	PUSH	OFFSET answerString
	PUSH	average
	PUSH	NEGATIVE_SIGN
	CALL	WriteVal
	CALL	crlf
;   -----------------------------------------------------------------
;	Display goodbye message
;   -----------------------------------------------------------------
	CALL	CRLF
	PUSH	offset goodbye
	CALL	bye

	Invoke ExitProcess,0	; exit to operating system
main ENDP

; ----------------------------------------------------------------------------------
; Name: introProc
;  Prints the program name and author, then gives an introduction to the program.
; Receives:
;	  - [EBP+24] = reference to programTitle
;	  - [EBP+20] = reference to author
;	  - [EBP+16] = reference to instruction1
;	  - [EBP+12] = reference to instruction2
;     - [EBP+8] = reference to instruction3
;  ----------------------------------------------------------------------------------
introProc PROC
	PUSH	EBP
	MOV		EBP, ESP
	mDisplayString [EBP+24]
	mDisplayString [EBP+20]
	CALL	CrLf
	mDisplayString [EBP+16]
	mDisplayString [EBP+12]
	mDisplayString [EBP+8]
	CALL	CrLf
	POP		EBP
	RET		20
introProc ENDP


; ----------------------------------------------------------------------------------
; Name: readVal
; Uses mGetString macro to ask user for a string of digits. Validates user input, 
; ensuring that input does not contain characters other than 0-9, +, or -. Also makes
; sure input fits into 32-bit register, and input is not blank. Then converts user input 
; ASCII string to its numeric value representation (SDWORD). Stores this value in memory.
; Preconditions: userString must be defined in data segment with > 12 BYTEs of buffer.
;		currentNum must be an SDWORD.
; Postconditions: None, all registers restored
; Receives:
;		- [EBP+28] = reference to prompt
;		- [EBP+24] = reference to userString
;		- [EBP+20] = reference to userStringLength
;		- [EBP+16] = reference to error (message)
;		- [EBP+12] = reference to invalid
;		- [EBP+8]  = reference to currentNum
; Returns:
;		-  the converted integer, saved to currentNum
;		-  invalid clear (0) if input is successfully converted, set (1) if input is invalid
;  ----------------------------------------------------------------------------------
readVal PROC
	PUSH	EBP
	MOV		EBP, ESP
	PUSHAD
	MOV		ESI, [EBP+24]						; move userString pointer into ESI			
	MOV		EDI, [EBP+20]						; move userStringLength pointer into EDI
	MOV		EBX,  [EDI]							
	mGetString [EBP+28], ESI, 1000, EBX			; prompt, userString address, buffer, userStringLength
;   -----------------------------------------------------------------
;	Validation of userString. Make sure it can convert to valid SDWORD integer.
;   -----------------------------------------------------------------
	MOV	    [EDI], EBX							
	MOV     ECX, [EDI]							; userStringLength into ECX for loop counter
	XOR	    EAX, EAX
	DEC	    ECX									; loop (userStringLength - 1) times
	CMP     ECX, 0								; if userString only 1 digit, check to see if it's a 0
	JNE     _validateFirstDigit
	CLD
	LODSB										
	CMP     EAX, 48								
	JE      _convertDigitString					; if it is a 0, it is valid and can be converted.
	DEC     ESI									; reset pointer to beginning of userString	
	JMP     _validateFirstDigit
_validateFirstDigit:
	CLD
	LODSB
	CMP     EAX, 48									
	JG      _checkUpper							; already checked for 0, so all other digits must be > 0 (no leading 0s) 
	CMP     EAX, 45								; if first char in string is a '-'
	JE      _validateNextDigits		
	CMP     EAX, 43								; if first char in string is a '+'
	JE		_validateNextDigits
	JMP		_invalid							; first char is not {0, 1+, -, +} so it must be invalid
_checkUpper:
	CMP		EAX, 57								; if first char is > 9, then it is invalid
	JG		_invalid	
	JECXZ	_convertDigitString					; if userString only 1 digit, it is validated and can be converted
	JMP		_validateNextDigits
_validateNextDigits:
	CLD
	LODSB										; move userString pointer to next char
	CMP		EAX, 48								; char must be in range 48-57 (for 0-9)
	JL		_invalid
	CMP		EAX, 57
	JG		_invalid
	DEC		ECX									
	JECXZ	_fitinRegister						; loop until all chars validated
	JMP		_validateNextDigits
_invalid:										; display error message and exit procedure
	mDisplayString [EBP+16]						
	PUSH	EDI
	PUSH	EAX
	MOV		EDI, [EBP+12]						; set invalid = 1
	MOV		EAX, [EDI]
	MOV		EAX, 1
	MOV		[EDI], EAX
	POP		EAX
	POP		EDI	
	JMP		_endReadValProc						
_fitinRegister:									; checks to see if userString as SDWORD can fit into 32-bit reg
	PUSH	EDX									;			by using ParseInteger32
	PUSH	EAX
	PUSH	ECX
	MOV		ESI, [EBP+24]						; reset pointer to beginning of string
	MOV		EDX, ESI
	MOV		ECX, [EDI]							; userStringLength 
	INC		ECX									; account for null byte
	XOR		EAX, EAX
	CALL	ParseInteger32
	POP		ECX
	POP		EAX
	POP		EDX
	JO		_invalid							; if Overflow flag is set, then the integer cannot fit and is invalid
	JMP		_convertDigitString					
;   -----------------------------------------------------------------
;	Validation is completed. Convert userString to a signed integer.
;   -----------------------------------------------------------------
_convertDigitString:
	PUSH	EDI
	PUSH	EAX
	MOV		EDI, [EBP+12]						; userString valid, so set invalid = 0 (clear it)
	MOV		EAX, [EDI]
	MOV		EAX, 0
	MOV		[EDI], EAX
	POP		EAX
	POP		EDI
	MOV		ECX, [EDI]							; reset strLength counter
	MOV		EBX, [EBP+8]						; address of currentNum into EBX
	MOV		ESI, [EBP+24]						; reset pointer to beginning of string
	XOR		EAX, EAX							; make sure EAX is clear before loading [ESI] into AL	
	CLD
	LODSB
	CMP		EAX, 45								; if there is a - or + sign, skip conversion for now and go to next digit
	JE		_sign
	CMP		EAX, 43									
	JE		_sign
	DEC		ESI									; if no prepended sign, reset pointer to beginning of string
	JMP		_nextDigit
_sign:											
	DEC		ECX									; decrease loop counter to account for sign char						    
_nextDigit:										; convert each char and loop until end of string
	LODSB			
	PUSH	EAX
	PUSH	EDI
	MOV		EDI, EAX							; move char into EDI
	SUB		EDI, 48								; char - 48 = integer value of digit						
	MOV		EAX, [EBX]							; move value of currentNum into EAX							
	XOR		EDX, EDX
	PUSH	EBX
	MOV		EBX, 10
	IMUL	EBX									; currentNum * 10
	POP		EBX
	ADD		EAX, EDI							; (currentNum * 10) + (current char - 48) = new currentNum
	MOV		[EBX], EAX							;  place new currentNum at correct address
	POP		EDI
	POP		EAX				
	DEC		ECX
	JECXZ	_evalNeg							; if we are at end of string, check to see if integer is negative
	JMP		_nextDigit
_evalNeg:
	MOV		ESI, [EBP+24]						; reset to beginning of string
	XOR		EAX, EAX	
	CLD
	LODSB
	CMP		EAX, 45							
	JNE		_endReadValProc
	MOV		EAX, [EBX]
	NEG		EAX									; if userString is negative, convert currentNum to its negative value
	MOV		[EBX], EAX
_endReadValProc:
	POPAD
	POP		EBP
	RET		24
readVal ENDP

  
; ----------------------------------------------------------------------------------
; Name: writeVal
; Takes numeric SDWORD and returns its equivalent as a string (ASCII digits)
; Preconditions: value referenced by [EBP+12] must be a numeric SDWORD (signed integer). answerString
; and answerStringReversed must have buffer of at least 12 bytes.
; Postconditions: none, all registers restored
; Receives:
;	- [EBP+20] = answerStringReversed
;	- [EBP+16] = answerString
;	- [EBP+12] =  currentNum, sum, or average (an SDWORD)
;   - [EBP+8] = NEGATIVE_SIGN
;	 LOCAL variables:
;			- lengthofString = the number of characters in the answerStringReversed
;			- negativeFlag = set to 1 if integer is negative, otherwise set to 0
; Returns:
;		- answerString, a string BYTE-array that is the ASCII representation of the 
;		SDWORD input
;		- anwerStringReversed, a reversed version of answerString
;  ----------------------------------------------------------------------------------
writeVal PROC
	LOCAL lengthofString:DWORD, negativeFlag:DWORD
	PUSHAD
	MOV		EDI, [EBP+20] 				; address of answerstringreversed in EDI
	MOV		EAX, [EBP+12]				; integer in EAX
	MOV		lengthofString, 0			
	CMP		EAX, 0
	JL		_negativeNumber				; if integer < 0, then it is a negative num so we need to add negative sign to its ASCII string representation
	MOV		negativeFlag, 0			
	JMP		_convert
_negativeNumber:
	MOV		negativeFlag, 1				
	NEG		EAX
	JMP		_convert 
_convert:
	MOV		EAX, EAX					; prepare for repeated division of integer
	CDQ
	XOR		EDX, EDX
	PUSH	EBX  
	MOV		EBX, 10
	IDIV	EBX							; divide integer by 10
	POP		EBX
	PUSH	EAX
	ADD		EDX, 48						; Remainder is the "current digit". Add 48 to remainder to get ascii representation of that digit
	MOV		EAX, EDX					; "current digit" in AL to move to string
	CLD
	STOSB								; place ascii digit into answerString
	INC		lengthofString
	POP		EAX
	CMP		EAX, 0						; repeated until quotient is 0
	JG		_convert
	JMP		_checkNegative
_checkNegative:
	CMP		negativeFlag, 1				; if integer is negative, append - sign to string
	JE		_addNegativeSign
	JMP		_reverseString
_addNegativeSign:
	PUSH	EAX
	MOV		EAX, [EBP+8]				; '-' in AL
	CLD					
	STOSB					
	POP		EAX
	INC		lengthofString
	JMP		_reverseString
_reverseString:							; conversion algorithm gives ASCII string in reverse order, so reverse to get correct ASCII string
	PUSH	ESI
	PUSH	EDI
	PUSH	ECX
	MOV		ECX, lengthofString
	MOV		ESI, [EBP+20]				
	ADD		ESI, ECX					; start from last char of answerStringReversed
	DEC		ESI  
	MOV		EDI, [EBP+16]				
_reverseLoop:	
	STD									; set direction flag so pointer of answerStringReversed decrements 		
    LODSB								; load char into AL
    CLD									; clear direction flag so pointer of answerString increments
    STOSB								; place char into answerString
	LOOP	_reverseLoop				; loop for all chars
	POP		ECX
	POP		EDI
	POP		ESI
_printOut:
	mDisplayString [EBP+16]			
_endWriteVal:
	POPAD
	RET		16
writeVal ENDP

; ----------------------------------------------------------------------------------------------------------------
; Name: bye
; Displays a goodbye message.
; Receives:
;	- [EBP+8] = reference to goodbye message
;------------------------------------------------------------------------------------------------------------------
bye PROC
	PUSH	EBP
	MOV		EBP, ESP
	mDisplayString [EBP+8]
	POP		EBP
	RET		4
bye ENDP

END main
