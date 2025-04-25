# Generated from Gallina.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .Gallina import Gallina
else:
    from Gallina import Gallina

# This class defines a complete generic visitor for a parse tree produced by Gallina.

class GallinaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by Gallina#goal.
    def visitGoal(self, ctx:Gallina.GoalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#ExVar.
    def visitExVar(self, ctx:Gallina.ExVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Cast.
    def visitCast(self, ctx:Gallina.CastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Parenthesis.
    def visitParenthesis(self, ctx:Gallina.ParenthesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Cond.
    def visitCond(self, ctx:Gallina.CondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Variable.
    def visitVariable(self, ctx:Gallina.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Fix.
    def visitFix(self, ctx:Gallina.FixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Sort.
    def visitSort(self, ctx:Gallina.SortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Product.
    def visitProduct(self, ctx:Gallina.ProductContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Let.
    def visitLet(self, ctx:Gallina.LetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Application.
    def visitApplication(self, ctx:Gallina.ApplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Fun.
    def visitFun(self, ctx:Gallina.FunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#Match.
    def visitMatch(self, ctx:Gallina.MatchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#subject_list.
    def visitSubject_list(self, ctx:Gallina.Subject_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#subject.
    def visitSubject(self, ctx:Gallina.SubjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#case_list.
    def visitCase_list(self, ctx:Gallina.Case_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#case_clause.
    def visitCase_clause(self, ctx:Gallina.Case_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#BasicPatt.
    def visitBasicPatt(self, ctx:Gallina.BasicPattContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#EnclosedPatt.
    def visitEnclosedPatt(self, ctx:Gallina.EnclosedPattContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#alias.
    def visitAlias(self, ctx:Gallina.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#binder_list.
    def visitBinder_list(self, ctx:Gallina.Binder_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#open_binder.
    def visitOpen_binder(self, ctx:Gallina.Open_binderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#sort_term.
    def visitSort_term(self, ctx:Gallina.Sort_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#universe_annot.
    def visitUniverse_annot(self, ctx:Gallina.Universe_annotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#universe_expr.
    def visitUniverse_expr(self, ctx:Gallina.Universe_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#name.
    def visitName(self, ctx:Gallina.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#evar_term.
    def visitEvar_term(self, ctx:Gallina.Evar_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Gallina#var.
    def visitVar(self, ctx:Gallina.VarContext):
        return self.visitChildren(ctx)



del Gallina