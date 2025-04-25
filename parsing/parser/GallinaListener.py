# Generated from Gallina.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .Gallina import Gallina
else:
    from Gallina import Gallina

# This class defines a complete listener for a parse tree produced by Gallina.
class GallinaListener(ParseTreeListener):

    # Enter a parse tree produced by Gallina#goal.
    def enterGoal(self, ctx:Gallina.GoalContext):
        pass

    # Exit a parse tree produced by Gallina#goal.
    def exitGoal(self, ctx:Gallina.GoalContext):
        pass


    # Enter a parse tree produced by Gallina#ExVar.
    def enterExVar(self, ctx:Gallina.ExVarContext):
        pass

    # Exit a parse tree produced by Gallina#ExVar.
    def exitExVar(self, ctx:Gallina.ExVarContext):
        pass


    # Enter a parse tree produced by Gallina#Cast.
    def enterCast(self, ctx:Gallina.CastContext):
        pass

    # Exit a parse tree produced by Gallina#Cast.
    def exitCast(self, ctx:Gallina.CastContext):
        pass


    # Enter a parse tree produced by Gallina#Parenthesis.
    def enterParenthesis(self, ctx:Gallina.ParenthesisContext):
        pass

    # Exit a parse tree produced by Gallina#Parenthesis.
    def exitParenthesis(self, ctx:Gallina.ParenthesisContext):
        pass


    # Enter a parse tree produced by Gallina#Cond.
    def enterCond(self, ctx:Gallina.CondContext):
        pass

    # Exit a parse tree produced by Gallina#Cond.
    def exitCond(self, ctx:Gallina.CondContext):
        pass


    # Enter a parse tree produced by Gallina#Variable.
    def enterVariable(self, ctx:Gallina.VariableContext):
        pass

    # Exit a parse tree produced by Gallina#Variable.
    def exitVariable(self, ctx:Gallina.VariableContext):
        pass


    # Enter a parse tree produced by Gallina#Fix.
    def enterFix(self, ctx:Gallina.FixContext):
        pass

    # Exit a parse tree produced by Gallina#Fix.
    def exitFix(self, ctx:Gallina.FixContext):
        pass


    # Enter a parse tree produced by Gallina#Sort.
    def enterSort(self, ctx:Gallina.SortContext):
        pass

    # Exit a parse tree produced by Gallina#Sort.
    def exitSort(self, ctx:Gallina.SortContext):
        pass


    # Enter a parse tree produced by Gallina#Product.
    def enterProduct(self, ctx:Gallina.ProductContext):
        pass

    # Exit a parse tree produced by Gallina#Product.
    def exitProduct(self, ctx:Gallina.ProductContext):
        pass


    # Enter a parse tree produced by Gallina#Let.
    def enterLet(self, ctx:Gallina.LetContext):
        pass

    # Exit a parse tree produced by Gallina#Let.
    def exitLet(self, ctx:Gallina.LetContext):
        pass


    # Enter a parse tree produced by Gallina#Application.
    def enterApplication(self, ctx:Gallina.ApplicationContext):
        pass

    # Exit a parse tree produced by Gallina#Application.
    def exitApplication(self, ctx:Gallina.ApplicationContext):
        pass


    # Enter a parse tree produced by Gallina#Fun.
    def enterFun(self, ctx:Gallina.FunContext):
        pass

    # Exit a parse tree produced by Gallina#Fun.
    def exitFun(self, ctx:Gallina.FunContext):
        pass


    # Enter a parse tree produced by Gallina#Match.
    def enterMatch(self, ctx:Gallina.MatchContext):
        pass

    # Exit a parse tree produced by Gallina#Match.
    def exitMatch(self, ctx:Gallina.MatchContext):
        pass


    # Enter a parse tree produced by Gallina#subject_list.
    def enterSubject_list(self, ctx:Gallina.Subject_listContext):
        pass

    # Exit a parse tree produced by Gallina#subject_list.
    def exitSubject_list(self, ctx:Gallina.Subject_listContext):
        pass


    # Enter a parse tree produced by Gallina#subject.
    def enterSubject(self, ctx:Gallina.SubjectContext):
        pass

    # Exit a parse tree produced by Gallina#subject.
    def exitSubject(self, ctx:Gallina.SubjectContext):
        pass


    # Enter a parse tree produced by Gallina#case_list.
    def enterCase_list(self, ctx:Gallina.Case_listContext):
        pass

    # Exit a parse tree produced by Gallina#case_list.
    def exitCase_list(self, ctx:Gallina.Case_listContext):
        pass


    # Enter a parse tree produced by Gallina#case_clause.
    def enterCase_clause(self, ctx:Gallina.Case_clauseContext):
        pass

    # Exit a parse tree produced by Gallina#case_clause.
    def exitCase_clause(self, ctx:Gallina.Case_clauseContext):
        pass


    # Enter a parse tree produced by Gallina#BasicPatt.
    def enterBasicPatt(self, ctx:Gallina.BasicPattContext):
        pass

    # Exit a parse tree produced by Gallina#BasicPatt.
    def exitBasicPatt(self, ctx:Gallina.BasicPattContext):
        pass


    # Enter a parse tree produced by Gallina#EnclosedPatt.
    def enterEnclosedPatt(self, ctx:Gallina.EnclosedPattContext):
        pass

    # Exit a parse tree produced by Gallina#EnclosedPatt.
    def exitEnclosedPatt(self, ctx:Gallina.EnclosedPattContext):
        pass


    # Enter a parse tree produced by Gallina#alias.
    def enterAlias(self, ctx:Gallina.AliasContext):
        pass

    # Exit a parse tree produced by Gallina#alias.
    def exitAlias(self, ctx:Gallina.AliasContext):
        pass


    # Enter a parse tree produced by Gallina#binder_list.
    def enterBinder_list(self, ctx:Gallina.Binder_listContext):
        pass

    # Exit a parse tree produced by Gallina#binder_list.
    def exitBinder_list(self, ctx:Gallina.Binder_listContext):
        pass


    # Enter a parse tree produced by Gallina#open_binder.
    def enterOpen_binder(self, ctx:Gallina.Open_binderContext):
        pass

    # Exit a parse tree produced by Gallina#open_binder.
    def exitOpen_binder(self, ctx:Gallina.Open_binderContext):
        pass


    # Enter a parse tree produced by Gallina#sort_term.
    def enterSort_term(self, ctx:Gallina.Sort_termContext):
        pass

    # Exit a parse tree produced by Gallina#sort_term.
    def exitSort_term(self, ctx:Gallina.Sort_termContext):
        pass


    # Enter a parse tree produced by Gallina#universe_annot.
    def enterUniverse_annot(self, ctx:Gallina.Universe_annotContext):
        pass

    # Exit a parse tree produced by Gallina#universe_annot.
    def exitUniverse_annot(self, ctx:Gallina.Universe_annotContext):
        pass


    # Enter a parse tree produced by Gallina#universe_expr.
    def enterUniverse_expr(self, ctx:Gallina.Universe_exprContext):
        pass

    # Exit a parse tree produced by Gallina#universe_expr.
    def exitUniverse_expr(self, ctx:Gallina.Universe_exprContext):
        pass


    # Enter a parse tree produced by Gallina#name.
    def enterName(self, ctx:Gallina.NameContext):
        pass

    # Exit a parse tree produced by Gallina#name.
    def exitName(self, ctx:Gallina.NameContext):
        pass


    # Enter a parse tree produced by Gallina#evar_term.
    def enterEvar_term(self, ctx:Gallina.Evar_termContext):
        pass

    # Exit a parse tree produced by Gallina#evar_term.
    def exitEvar_term(self, ctx:Gallina.Evar_termContext):
        pass


    # Enter a parse tree produced by Gallina#var.
    def enterVar(self, ctx:Gallina.VarContext):
        pass

    # Exit a parse tree produced by Gallina#var.
    def exitVar(self, ctx:Gallina.VarContext):
        pass



del Gallina