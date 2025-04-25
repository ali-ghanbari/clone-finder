from antlr4.error.ErrorListener import ErrorListener

from antlr4 import InputStream, CommonTokenStream

from parsing.parser.GallinaLexer import GallinaLexer
from parsing.parser.Gallina import Gallina
from parsing.parser.GallinaVisitor import GallinaVisitor
from parsing.ast.goal_ast import *


class GoalParser:
    def __init__(self, goal : str):
        self.__goal = goal
        input_stream = InputStream(goal)
        lexer = GallinaLexer(input_stream)
        self.__stream = CommonTokenStream(lexer)

    def parse(self) -> Term:
        parser = Gallina(self.__stream)
        error_listener = GoalErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        ast = GoalASTConstructor().visit(parser.goal())
        if error_listener.errors:
            print('-' * 50)
            print('Following errors:')
            for err in error_listener.errors:
                print(err)
            print('were encountered when parsing:')
            print(self.__goal)
            print('-' * 50)
            quit()
        return ast


class GoalASTConstructor(GallinaVisitor):
    def visitGoal(self, ctx: Gallina.GoalContext):
        return self.visit(ctx.term())

    def visitName(self, ctx: Gallina.NameContext):
        return Var(ctx.getText())

    def visitUniverse_annot(self, ctx: Gallina.Universe_annotContext):
        return ctx.getText()

    def visitCast(self, ctx: Gallina.CastContext):
        term = self.visit(ctx.term(0))
        term_type = self.visit(ctx.term(1))
        return Cast(term, term_type)

    def visitParenthesis(self, ctx: Gallina.ParenthesisContext):
        return self.visit(ctx.term())

    def visitVar(self, ctx: Gallina.VarContext):
        return Var(ctx.getText())

    def visitVariable(self, ctx: Gallina.VariableContext):
        return self.visit(ctx.var())

    def visitExVar(self, ctx: Gallina.ExVarContext):
        return self.visit(ctx.evar_term())

    def visitEvar_term(self, ctx: Gallina.Evar_termContext):
        if ctx.UNDRSCORE() is not None:
            return Var(ctx.getText())
        return Var('?%s' % ctx.var(0).getText())

    def visitSort(self, ctx: Gallina.SortContext):
        return self.visit(ctx.sort_term())

    def visitSort_term(self, ctx: Gallina.Sort_termContext):
        name = ctx.getChild(0).getText()
        annotation = None
        if ctx.universe_annot() is not None:
            annotation = self.visit(ctx.universe_annot())
        return Sort(name, annotation)

    def visitProduct(self, ctx: Gallina.ProductContext):
        params = self.visit(ctx.getChild(1))
        if isinstance(params, Binder):
            params = [params]
        body = self.visit(ctx.term())
        return Product.build(params, body)

    def visitFix(self, ctx: Gallina.FixContext):
        name = self.visit(ctx.var(0))
        params = self.visit(ctx.binder_list())
        struct = None
        if ctx.var(1) is not None:
            struct = self.visit(ctx.var(1))
        ret_ty = self.visit(ctx.term(0))
        body = self.visit(ctx.term(1))
        return Fix(name, params, ret_ty, body, struct=struct)

    def visitLet(self, ctx: Gallina.LetContext):
        var = self.visit(ctx.var())
        var_ty = self.visit(ctx.term(0))
        var_def = self.visit(ctx.term(1))
        body = self.visit(ctx.term(2))
        return Let(var, var_ty, var_def, body)

    def visitCond(self, ctx: Gallina.CondContext):
        guard = self.visit(ctx.term(0))
        guard_alias = None
        if ctx.alias() is not None:
            guard_alias = self.visit(ctx.alias())
        ret_ty = self.visit(ctx.term(1))
        then_branch = self.visit(ctx.term(2))
        else_branch = self.visit(ctx.term(3))
        return Cond(guard, ret_ty, then_branch, else_branch, guard_alias=guard_alias)

    def visitFun(self, ctx: Gallina.FunContext):
        params = self.visit(ctx.getChild(1))
        if isinstance(params, Binder):
            params = [params]
        body = self.visit(ctx.term())
        return Fun.build(params, body)

    def visitApplication(self, ctx: Gallina.ApplicationContext):
        func = self.visit(ctx.term(0))
        arg = self.visit(ctx.term(1))
        return App(func, arg)

    def visitSubject_list(self, ctx: Gallina.Subject_listContext):
        subjects = []
        for sc in ctx.subject():
            subjects.append(self.visit(sc))
        return subjects

    def visitSubject(self, ctx: Gallina.SubjectContext):
        term = self.visit(ctx.term())
        term_alias = None
        if ctx.alias() is not None:
            term_alias = self.visit(ctx.alias())
        pattern = None
        if ctx.pattern() is not None:
            pattern = self.visit(ctx.pattern())
        return MatchSubject(term, term_alias, pattern)

    def visitMatch(self, ctx: Gallina.MatchContext):
        subject_list = self.visit(ctx.subject_list())
        ret_ty = None
        if ctx.term() is not None:
            ret_ty = self.visit(ctx.term())
        case_list = []
        if ctx.case_list() is not None:
            case_list = self.visit(ctx.case_list())
        return Match(subject_list, case_list, ret_ty=ret_ty)

    def visitCase_list(self, ctx: Gallina.Case_listContext):
        case_list = []
        for ccc in ctx.case_clause():
            case_list.append(self.visit(ccc))
        return case_list

    def visitCase_clause(self, ctx: Gallina.Case_clauseContext):
        patterns = []
        for pc in ctx.pattern():
            patterns.append(self.visit(pc))
        body = self.visit(ctx.term())
        return CaseClause(patterns, body)

    def visitAlias(self, ctx: Gallina.AliasContext):
        return Var(self.visit(ctx.var()))

    def visitBasicPatt(self, ctx: Gallina.BasicPattContext):
        pattern = []
        for nc in ctx.name():
            pattern.append(self.visit(nc))
        alias = None
        if ctx.alias() is not None:
            alias = self.visit(ctx.alias())
        return Pattern(pattern, alias)

    def visitEnclosedPatt(self, ctx: Gallina.EnclosedPattContext):
        return self.visit(ctx.pattern())

    def visitBinder_list(self, ctx: Gallina.Binder_listContext):
        binders = []
        for obc in ctx.open_binder():
            binders.append(self.visit(obc))
        return binders

    def visitOpen_binder(self, ctx: Gallina.Open_binderContext):
        names = []
        for nc in ctx.name():
            names.append(self.visit(nc))
        ty = self.visit(ctx.term())
        return Binder(names, ty)


class GoalErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []  # Store errors for later access

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        self.errors.append(f"Line {line}:{column} - {msg}")

    def reportAmbiguity(self, recognizer, dfa, start_index, stop_index, exact, ambig_alts, configs):
        msg = "Ambiguity error"
        self.errors.append(f"Line {recognizer.getTokenStream().get(start_index).line}:{recognizer.getTokenStream().get(start_index).column} - {msg}")

    def reportAttemptingFullContext(self, recognizer, dfa, start_index, stop_index, conflicting_alts, configs):
        msg = "Attempting full context error"
        self.errors.append(f"Line {recognizer.getTokenStream().get(start_index).line}:{recognizer.getTokenStream().get(start_index).column} - {msg}")

    def reportContextSensitivity(self, recognizer, dfa, start_index, stop_index, prediction, configs):
         msg = "Context sensitivity error"
         self.errors.append(f"Line {recognizer.getTokenStream().get(start_index).line}:{recognizer.getTokenStream().get(start_index).column} - {msg}")
