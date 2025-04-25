parser grammar Gallina;

options { tokenVocab=GallinaLexer; }

goal: term EOF;

term: <assoc=left> term term # Application
    | <assoc=left> term COLON term # Cast
    | var # Variable
    | sort_term # Sort
    | LPAREN term RPAREN # Parenthesis
    | <assoc=right> FUN (open_binder | binder_list) MAPSTO term # Fun
    | <assoc=right> FORALL (open_binder | binder_list) COMMA term # Product
    | LET var COLON term ASSGN term IN term # Let
    | IF term (AS alias)? RET term THEN term ELSE term # Cond
    | MATCH subject_list (RET term)? WITH case_list? END # Match
    | FIX var binder_list (LCBRACE STRUCT var RCBRACE)? COLON term ASSGN term # Fix
    | evar_term # ExVar
    ;

subject_list: subject (COMMA subject)*;

subject: term (AS alias)? (IN pattern)?;

case_list: PIPE? case_clause (PIPE case_clause)*;

case_clause: pattern (COMMA pattern)* MAPSTO term;

pattern: name+ (AS alias)? # BasicPatt
       | LPAREN pattern RPAREN # EnclosedPatt
       ;

alias: var;

binder_list: (LPAREN open_binder RPAREN)+;

open_binder: name+ COLON term;

sort_term: SET
         | PROP
         | SPROP
         | TYPE (universe_annot)?
         ;

universe_annot: ATSGN LCBRACE UNDRSCORE RCBRACE
              | ATSGN LCBRACE MAX LPAREN universe_expr (COMMA universe_expr)* RPAREN RCBRACE
              | ATSGN LCBRACE (universe_expr)* RCBRACE
              ;

universe_expr: name (PLUS NUM)?;

name: var | UNDRSCORE;

evar_term: UNDRSCORE
         | QMARK var
         | QMARK LSBRACE var RSBRACE
         | QMARK LSBRACE QMARK var RSBRACE
         | QMARK var ATSGN LCBRACE var ASSGN term (SEMICOLON var ASSGN term)* RCBRACE
         ;

var: VAR (universe_annot)? | MAX;
