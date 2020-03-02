.class public Program
.super java/lang/Object
.method public <init>()V
aload_0
invokenonvirtual java/lang/Object/<init>()V
return
.end method
.method public static main([Ljava/lang/String;)V
.limit locals 5
.limit stack 1024
new java/util/Scanner
dup
getstatic java/lang/System.in Ljava/io/InputStream;
invokespecial java/util/Scanner.<init>(Ljava/io/InputStream;)V
astore 0
aload 0
invokevirtual java/util/Scanner.nextInt()I
istore 1
sipush 0
istore 2
l1:
iload 1
sipush 3
if_icmple l2
iload 2
sipush 1
iadd
istore 2
iload 1
sipush 1
isub
istore 1
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 2
invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
goto l1
l2:
sipush 1
iload 1
iadd
sipush 3
imul
istore 3
l3:
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 3
invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
iload 3
sipush 1
isub
istore 3
iload 3
sipush 0
if_icmpne l3
iload 2
sipush 5
if_icmple l4
iload 2
sipush 10
if_icmpge l4
getstatic java/lang/System/out Ljava/io/PrintStream;
sipush 25
invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
goto l5
l4:
iload 1
iload 2
iadd
istore 4
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 4
sipush 25
iadd
invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
l5:
return
.end method
