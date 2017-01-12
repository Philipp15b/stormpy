import pycarl
import stormpy
import stormpy.logic

class TestFormulas:

    def test_probability_formula(self):
        formula_str = "P=? [F \"one\"]"
        properties = stormpy.parse_properties(formula_str)
        formula = properties[0].raw_formula
        assert type(formula) == stormpy.logic.ProbabilityOperator
        assert len(properties) == 1
        assert str(formula) == formula_str

    def test_reward_formula(self):
        formula_str = "R=? [F \"one\"]"
        properties = stormpy.parse_properties(formula_str)
        formula = properties[0].raw_formula
        assert type(formula) == stormpy.logic.RewardOperator
        assert len(properties) == 1
        assert str(formula) == "R[exp]=? [F \"one\"]"

    def test_formula_list(self):
        formulas = []
        prop = "=? [F \"one\"]"
        forms = stormpy.parse_properties("P" + prop)
        formulas.append(forms[0].raw_formula)
        forms = stormpy.parse_properties("R" + prop)
        formulas.append(forms[0].raw_formula)
        assert len(formulas) == 2
        assert str(formulas[0]) == "P" + prop
        assert str(formulas[1]) == "R[exp]" + prop

    def test_bounds(self):
        prop = "P=? [F \"one\"]"
        formula = stormpy.parse_properties(prop)[0].raw_formula
        assert not formula.has_bound
        prop = "P<0.4 [F \"one\"]"
        formula = stormpy.parse_properties(prop)[0].raw_formula
        assert formula.has_bound
        assert formula.threshold == pycarl.Rational("0.4")
        assert formula.comparison_type == stormpy.logic.ComparisonType.LESS

    def test_set_bounds(self):
        prop = "P<0.4 [F \"one\"]"
        formula = stormpy.parse_properties(prop)[0].raw_formula
        formula.threshold = pycarl.Rational("0.2")
        formula.comparison_type = stormpy.logic.ComparisonType.GEQ
        assert formula.threshold == pycarl.Rational("0.2")
        assert formula.comparison_type == stormpy.logic.ComparisonType.GEQ
        assert str(formula) == "P>=1/5 [F \"one\"]"
