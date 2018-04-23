	.section	__TEXT,__text,regular,pure_instructions
	.macosx_version_min 10, 12
	.globl	_main
	.p2align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## BB#0:
	pushq	%rbp
Lcfi0:
	.cfi_def_cfa_offset 16
Lcfi1:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Lcfi2:
	.cfi_def_cfa_register %rbp
	subq	$48, %rsp
	movl	$0, -4(%rbp)
	movl	$0, -24(%rbp)
	movl	-24(%rbp), %eax
	movl	%eax, -8(%rbp)
	movl	$1, -28(%rbp)
	movl	-28(%rbp), %eax
	movl	%eax, -12(%rbp)
	movl	$10, -32(%rbp)
	movl	-32(%rbp), %eax
	movl	%eax, -16(%rbp)
LBB0_1:                                 ## =>This Inner Loop Header: Depth=1
	cmpl	$0, -16(%rbp)
	je	LBB0_3
## BB#2:                                ##   in Loop: Header=BB0_1 Depth=1
	movl	-8(%rbp), %eax
	movl	%eax, -20(%rbp)
	movl	-12(%rbp), %eax
	movl	%eax, -8(%rbp)
	movl	-12(%rbp), %eax
	addl	-20(%rbp), %eax
	movl	%eax, -36(%rbp)
	movl	-36(%rbp), %eax
	movl	%eax, -12(%rbp)
	movl	$1, -40(%rbp)
	movl	-16(%rbp), %eax
	subl	-40(%rbp), %eax
	movl	%eax, -44(%rbp)
	movl	-44(%rbp), %eax
	movl	%eax, -16(%rbp)
	jmp	LBB0_1
LBB0_3:
	leaq	L_.str(%rip), %rdi
	movl	-8(%rbp), %esi
	movb	$0, %al
	callq	_printf
	movl	-4(%rbp), %esi
	movl	%eax, -48(%rbp)         ## 4-byte Spill
	movl	%esi, %eax
	addq	$48, %rsp
	popq	%rbp
	retq
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"%d\n"


.subsections_via_symbols
