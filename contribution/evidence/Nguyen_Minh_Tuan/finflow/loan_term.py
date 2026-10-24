"""B3.1 — Loan term theo tuổi (FINAL PLAN cập nhật 2026-09-25 §B3.1; Spec 2026-09-25 §9).

    older_borrower_age      = max(age_1, age_2) nếu có age_2, ngược lại age_1
    max_term_by_age_months  = (MAX_AGE_AT_MATURITY − older_borrower_age) × 12
    final_max_term_months   = min(max_term_by_age_months, bank_max_term_months)

3 edge case bắt buộc:
  (1) older_borrower_age ≥ tuổi tối đa khi đáo hạn → chặn, báo "không đủ tuổi để vay" (không để ra số âm)
  (2) final_max_term_months ≤ grace_period_months (24) → chặn
  (3) loan term KHÔNG còn là hằng số: loan_calc.simulate() bắt buộc nhận loan_term_months làm tham số
Bổ sung (ngoài plan, để tránh input rác): tuổi phải là số nguyên ≥ 18.
"""
import math

from .fin_assumptions import FIN_ASSUMPTIONS


class LoanTermError(ValueError):
    """Lỗi nghiệp vụ có mã (code) để UI hiển thị + message tiếng Việt."""

    def __init__(self, code, message, **details):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details


def _clean_age(age, label, min_age):
    if isinstance(age, bool) or not isinstance(age, (int, float)):
        raise LoanTermError("AGE_INVALID", f"{label} phải là số nguyên (tuổi tròn năm), nhận {age!r}")
    if isinstance(age, float):
        if math.isnan(age) or math.isinf(age) or not age.is_integer():
            raise LoanTermError("AGE_INVALID", f"{label} phải là số nguyên (tuổi tròn năm), nhận {age!r}")
        age = int(age)
    if age < min_age:
        raise LoanTermError("AGE_BELOW_MIN", f"{label} = {age}: người vay phải từ đủ {min_age} tuổi")
    return age


def calc_max_loan_term(age_1, age_2=None, bank_max_term_months=None, *, max_age_at_maturity=None,
                       grace_period_months=None, min_age=None):
    """Trả dict {older_borrower_age, max_term_by_age_months, max_term_by_bank_months, final_max_term_months,
    binding_constraint, grace_period_months}; ném LoanTermError khi rơi vào edge case."""
    a = FIN_ASSUMPTIONS
    bank_max = a["bank_max_term_months"] if bank_max_term_months is None else int(bank_max_term_months)
    max_age = a["max_borrower_age_at_maturity"] if max_age_at_maturity is None else int(max_age_at_maturity)
    grace = a["grace_period_months"] if grace_period_months is None else int(grace_period_months)
    min_age = a["min_borrower_age"] if min_age is None else int(min_age)

    a1 = _clean_age(age_1, "age_1", min_age)
    a2 = None if age_2 is None else _clean_age(age_2, "age_2", min_age)
    older = a1 if a2 is None else max(a1, a2)

    if older >= max_age:  # edge case 1
        raise LoanTermError("AGE_LIMIT",
                            f"Không đủ tuổi để vay: người vay lớn tuổi nhất {older} tuổi, "
                            f"tuổi tối đa khi đáo hạn là {max_age}.",
                            older_borrower_age=older, max_age_at_maturity=max_age)
    by_age = (max_age - older) * 12
    final = min(by_age, bank_max)
    if final <= grace:  # edge case 2
        raise LoanTermError("TERM_NOT_ABOVE_GRACE",
                            f"Thời hạn vay tối đa tính được ({final} tháng) không lớn hơn thời gian ân hạn gốc "
                            f"({grace} tháng) — không thể lập lịch trả gốc.",
                            final_max_term_months=final, grace_period_months=grace)
    return {
        "older_borrower_age": older,
        "max_term_by_age_months": by_age,
        "max_term_by_bank_months": bank_max,
        "final_max_term_months": final,
        "binding_constraint": "age" if by_age < bank_max else "bank",
        "grace_period_months": grace,
    }


def validate_loan_term(loan_term_months, final_max_term_months, grace_period_months=None):
    """Loan term user chọn phải là số tháng nguyên, > ân hạn và ≤ final_max_term_months."""
    grace = FIN_ASSUMPTIONS["grace_period_months"] if grace_period_months is None else int(grace_period_months)
    bad_type = isinstance(loan_term_months, bool) or not isinstance(loan_term_months, (int, float))
    if bad_type or (isinstance(loan_term_months, float) and not loan_term_months.is_integer()):
        raise LoanTermError("TERM_INVALID", f"loan_term phải là số tháng nguyên, nhận {loan_term_months!r}")
    lt = int(loan_term_months)
    if lt <= grace:
        raise LoanTermError("TERM_NOT_ABOVE_GRACE",
                            f"loan_term {lt} tháng phải lớn hơn thời gian ân hạn gốc {grace} tháng",
                            loan_term_months=lt, grace_period_months=grace)
    if lt > final_max_term_months:
        raise LoanTermError("TERM_ABOVE_MAX",
                            f"loan_term {lt} tháng vượt mức tối đa {final_max_term_months} tháng theo tuổi/ngân hàng",
                            loan_term_months=lt, final_max_term_months=final_max_term_months)
    return lt
