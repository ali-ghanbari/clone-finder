lexer grammar GallinaLexer;

MAX: 'max';
LET: 'let';
IF: 'if';
THEN: 'then';
ELSE: 'else';
FUN: 'fun';
FIX: 'fix';
FORALL: 'forall';
MATCH: 'match';
WITH: 'with';
RET: 'return';
STRUCT: 'struct';
END: 'end';
AS: 'as';
IN: 'in';
SET: 'Set';
PROP: 'Prop';
SPROP: 'SProp';
TYPE: 'Type';

UNDRSCORE: '_';

COMMENT: '(*' .*? '*)' -> skip;

LPAREN: '(';
RPAREN: ')';
MAPSTO: '=>';
ASSGN: ':=';
LCBRACE: '{';
RCBRACE: '}';
COLON: ':';
COMMA: ',';
SEMICOLON: ';';
DOT: '.';
PIPE: '|';
ATSGN: '@';
LSBRACE: '[';
RSBRACE: ']';
PLUS: '+';
QMARK: '?';

VAR: [@a-zA-Z\u0080-\uFFFF][a-zA-Z0-9_'.\u0080-\uFFFF]*;

NUM: [1-9][0-9]*;

WS: [ \t\r\n]+ -> skip;
