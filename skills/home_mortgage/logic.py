from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MortgageInputs:
    home_price: float
    down_payment_pct: float
    annual_interest_rate: float
    term_years: int
    property_tax_rate: float
    annual_home_insurance: float
    pmi_rate: float
    hoa_monthly: float
    maintenance_monthly: float = 0.0


@dataclass
class AmortizationRow:
    month: int
    opening_balance: float
    interest_paid: float
    principal_paid: float
    ending_balance: float


def _monthly_pi_payment(principal: float, annual_rate_pct: float, term_years: int) -> float:
    months = term_years * 12
    monthly_rate = (annual_rate_pct / 100) / 12

    if monthly_rate == 0:
        return principal / months

    factor = (1 + monthly_rate) ** months
    return principal * (monthly_rate * factor) / (factor - 1)


def _build_amortization(loan_amount: float, annual_rate_pct: float, term_years: int, monthly_pi: float) -> List[AmortizationRow]:
    monthly_rate = (annual_rate_pct / 100) / 12
    rows: List[AmortizationRow] = []
    balance = loan_amount

    for month in range(1, term_years * 12 + 1):
        interest_paid = balance * monthly_rate
        principal_paid = monthly_pi - interest_paid
        ending_balance = max(0.0, balance - principal_paid)

        rows.append(
            AmortizationRow(
                month=month,
                opening_balance=balance,
                interest_paid=interest_paid,
                principal_paid=principal_paid,
                ending_balance=ending_balance,
            )
        )
        balance = ending_balance

        if balance <= 0:
            break

    return rows


def _pmi_monthly(loan_amount: float, down_payment_pct: float, pmi_rate: float) -> float:
    if down_payment_pct >= 20:
        return 0.0
    return (loan_amount * (pmi_rate / 100)) / 12


def _pmi_removal_month(amortization: List[AmortizationRow], home_price: float, threshold_ltv: float) -> int:
    for row in amortization:
        ltv = row.ending_balance / home_price
        if ltv <= threshold_ltv:
            return row.month
    return len(amortization)


def _rate_comparison(base: MortgageInputs, rates: List[float]) -> List[Dict[str, float]]:
    comparison = []
    loan_amount = base.home_price * (1 - (base.down_payment_pct / 100))
    taxes = (base.home_price * (base.property_tax_rate / 100)) / 12
    insurance = base.annual_home_insurance / 12

    for rate in rates:
        monthly_pi = _monthly_pi_payment(loan_amount, rate, base.term_years)
        total_interest = (monthly_pi * base.term_years * 12) - loan_amount
        total_monthly = monthly_pi + taxes + insurance
        comparison.append(
            {
                "rate": rate,
                "monthly_pi": monthly_pi,
                "total_monthly_tax_ins": total_monthly,
                "total_interest": total_interest,
            }
        )

    return comparison


def build_true_cost_model(inputs: MortgageInputs, comparison_rates: List[float] | None = None) -> Dict[str, object]:
    loan_amount = inputs.home_price * (1 - (inputs.down_payment_pct / 100))
    monthly_pi = _monthly_pi_payment(loan_amount, inputs.annual_interest_rate, inputs.term_years)

    monthly_taxes = (inputs.home_price * (inputs.property_tax_rate / 100)) / 12
    monthly_insurance = inputs.annual_home_insurance / 12
    monthly_pmi = _pmi_monthly(loan_amount, inputs.down_payment_pct, inputs.pmi_rate)

    amortization = _build_amortization(loan_amount, inputs.annual_interest_rate, inputs.term_years, monthly_pi)
    total_interest = sum(row.interest_paid for row in amortization)

    total_monthly_cost = (
        monthly_pi
        + monthly_taxes
        + monthly_insurance
        + monthly_pmi
        + inputs.hoa_monthly
        + inputs.maintenance_monthly
    )

    comparison = _rate_comparison(inputs, comparison_rates or [6.0, 6.5, 7.0])

    if monthly_pmi > 0:
        pmi_request_cancel_month = _pmi_removal_month(amortization, inputs.home_price, 0.80)
        pmi_auto_remove_month = _pmi_removal_month(amortization, inputs.home_price, 0.78)
    else:
        pmi_request_cancel_month = 0
        pmi_auto_remove_month = 0

    return {
        "inputs": inputs,
        "loan_amount": loan_amount,
        "monthly_breakdown": {
            "principal_interest": monthly_pi,
            "property_tax": monthly_taxes,
            "home_insurance": monthly_insurance,
            "pmi": monthly_pmi,
            "hoa": inputs.hoa_monthly,
            "maintenance": inputs.maintenance_monthly,
            "total_monthly_cost": total_monthly_cost,
        },
        "amortization_schedule": amortization,
        "amortization_first_12": amortization[:12],
        "total_interest_full_term": total_interest,
        "rate_comparison": comparison,
        "rule_of_thumb_1_25_pct": inputs.home_price * 0.0125,
        "pmi_cancel_80_month": pmi_request_cancel_month,
        "pmi_auto_remove_78_month": pmi_auto_remove_month,
    }
