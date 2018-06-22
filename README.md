'Sm' is a language designed to be compact, all reserved words are
two characters in length.

Whats the point? ...ug well.. it was fun to make?

contained is a scanner, parser and code generator. Together they
produce Java assembly to be run on a JVM.

Pipe your input file to the code generator and pipe the output to 
desired assembly file. Using Jasmin convert assembly code to a Java 
Class file and Voila! you are good to go.

The Compiler excepts programs that follow this 
Extented-BNF

Program = Statements
Statements = Statement (';' Statement)*
Statement = If | While | For| Assignment | Input | Output

If = 'if' BooleanExpression '{' Statements '}' ['el' '{' Statements '}']
While = 'wl' BooleanExpression '{' Statements '}'
For = 'fr' Assignment '{' Statements '}'
Assignment = identifier ':' Expression
Input = 'in' identifier
Output = 'ot' (identifier | Expression)

BooleanExpression = BooleanTerm ('|' BooleanTerm)*
BooleanTerm = BooleanFactor ('&' BooleanFactor)*
BooleanFactor = 'nt' BooleanFactor | Comparison

Comparison = Expression Relation Expression
Relation = '=' | '!=' | '<' | '<=' | '>' | '>='

Expression = Term (('+' | '-') Term)*
Term = Factor (('*' | '/') Factor)*
Factor = '('Expression')' | number | identifier

Some Limitations:
Integers cant be to long.
Stack size must not exceed 1024.
Integer is the only type.
Logical operators cannot be nested.
