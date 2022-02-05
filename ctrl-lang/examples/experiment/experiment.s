	.text
	.file	"<string>"
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	.cfi_startproc
	subl	$20, %esp
	.cfi_def_cfa_offset 24
	pushl	24(%esp)
	.cfi_adjust_cfa_offset 4
	calll	square
	addl	$24, %esp
	.cfi_adjust_cfa_offset -24
	retl
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc

	.globl	fact
	.p2align	4, 0x90
	.type	fact,@function
fact:
	.cfi_startproc
	pushl	%esi
	.cfi_def_cfa_offset 8
	.cfi_offset %esi, -8
	movl	8(%esp), %esi
	testl	%esi, %esi
	je	.LBB1_2
	movb	$1, %al
	testb	%al, %al
	je	.LBB1_2
	leal	-1(%esi), %eax
	pushl	%eax
	.cfi_adjust_cfa_offset 4
	calll	fact
	addl	$4, %esp
	.cfi_adjust_cfa_offset -4
	imull	%esi, %eax
	popl	%esi
	retl
.LBB1_2:
	movl	$1, %eax
	popl	%esi
	retl
.Lfunc_end1:
	.size	fact, .Lfunc_end1-fact
	.cfi_endproc

	.globl	square
	.p2align	4, 0x90
	.type	square,@function
square:
	.cfi_startproc
	movl	4(%esp), %eax
	imull	%eax, %eax
	retl
.Lfunc_end2:
	.size	square, .Lfunc_end2-square
	.cfi_endproc


	.section	".note.GNU-stack","",@progbits
