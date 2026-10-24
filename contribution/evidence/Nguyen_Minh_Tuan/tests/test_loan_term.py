"""B3.1 — calc_max_loan_term + 3 edge case + validate_loan_term."""
import unittest

from finflow.fin_assumptions import FIN_ASSUMPTIONS
from finflow.loan_calc import simulate
from finflow.loan_term import LoanTermError, calc_max_loan_term, validate_loan_term


class TestCalcMaxLoanTerm(unittest.TestCase):
    def test_single_borrower_bank_cap_binds(self):
        r = calc_max_loan_term(30)
        self.assertEqual(r["max_term_by_age_months"], (75 - 30) * 12)
        self.assertEqual(r["final_max_term_months"], 360)
        self.assertEqual(r["binding_constraint"], "bank")

    def test_couple_uses_older_borrower(self):
        r = calc_max_loan_term(30, 50)
        self.assertEqual(r["older_borrower_age"], 50)
        self.assertEqual(r["final_max_term_months"], 300)
        self.assertEqual(r["binding_constraint"], "age")
        self.assertEqual(calc_max_loan_term(50, 30)["final_max_term_months"], 300)  # thứ tự không quan trọng

    def test_bank_cap_is_single_parameter(self):
        self.assertEqual(calc_max_loan_term(30, None, 35 * 12)["final_max_term_months"], 420)
        self.assertEqual(FIN_ASSUMPTIONS["bank_max_term_months"], 360)

    def test_edge_case_1_age_at_or_above_limit(self):
        for age in (75, 80):
            with self.assertRaises(LoanTermError) as cm:
                calc_max_loan_term(age)
            self.assertEqual(cm.exception.code, "AGE_LIMIT")
        with self.assertRaises(LoanTermError) as cm:
            calc_max_loan_term(40, 75)  # người trẻ + người 75 tuổi → vẫn chặn
        self.assertEqual(cm.exception.code, "AGE_LIMIT")

    def test_edge_case_2_term_not_above_grace(self):
        for age in (73, 74):  # (75-73)*12 = 24 ≤ 24 ; 12 ≤ 24
            with self.assertRaises(LoanTermError) as cm:
                calc_max_loan_term(age)
            self.assertEqual(cm.exception.code, "TERM_NOT_ABOVE_GRACE")
        self.assertEqual(calc_max_loan_term(72)["final_max_term_months"], 36)

    def test_max_age_parameter_for_mb_confirmation(self):
        self.assertEqual(calc_max_loan_term(45, max_age_at_maturity=70)["final_max_term_months"], 300)
        self.assertEqual(calc_max_loan_term(45)["final_max_term_months"], 360)

    def test_invalid_ages_rejected(self):
        for bad in (17, "30", 30.5, True, float("nan"), None):
            with self.assertRaises(LoanTermError):
                calc_max_loan_term(bad)
        self.assertEqual(calc_max_loan_term(30.0)["older_borrower_age"], 30)


class TestValidateLoanTerm(unittest.TestCase):
    def test_bounds(self):
        self.assertEqual(validate_loan_term(360, 360), 360)
        self.assertEqual(validate_loan_term(25, 360), 25)
        for bad, code in ((361, "TERM_ABOVE_MAX"), (24, "TERM_NOT_ABOVE_GRACE"), (300.5, "TERM_INVALID"), ("360", "TERM_INVALID")):
            with self.assertRaises(LoanTermError) as cm:
                validate_loan_term(bad, 360)
            self.assertEqual(cm.exception.code, code)


class TestEdgeCase3NoGlobalConstant(unittest.TestCase):
    def test_no_loan_term_constant_in_assumptions(self):
        self.assertNotIn("Loan_term_months", FIN_ASSUMPTIONS)

    def test_engine_requires_loan_term_parameter(self):
        inputs = dict(purchase_price=5e9, savings=1.5e9, income_1=40e6, living_cost=10e6, monthly_rent=15e6)
        with self.assertRaises(TypeError):
            simulate(inputs, None)
        self.assertEqual(simulate(inputs, 240)["loan_term_months"], 240)


if __name__ == "__main__":
    unittest.main()
