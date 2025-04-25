from abc import abstractmethod
from copy import deepcopy
from typing import List, Set, Optional


class Term:
    """
    Base class representing a term in Gallina's AST.
    """

    @abstractmethod
    def subst(self, var : 'Var', replacement : 'Var') -> 'Term':
        """
        Substitute occurrences of the specified variable with the replacement variable in the term.

        Args:
            var (Var): The variable to be replaced.
            replacement (Var): The variable that will replace occurrences of the `var`.

        Returns:
            Term: This after the substitution applied.

        Raises:
            NotImplementedError: If the method is not overridden by a subclass.
        """
        raise NotImplementedError('Not implemented')

    @abstractmethod
    def free_vars(self) -> Set['Var']:
        """
        Retrieve the set of free variables in the term.

        Returns:
            Set[Var]: A set containing all free variables present in the term.

        Raises:
            NotImplementedError: If the method is not overridden by a subclass.
        """
        raise NotImplementedError('Not implemented')

    @abstractmethod
    def alpha_equiv(self, other : 'Term') -> bool:
        """
        Check alpha equivalence with another term.

        Alpha equivalence means that the two terms are identical up to a renaming
        of bound variables.

        Args:
            other (Term): The other term to compare for alpha equivalence.

        Returns:
            bool: True if the terms are alpha equivalent, False otherwise.

        Raises:
            NotImplementedError: If the method is not overridden by a subclass.
        """
        raise NotImplementedError('Not implemented.')


class Var(Term):
    """
       Represents a variable term in Gallina's AST.
    """

    def __init__(self, name : str):
        """
        Initialize a variable with a given name.

        Args:
            name (str): The name of the variable.
        """
        self.__name = name

    def __repr__(self):
        return self.__name

    def __eq__(self, other) -> bool:
        """
        Check if another Var is equal to this one based on its name.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if the other object is a Var and has the same name.
        """
        return isinstance(other, Var) and self.__name == other.__name

    def __hash__(self) -> int:
        """
        Compute a hash value for the Var based on its name.

        Returns:
            int: The hash value of the name.
        """
        return hash(self.__name)

    def subst(self, var : 'Var', replacement : 'Var'):
        """
        Substitute this variable with a replacement if it matches the given variable.

        Args:
            var (Var): The variable to be replaced.
            replacement (Var): The variable that will replace.

        Returns:
            Term: A new Var instance representing the result of substitution,
                  either the replacement or the original Var.
        """
        if self.__name == var.__name:
            self.__name = replacement.__name
        return self

    def free_vars(self) -> Set['Var']:
        """
        Retrieve the set of free variables, which is the Var itself.

        Returns:
            Set[Var]: A set containing this variable as the only free variable.
        """
        return {self}

    def get_name(self) -> str:
        """
        Get the name of this variable.

        Returns:
            str: The name of the variable.
        """
        return self.__name

    def alpha_equiv(self, other : Term) -> bool:
        """
        Check alpha equivalence with another term.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if the other term is the same variable, False otherwise.
        """
        return self == other


class Pattern:
    """
    Represents a pattern in Gallina's AST, which may include a list of variable names
    and an optional alias. Patterns facilitate destructuring expressions.
    """

    def __init__(self, names : List[Var], alias : Optional[Var] = None):
        """
        Initialize a Pattern with given variable names and an optional alias.

        Args:
            names (List[Var]): The list of variable names in the pattern.
            alias (Var, optional): An optional alias for the pattern. Default is None.
        """
        self.__names = names
        self.__alias = alias

    def alpha_equiv(self, other: 'Pattern') -> bool:
        """
        Check alpha equivalence with another term.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if the terms are alpha equivalent, False otherwise.
        """
        return isinstance(other, Pattern) and self.__names[0] == other.__names[0]

    def __eq__(self, other) -> bool:
        """
        Check equality with another Pattern.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if the other object is a Pattern with the same names and alias.
        """
        return isinstance(other, Pattern) and (self.__names == other.__names) and (self.__alias == other.__alias)

    def __hash__(self) -> int:
        """
        Compute a hash value for the Pattern, based on its names and alias.

        Returns:
            int: The hash value.
        """
        return hash(self.__names[0])

    def get_bound_vars(self) -> Set[Var]:
        """
        Retrieve the set of bound variables in the pattern.

        Returns:
            Set[Var]: A set of variables that are bound by the pattern.
        """
        return set(self.__names[1:] + ([self.__alias] if self.has_alias() else []))

    def free_vars(self) -> Set[Var]:
        """
        Retrieve the set of free variables in the pattern.

        Returns:
            Set[Var]: A set containing the first variable if it is not a wildcard.
        """
        return {self.__names[0]} if self.__names and self.__names[0].get_name() != '_' else set()

    def get_names(self) -> List[Var]:
        """
        Get the list of variable names in the pattern.

        Returns:
            List[Var]: The list of variable names.
        """
        return self.__names

    def has_alias(self) -> bool:
        """
        Check if the pattern has an alias.

        Returns:
            bool: True if there is an alias, False otherwise.
        """
        return self.__alias is not None

    def get_alias(self) -> Var:
        """
        Get the alias of the pattern, if any.

        Returns:
            Var: The alias variable, or None if no alias exists.
        """
        return self.__alias


class CaseClause:
    """
    Represents a case clause in Gallina's AST, consisting of patterns
    and a resultant body expression when a match occurs.
    """

    def __init__(self, patterns : List[Pattern], body : Term):
        """
        Initialize the CaseClause with the given patterns and body.

        Args:
            patterns (List[Pattern]): The patterns that this clause matches against.
            body (Term): The body expression evaluated if the patterns match.
        """
        self.__patterns = patterns
        self.__body = body

    def __eq__(self, other) -> bool:
        """
        Check equality with another CaseClause by comparing patterns and body.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if the other object has identical patterns and body.
        """
        if not isinstance(other, CaseClause):
            return False
        return self.__patterns == other.__patterns and self.__body == other.__body

    def alpha_equiv(self, other: 'CaseClause') -> bool:
        """
        Check alpha equivalence with another term.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if terms are alpha equivalent according to bound variable renaming rules.
        """
        if len(self.__patterns) != len(other.__patterns):
            return False

        this_bvs = [bv for pattern in self.__patterns for bv in pattern.get_bound_vars() if bv.get_name() != '_']
        other_bvs = [bv for pattern in other.__patterns for bv in pattern.get_bound_vars() if bv.get_name() != '_']

        n = len(this_bvs)
        if n != len(other_bvs):
            return False

        this_bvs.sort(key=lambda x: x.get_name())
        other_bvs.sort(key=lambda x: x.get_name())
        this_body = deepcopy(self.__body)
        other_body = deepcopy(other.__body)

        for i in range(n):
            v = Var('SynthesizedVar#%d' % i)
            this_body.subst(this_bvs[i], v)
            other_body.subst(other_bvs[i], v)

        return this_body == other_body

    def __hash__(self) -> int:
        """
        Compute a hash for the CaseClause, based on its patterns.

        Returns:
            int: The hash value.
        """
        return hash(tuple(self.__patterns))

    def free_vars(self) -> Set[Var]:
        """
        Retrieve the set of free variables in the body, excluding those bound by patterns.

        Returns:
            Set[Var]: A set of free variables.
        """
        fvs = set(self.__body.free_vars())
        for pattern in self.__patterns:
            fvs.difference_update(bv for bv in pattern.get_bound_vars() if bv.get_name() != '_')
        return fvs

    def get_patterns(self) -> List[Pattern]:
        """
        Get the list of patterns in this case clause.

        Returns:
            List[Pattern]: The list of patterns.
        """
        return self.__patterns

    def get_body(self) -> Term:
        """
        Get the body term associated with this case clause.

        Returns:
            Term: The body term.
        """
        return self.__body


class MatchSubject:
    """
    Represents a match subject in Gallina's AST, optionally having a term alias and a pattern.
    """

    def __init__(self, term : Term, term_alias: Optional[Var] = None, pattern: Optional[Pattern] = None):
        """
        Initialize a MatchSubject with a term, optional alias, and pattern.

        Args:
            term (Term): The main term of the match subject.
            term_alias (Optional[Var]): An optional variable alias for the term.
            pattern (Optional[Pattern]): An optional pattern associated with the term.
        """
        self.__term = term
        self.__term_alias = term_alias
        self.__pattern = pattern

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if terms are alpha equivalent, False otherwise.
        """
        if not isinstance(other, MatchSubject):
            return False
        return self.__term.alpha_equiv(other.__term)

    def __eq__(self, other) -> bool:
        """
        Check equality with another MatchSubject.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if the other object has the same term, term alias, and pattern.
        """
        if not isinstance(other, MatchSubject):
            return False
        if (self.__term_alias is None) != (other.__term_alias is None):
            return False
        if self.__term_alias is not None and self.__term_alias != other.__term_alias:
            return False
        if (self.__pattern is None) != (other.__pattern is None):
            return False
        if self.__pattern is not None and self.__pattern != other.__pattern:
            return False
        return self.__term == other.__term

    def get_bound_vars(self) -> Set[Var]:
        """
        Retrieve the set of bound variables, including term alias and pattern bound variables.

        Returns:
            Set[Var]: A set of bound variables.
        """
        bvs = set()
        if self.__term_alias:
            bvs.add(self.__term_alias)
        if self.__pattern:
            bvs.update(self.__pattern.get_bound_vars())
        return bvs

    def free_vars(self) -> Set[Var]:
        """
        Retrieve the set of free variables in the term and pattern.

        Returns:
            Set[Var]: A set of free variables.
        """
        fvs = set(self.__term.free_vars())
        if self.__pattern:
            fvs.update(self.__pattern.free_vars())
        return fvs

    def get_subject_term(self) -> Term:
        """
        Get the term associated with the match subject.

        Returns:
            Term: The associated term.
        """
        return self.__term

    def has_term_alias(self) -> bool:
        """
        Check if there is a term alias.

        Returns:
            bool: True if a term alias exists, False otherwise.
        """
        return self.__term_alias is not None

    def get_term_alias(self) -> Optional[Var]:
        """
        Get the term alias, if it exists.

        Returns:
            Optional[Var]: The term alias or None if not present.
        """
        return self.__term_alias

    def has_pattern(self) -> bool:
        """
        Check if there is an associated pattern.

        Returns:
            bool: True if a pattern exists, False otherwise.
        """
        return self.__pattern is not None

    def get_pattern(self) -> Optional[Pattern]:
        """
        Get the associated pattern, if it exists.

        Returns:
            Optional[Pattern]: The associated pattern or None if not present.
        """
        return self.__pattern


class Match(Term):
    """
    Represents a match expression in Gallina's AST, including derived types,
    subjects, and potential return types.
    """

    def __init__(self, subjects : List[MatchSubject], cases : List[CaseClause], ret_ty: Optional[Term] = None):
        """
        Initialize a Match object with subjects, cases, and an optional return type.

        Args:
            subjects (List[MatchSubject]): The subjects for pattern matching.
            cases (List[CaseClause]): The case clauses considered for the match.
            ret_ty (Optional[Term]): The optional return type, if specified.
        """
        self.__subjects = subjects
        self.__ret_ty = ret_ty
        self.__cases = cases

    def __eq__(self, other) -> bool:
        """
        Check equality with another Match object.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if all subjects, cases, and return type match.
        """
        if not isinstance(other, Match):
            return False
        return (self.__subjects == other.__subjects and
                set(self.__cases) == set(other.__cases) and
                self.__ret_ty == other.__ret_ty)

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if the match constructs are alpha equivalent.
        """
        if not isinstance(other, Match):
            return False
        if len(self.__cases) != len(other.__cases):
            return False
        if len(self.__subjects) != len(other.__subjects):
            return False

        for c1 in self.__cases:
            for c2 in other.__cases:
               if not c1.alpha_equiv(c2):
                   return False

        this_bvs = [bv for subject in self.__subjects for bv in subject.get_bound_vars() if bv.get_name() != '_']
        other_bvs = [bv for subject in other.__subjects for bv in subject.get_bound_vars() if bv.get_name() != '_']

        n = len(this_bvs)
        if n != len(other_bvs):
            return False

        this_bvs.sort(key=lambda x: x.get_name())
        other_bvs.sort(key=lambda x: x.get_name())
        this_ret_ty = deepcopy(self.__ret_ty)
        other_ret_ty = deepcopy(other.__ret_ty)

        for i in range(n):
            v = Var('SynthesizedVar#%d' % i)
            this_ret_ty.subst(this_bvs[i], v)
            other_ret_ty.subst(other_bvs[i], v)

        return this_ret_ty == other_ret_ty

    def subst(self, var: Var, replacement: Var) -> Term:
        """
        Substitute occurrences of a variable with a replacement variable.

        Args:
            var (Var): The variable to replace.
            replacement (Var): The replacement variable.
        """
        bvs = set()
        for subject in self.__subjects:
            bvs.update(subject.get_bound_vars())
            subject.get_subject_term().subst(var, replacement)
        if var not in bvs:
            self.__ret_ty.subst(var, replacement)
        for cc in self.__cases:
            bvs = set()
            for p in cc.get_patterns():
                bvs.update(p.get_bound_vars())
            if var not in bvs:
                cc.get_body().subst(var, replacement)
        return self

    def free_vars(self) -> Set[Var]:
        """
        Calculate the free variables in the match expression.

        Returns:
            Set[Var]: A set of free variables.
        """
        fvs = {fv for subject in self.__subjects for fv in subject.free_vars()}
        if self.__ret_ty:
            fvs.update(self.__ret_ty.free_vars())
        for case in self.__cases:
            fvs.update(case.free_vars())
        return fvs

    def get_subjects(self) -> List[MatchSubject]:
        """
        Get the list of match subjects.

        Returns:
            List[MatchSubject]: The match subjects.
        """
        return self.__subjects

    def has_return_type(self) -> bool:
        """
        Check if the match expression has a return type.

        Returns:
            bool: True if a return type is specified, False otherwise.
        """
        return self.__ret_ty is not None

    def get_return_type(self) -> Optional[Term]:
        """
        Get the return type of the match expression.

        Returns:
            Optional[Term]: The return type, if specified.
        """
        return self.__ret_ty

    def get_cases(self) -> List[CaseClause]:
        """
        Get the case clauses of the match expression.

        Returns:
            List[CaseClause]: The case clauses.
        """
        return self.__cases


class Cond(Term):
    """
    Represents a conditional expression in Gallina's AST, consisting of a guard,
    optional alias, return type, and branches.
    """

    def __init__(self, guard : Term, ret_ty : Term, then_branch : Term,
                 else_branch : Term, guard_alias : Optional[Var] = None):
        """
        Initialize a Cond object with the given components.

        Args:
            guard (Term): The condition under which the then branch is executed.
            ret_ty (Term): The return type of the conditional.
            then_branch (Term): The term evaluated when the guard is true.
            else_branch (Term): The term evaluated when the guard is false.
            guard_alias (Var, optional): An optional alias for the guard value.
        """
        super().__init__()
        self.__guard = guard
        self.__ret_ty = ret_ty
        self.__then_branch = then_branch
        self.__else_branch = else_branch
        self.__guard_alias = guard_alias

    def __eq__(self, other) -> bool:
        """
        Check equality with another Cond object.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if the conditions, return types, branches, and optional guards are the same.
        """
        if not isinstance(other, Cond):
            return False
        if (self.__guard_alias is None) != (other.__guard_alias is None):
            return False
        if self.__guard_alias is not None and self.__guard_alias != other.__guard_alias:
            return False
        return (self.__guard == other.__guard and
                self.__ret_ty == other.__ret_ty and
                self.__then_branch == other.__then_branch and
                self.__else_branch == other.__else_branch)

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another conditional term.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if the terms are alpha equivalent, False otherwise.
        """
        if not isinstance(other, Cond):
            return False
        if (self.__guard_alias is None) != (other.__guard_alias is None):
            return False
        if self.__guard_alias is not None:
            v = Var('SynthesizedVar#0')
            this_ret_ty = deepcopy(self.__ret_ty).subst(self.__guard_alias, v)
            other_ret_ty = deepcopy(other.__ret_ty).subst(other.__guard_alias, v)
            if this_ret_ty != other_ret_ty:
                return False
        return (self.__guard.alpha_equiv(other.__guard)
                and self.__then_branch.alpha_equiv(other.__then_branch)
                and self.__else_branch.alpha_equiv(other.__else_branch))

    def free_vars(self) -> Set[Var]:
        """
        Retrieve the set of free variables within the conditional expression.

        Returns:
            Set[Var]: A set of free variables.
        """
        fvs = set()
        fvs.update(self.__ret_ty.free_vars())
        if self.__guard_alias is not None:
            fvs.discard(self.__guard_alias)
        fvs.update(self.__then_branch.free_vars())
        fvs.update(self.__else_branch.free_vars())
        return fvs

    def subst(self, var: Var, replacement: Var):
        """
        Perform substitution of a variable within the conditional's branches.

        Args:
            var (Var): The variable to be replaced.
            replacement (Var): The variable to replace `var`.
        """
        self.__then_branch.subst(var, replacement)
        self.__else_branch.subst(var, replacement)
        if self.__guard_alias != var:
            self.__ret_ty.subst(var, replacement)
        return self

    def get_guard(self) -> Term:
        """
        Get the guard term of the conditional.

        Returns:
            Term: The guard term.
        """
        return self.__guard

    def get_ret_ty(self) -> Term:
        """
        Get the return type of the conditional.

        Returns:
            Term: The return type term.
        """
        return self.__ret_ty

    def get_then_branch(self) -> Term:
        """
        Get the then-branch of the conditional.

        Returns:
            Term: The then-branch term.
        """
        return self.__then_branch

    def get_else_branch(self) -> Term:
        """
        Get the else-branch of the conditional.

        Returns:
            Term: The else-branch term.
        """
        return self.__else_branch

    def has_guard_alias(self) -> bool:
        """
        Check if the conditional has a guard alias.

        Returns:
            bool: True if there's a guard alias, False otherwise.
        """
        return self.__guard_alias is not None

    def get_guard_alias(self) -> Var:
        """
        Get the guard alias variable, if any.

        Returns:
            Var: The guard alias, or None if not present.
        """
        return self.__guard_alias


class Binder:
    """
    Represents a binder in Gallina's AST, consisting of a list of names and their associated type.

    A binder is generally used to denote the scope of variables in context of a type.
    """

    def __init__(self, names : List[Var], ty : Term):
        """
        Initialize a Binder object with variables and a corresponding type.

        Args:
            names (List[Var]): The names that are bound by this binder.
            ty (Term): The type associated with the bound variables.
        """
        self.__names = names
        self.__ty = ty

    def __eq__(self, other) -> bool:
        """
        Check equality with another Binder object.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if both binders have the same names and type.
        """
        if not isinstance(other, Binder):
            return False
        return self.__names == other.__names and self.__ty == other.__ty

    def get_names(self) -> List[Var]:
        """
        Get the variable names bound by this binder.

        Returns:
            List[Var]: The list of bound variable names.
        """
        return self.__names

    def get_type(self) -> Term:
        """
        Get the type associated with this binder.

        Returns:
            Term: The type of the bound variables.
        """
        return self.__ty

    def free_vars(self) -> Set[Var]:
        """
        Calculate the set of free variables in the type, excluding bound names.

        Returns:
            Set[Var]: The set of free variables.
        """
        fvs = set(self.__ty.free_vars())
        fvs.difference_update(self.__names)
        return fvs


class Fix(Term):
    """
    Represents a fixed-point (recursive) function in Gallina's AST, including its name,
    parameters, structure, return type, and body.
    """

    def __init__(self, name : Var, params : List[Binder], ret_ty : Term, body : Term, struct : Optional[Var] = None):
        """
        Initialize a Fix object representing a recursive function.

        Args:
            name (Var): The function or recursive binding name.
            params (List[Binder]): The list of parameters.
            ret_ty (Term): The return type of the function.
            body (Term): The body of the function.
            struct (Var, optional): The structural recursion parameter, if applicable.
        """
        super().__init__()
        self.__name = name
        self.__params = params
        self.__struct = struct
        self.__ret_ty = ret_ty
        self.__body = body

    def __eq__(self, other) -> bool:
        """
        Check equality with another Fix object.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if all elements (name, params, ret_ty, body, struct) are equal.
        """
        if not isinstance(other, Fix):
            return False
        if (self.__struct is None) != (other.__struct is None):
            return False
        if self.__struct is not None and self.__struct != other.__struct:
            return False
        return (self.__name == other.__name and
                self.__params == other.__params and
                self.__ret_ty == other.__ret_ty and
                self.__body == other.__body)

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term considering variable naming.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if terms are alpha equivalent, using consistent renaming of bound variables.
        """
        if not isinstance(other, Fix):
            return False
        if len(self.__params) != len(other.__params):
            return False
        if not self.__ret_ty.alpha_equiv(other.__ret_ty):
            return False

        # Collecting all bound variables
        this_bvs = [self.__name] + [pname for param in self.__params for pname in param.get_names() if pname.get_name() != '_']
        other_bvs = [other.__name] + [pname for param in other.__params for pname in param.get_names() if pname.get_name() != '_']

        if len(this_bvs) != len(other_bvs):
            return False

        this_bvs.sort(key=lambda x: x.get_name())
        other_bvs.sort(key=lambda x: x.get_name())
        this_body = deepcopy(self.__body)
        other_body = deepcopy(other.__body)
        for i in range(len(this_bvs)):
            v = Var('SynthesizedVar#%d' % i)
            this_body.subst(this_bvs[i], v)
            other_body.subst(other_bvs[i], v)

        return this_body == other_body

    def free_vars(self) -> Set[Var]:
        """
        Calculate the set of free variables in the Fix expression.

        Returns:
            Set[Var]: A set containing all free variables not bound within the Fix expression.
        """
        param_types_fvs = set()
        for p in self.__params:
            param_types_fvs.update(p.free_vars())
        for p in self.__params:
            for n in p.get_names():
                param_types_fvs.discard(n)
        body_fvs = set(self.__body.free_vars())
        body_fvs.discard(self.__name)
        for p in self.__params:
            for n in p.get_names():
                body_fvs.discard(n)
        fvs = set(self.__ret_ty.free_vars())
        fvs.update(param_types_fvs)
        fvs.update(body_fvs)
        return fvs

    def subst(self, var: 'Var', replacement: 'Var') -> Term:
        """
        Substitute occurrences of a variable with a replacement variable within the Fix expression.

        Args:
            var (Var): The variable to replace.
            replacement (Var): The variable to use as replacement.
        """
        if self.__name == var:
            return
        params = set()
        for p in self.__params:
            params.update(p.get_names())
        if var in params:
            return
        for p in self.__params:
            p.get_type().subst(var, replacement)
        self.__ret_ty.subst(var, replacement)
        self.__body.subst(var, replacement)
        return self

    def get_name(self) -> Var:
        """
        Get the name of the Fix function.

        Returns:
            Var: The name variable of the Fix.
        """
        return self.__name

    def get_params(self) -> List[Binder]:
        """
        Get the parameters of the Fix function.

        Returns:
            List[Binder]: The list of parameter binders.
        """
        return self.__params

    def has_struct(self) -> bool:
        """
        Check if there is a structural recursion parameter.

        Returns:
            bool: True if a structural recursion parameter is specified, False otherwise.
        """
        return self.__struct is not None

    def get_struct(self) -> Var:
        """
        Get the structural recursion parameter, if available.

        Returns:
            Var: The structural recursion variable, or None if not present.
        """
        return self.__struct

    def get_return_type(self) -> Term:
        """
        Get the return type of the Fix function.

        Returns:
            Term: The return type term.
        """
        return self.__ret_ty

    def get_body(self) -> Term:
        """
        Get the body of the Fix function.

        Returns:
            Term: The body term.
        """
        return self.__body


class Sort(Term):
    """
    Represents a sort in Gallina's AST, defined primarily by its name and an optional annotation.
    """

    def __init__(self, name : str, annotation : Optional[str] = None):
        """
        Initialize a Sort with a specified name and optional annotation.

        Args:
            name (str): The name of the sort.
            annotation (str, optional): An optional annotation for the sort.
        """
        self.__name = name
        self.__annotation = annotation

    def __eq__(self, other) -> bool:
        """
        Check if this Sort is equal to another, considering name and annotation.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if the other Sort has the same name and annotation.
        """
        if not isinstance(other, Sort):
            return False
        return self.__name == other.__name and self.__annotation == other.__annotation

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term, which for sorts is identical to equality.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if the terms are equivalent.
        """
        return self == other

    def subst(self, var: Var, replacement: Var) -> Term:
        """
        Perform substitution, which for Sorts is a no-op as sorts do not contain variables.

        Args:
            var (Var): The variable to replace.
            replacement (Var): The replacement variable.
        """
        return self

    def free_vars(self) -> Set[Var]:
        """
        Determine the set of free variables, which is always empty for Sorts.

        Returns:
            Set[Var]: An empty set, since sorts contain no variables.
        """
        return set()

    def get_name(self) -> str:
        """
        Retrieve the full name of the sort, including any annotation.

        Returns:
            str: The full name with annotation if present.
        """
        return f"{self.__name}{self.__annotation or ''}"


class TermAbstraction(Term):
    """
    Represents a term abstraction in Gallina's AST, effectively a lambda abstraction with
    a variable, its type, and a body term.
    """

    def __init__(self, var : Var, var_type : Term, body : Term):
        """
        Initialize a TermAbstraction with a variable, its type, and body.

        Args:
            var (Var): The variable being abstracted.
            var_type (Term): The type of the bound variable.
            body (Term): The body of the abstraction.
        """
        self._var = var
        self._var_type = var_type
        self._body = body

    def __eq__(self, other) -> bool:
        """
        Check equality with another TermAbstraction object.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if both abstractions have the same variable type and body.
        """
        if not isinstance(other, TermAbstraction):
            return False
        return self._var_type == other._var_type and self._body == other._body

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term, considering variable renaming.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if the terms are alpha equivalent, considering renaming of bound variables.
        """
        if not isinstance(other, TermAbstraction):
            return False
        if not self._var_type.alpha_equiv(other._var_type):
            return False

        # If variables are the same, directly compare bodies
        if self._var == other._var:
            return self._body.alpha_equiv(other._body)

        # Otherwise, perform substitution to compare under alpha equivalence
        synthesized_var = Var('SynthesizedVar#0')
        this_body = deepcopy(self._body).subst(self._var, synthesized_var)
        other_body = deepcopy(other._body).subst(other._var, synthesized_var)
        return this_body == other_body

    def subst(self, var: Var, replacement: Var) -> Term:
        """
        Substitute occurrences of a variable in the term abstraction, respecting scope rules.

        Args:
            var (Var): The variable to replace.
            replacement (Var): The variable to replace var with.
        """
        self._var_type.subst(var, replacement)
        if var != self._var:
            self._body.subst(var, replacement)
        return self

    def free_vars(self) -> Set[Var]:
        """
        Calculate the set of free variables in the term abstraction.

        Returns:
            Set[Var]: A set of free variables, excluding the bound variable.
        """
        fvs = self._body.free_vars()
        fvs.discard(self._var)  # Remove the bound variable from free variables
        fvs.update(self._var_type.free_vars())
        return fvs

    def get_body(self):
        return self._body

class Fun(TermAbstraction):
    """
    Represents a function abstraction in Gallina's AST. A function abstraction is a specific form of term abstraction
    where the terms are interpreted as functions.
    """

    def __init__(self, param : Var, param_type : Term, body : Term):
        """
        Initialize a function abstraction with a parameter, its type, and the function body.

        Args:
            param (Var): The function parameter.
            param_type (Term): The type of the function parameter.
            body (Term): The body of the function.
        """
        super().__init__(param, param_type, body)

    @staticmethod
    def build(params: List[Binder], body: Term) -> 'Fun':
        """
        Build a nested sequence of function abstractions from a list of parameter binders and a body.

        Args:
            params (List[Binder]): A list of binders representing parameters and their types.
            body (Term): The body term of the function.

        Returns:
            Fun: A nested function abstraction where each layer corresponds to a parameter.
        """
        fun = body
        # Construct the nested function in a reverse order: outer params applied last
        for param in reversed(params):
            for name in reversed(param.get_names()):
                fun = Fun(name, param.get_type(), fun)
        return fun

    def __eq__(self, other) -> bool:
        """
        Check equality with another Fun object using the TermAbstraction equality logic.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if both function terms are equal per TermAbstraction's logic.
        """
        return isinstance(other, Fun) and super().__eq__(other)

    def alpha_equiv(self, other: Term) -> bool:
        return isinstance(other, Fun) and super().alpha_equiv(other)


class Product(TermAbstraction):
    """
    Represents a dependent product type (similar to a Pi type) in Gallina's AST. It extends
    the concept of a function abstraction to types, allowing dependent typing based on parameter values.
    """

    def __init__(self, param: Var, param_type: Term, body: Term):
        """
        Initializes the Product with a parameter, its type, and the body of the product.

        Args:
            param (Var): The parameter being abstracted.
            param_type (Term): The type of the parameter.
            body (Term): The body of the product type.
        """
        super().__init__(param, param_type, body)

    @staticmethod
    def build(params: List[Binder], body: Term) -> 'Product':
        """
        Build a nested product type from a list of parameter binders and a type body.

        Args:
            params (List[Binder]): A list of parameter binders each containing parameter names and their types.
            body (Term): The body term of the product type.

        Returns:
            Product: A nested product type abstraction.
        """
        product = body
        # Construct nested products where outer params are applied last
        for param in reversed(params):
            for name in reversed(param.get_names()):
                product = Product(name, param.get_type(), product)
        return product

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term, specific to Product terms.

        Args:
            other (Term): The term to check for alpha equivalence.

        Returns:
            bool: True if products are alpha equivalent, utilizing TermAbstraction's logic.
        """
        return isinstance(other, Product) and super().alpha_equiv(other)

    def __eq__(self, other) -> bool:
        """
        Check equality with another Product using the TermAbstraction equality logic.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if both products are equal per TermAbstraction's logic.
        """
        return isinstance(other, Product) and super().__eq__(other)


class Let(TermAbstraction):
    """
    Represents a 'let' binding abstraction in Gallina's AST, encapsulating a variable,
    its type, its definition, and the body in which it is used.
    """

    def __init__(self, var : Var, var_type : Term, var_def : Term, body : Term):
        """
        Initialize a Let binding with a variable, its type, its definition, and a body.

        Args:
            var (Var): The variable that is bound.
            var_type (Term): The type of the variable.
            var_def (Term): The term defining the variable.
            body (Term): The body in which the variable is used.
        """
        super().__init__(var, var_type, body)
        self.__var_def = var_def

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term, specific to Let bindings.

        Args:
            other (Term): The term to check for alpha equivalence.

        Returns:
            bool: True if let-bindings are alpha equivalent, using TermAbstraction's logic.
        """
        return isinstance(other, Let) and super().alpha_equiv(other) and self.__var_def.alpha_equiv(other.__var_def)

    def __eq__(self, other) -> bool:
        """
        Check equality with another Let binding using the TermAbstraction equality logic.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if both Lets are equal per TermAbstraction's logic.
        """
        return isinstance(other, Let) and super().__eq__(other) and self.__var_def == other.__var_def

    def subst(self, var: Var, replacement: Var) -> Term:
        """
        Substitute occurrences of a variable within the Let binding's definition and body.

        Args:
            var (Var): The variable to replace.
            replacement (Var): The replacement variable.
        """
        # Substitute in var_type and body
        super().subst(var, replacement)
        # Substitute in var_def
        self.__var_def.subst(var, replacement)
        return self

    def free_vars(self) -> Set[Var]:
        """
        Calculate the set of free variables in the Let binding.

        Returns:
            Set[Var]: A set of free variables, excluding the bound variable.
        """
        fvs = super().free_vars()
        fvs.update(self.__var_def.free_vars())
        return fvs


class Cast(Term):
    """
    Represents a cast operation in Gallina's AST, including the term to be cast and the target type.
    """

    def __init__(self, term : Term, term_type : Term):
        """
        Initialize a Cast with a term and the target type for the cast.

        Args:
            term (Term): The term being cast.
            term_type (Term): The target type of the cast.
        """
        super().__init__()
        self.__term = term
        self.__term_type = term_type

    def __eq__(self, other) -> bool:
        """
        Check equality with another Cast object.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if both cast terms and types are equal.
        """
        if not isinstance(other, Cast):
            return False
        return self.__term == other.__term and self.__term_type == other.__term_type

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term, specific to Cast terms.

        Args:
            other (Term): The term to check for alpha equivalence.

        Returns:
            bool: True if the terms are alpha equivalent.
        """
        if not isinstance(other, Cast):
            return False
        return self.__term.alpha_equiv(other.__term) and self.__term_type.alpha_equiv(other.__term_type)

    def subst(self, var: Var, replacement: Var) -> 'Cast':
        """
        Substitute occurrences of a variable within the Cast's term and type.

        Args:
            var (Var): The variable to replace.
            replacement (Var): The replacement variable.

        Returns:
            Cast: The updated Cast object with substitutions applied.
        """
        self.__term.subst(var, replacement)
        self.__term_type.subst(var, replacement)
        return self

    def free_vars(self) -> Set[Var]:
        """
        Calculate the set of free variables in the Cast expression.

        Returns:
            Set[Var]: A set of free variables from the term and its type.
        """
        return self.__term.free_vars() | self.__term_type.free_vars()


class App(Term):
    """
    Represents an application in Gallina's AST, consisting of a function applied to an argument.
    """

    def __init__(self, func : Term, arg : Term):
        """
        Initializes an application with the function and the argument it is applied to.

        Args:
            func (Term): The function term in the application.
            arg (Term): The argument term in the application.
        """
        super().__init__()
        self.__func = func
        self.__arg = arg

    def alpha_equiv(self, other: Term) -> bool:
        """
        Check alpha equivalence with another term.

        Args:
            other (Term): The term to compare for alpha equivalence.

        Returns:
            bool: True if both applications are alpha equivalent.
        """
        if not isinstance(other, App):
            return False
        return self.__func.alpha_equiv(other.__func) and self.__arg.alpha_equiv(other.__arg)

    def __eq__(self, other) -> bool:
        """
        Check equality with another App object.

        Args:
            other: The other object to compare.

        Returns:
            bool: True if both applications have the same function and argument.
        """
        if not isinstance(other, App):
            return False
        return self.__func == other.__func and self.__arg == other.__arg

    def subst(self, var: Var, replacement: Var) -> Term:
        """
        Substitute occurrences of a variable within the application.

        Args:
            var (Var): The variable to replace.
            replacement (Var): The replacement variable.
        """
        self.__func.subst(var, replacement)
        self.__arg.subst(var, replacement)
        return self

    def free_vars(self) -> Set[Var]:
        """
        Calculate the set of free variables in the application.

        Returns:
            Set[Var]: A set containing free variables from the function and argument.
        """
        return self.__func.free_vars() | self.__arg.free_vars()

    def get_func(self) -> Term:
        """
        Get the function term of the application.

        Returns:
            Term: The function term.
        """
        return self.__func

    def get_arg(self) -> Term:
        """
        Get the argument term of the application.

        Returns:
            Term: The argument term.
        """
        return self.__arg
