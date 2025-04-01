import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def cds_pricer(recovery_rate, rf_rate, tenor, coupon, upfront, credit_spread):
    """
    Calculate the par spread and present value of a CDS. The methodology for pricing CDS involves calculating the
    present value of the protection leg and the premium leg. The par spread is the credit spread that makes the present
    value of the CDS equal to zero.

    CDS can be priced using various models. The main types of models are reduced-form models and structural models,
    which directly model the default process of the underlying entity, or market-driven approaches which infer credit
    spreads from observed market data rather than directly modeling the default process.

    Examples of reduced form models include the Jarrow-Turnbull model (single factor hazard rate), the Duffie-Singleton
    model (stochastic intensity), and extensions of these such as models including a jump-to-default component.

    Examples of structural models include the Merton model (firm value and liabilities) and the Longstaff-Schwartz model
    (firm value and default barrier).

    Reduced form models' key assumption is that default is modeled as a stochastic process independent of the firm's
    fundamentals. Structural models, on the other hand, model default as a function of the firm's assets and
    liabilities, which assumes that markets are efficient and that the firm's value is observable.

    A market-driven approach would infer the hazard rate process from several CDS contracts with different maturities,
    perhaps using a bootstrapping approach to infer a piecewise-constant hazard rate curve.

    This CDS pricer uses a trivial form of the single-factor Jarrow-Turnbull model with a constant hazard rate and
    risk-free rate. The coupon payments are assumed to be continuous and the default time is assumed to follow an
    exponential distribution.

    Parameters
    ----------
    recovery_rate : float
        Recovery rate in case of default, between 0 and 1.
    rf_rate : float
        Constant risk-free rate, between 0 and 1.
    tenor : float
        Time to maturity of the CDS, in years.
    coupon : float
        Constant CDS coupon rate, between 0 and 1.
    upfront : float
        Upfront payment at the start of the CDS contract.
    credit_spread : float
        Constant credit spread, between 0 and 1.

    Returns
    -------
    (float, float)
        The par spread and present value of the CDS.
    """
    # Calculate the (constant) hazard rate
    hazard_rate = credit_spread / (1 - recovery_rate)

    # Calculate the present value of the protection leg
    risky_discount_rate = rf_rate + hazard_rate
    protection_leg_pv = ((1 - recovery_rate) * (hazard_rate / risky_discount_rate) * 
                         (1 - np.exp(-risky_discount_rate * tenor)))

    # Calculate the present value of the premium leg
    annuity_factor = (1 - np.exp(-risky_discount_rate * tenor)) / risky_discount_rate
    premium_leg_pv = coupon * annuity_factor

    # Calculate the par spread
    # Note: In this model, par_spread always equals credit_spread
    par_spread = protection_leg_pv / annuity_factor

    # Calculate the present value of the CDS
    cds_pv = protection_leg_pv - premium_leg_pv - upfront

    return par_spread, cds_pv


def plot_par_spread_vs_recovery_rate(rf_rate, tenor, coupon, upfront, credit_spread):
    recovery_rates = np.linspace(0.01, 0.99, 100)  # Recovery rates from 1% to 99%
    par_spreads = np.array([])  # Initialize an empty array to store par spreads

    for recovery_rate in recovery_rates:
        par_spread, _ = cds_pricer(
            recovery_rate, rf_rate, tenor, coupon, upfront, credit_spread)
        par_spreads = np.append(par_spreads, par_spread)  # Append the calculated par spread to the array

    plt.figure(figsize=(10, 6))
    plt.plot(100 * recovery_rates, 10000 * par_spreads, label='Par Spread')
    plt.xlabel('Recovery Rate (%)')
    plt.ylabel('Par Spread (bp)')
    plt.title('Par Spread vs. Recovery Rate')
    plt.legend()
    plt.grid(True)
    plt.show()


def strip_credit_spread(recovery_rate, rf_rate, tenor, coupon, upfront, x0=0.01):
    """
    Strip the credit spread from a CDS contract by fitting the credit spread that makes the present value of the CDS
    equal to zero. This prototype finds a single constant credit spread given a single CDS contract.

    To strip a credit curve from multiple CDS contracts, one would solve for the hazard rate iteratively, starting
    from the shortest maturity and working outward. This assumes the hazard rate is piecewise-constant.
    Alternatively, one could assume a parametric form such as a Nelson-Siegel curve. Then would apply optimization
    methods to minimize squared pricing errors.
    If one assumes a cubic spline curve, then would would solve a set of simultaneous equations for the 
    parameters of the spline.
    A more sophisticated approach would involve stochastic modeling of the hazard rate process, such as a 
    Cox-Ingersoll-Ross (CIR) model.

    Parameters
    ----------
    recovery_rate : float
        Recovery rate in case of default, between 0 and 1.
    rf_rate : float
        Constant risk-free rate, between 0 and 1.
    tenor : float
        Time to maturity of the CDS, in years.
    coupon : float
        Constant CDS coupon rate, between 0 and 1.
    upfront : float
        Upfront payment at the start of the CDS contract.
    x0 : float
        Initial guess for the credit spread.

    Returns
    -------
    float
        The fitted credit spread.
    """
    def objective(credit_spread):
        return cds_pricer(recovery_rate, rf_rate, tenor, coupon, upfront, credit_spread)[1]

    fitted_credit_spread = fsolve(objective, np.array(x0))[0]
    return fitted_credit_spread


def main():
    parser = argparse.ArgumentParser(description="CDS Pricer and Credit Spread Stripper")
    subparsers = parser.add_subparsers(
        dest="command", required=True,
        help="Select mode: 'p' for CDS pricing or 's' for credit spread stripping")

    # CDS Pricer
    pricer_parser = subparsers.add_parser("p", help="CDS Pricer")
    pricer_parser.add_argument("--recovery_rate", type=float, help="Recovery rate", default=0.4)
    pricer_parser.add_argument("--rf_rate", type=float, help="Constant risk-free rate", default=0.04)
    pricer_parser.add_argument("--tenor", type=float, help="Time to maturity (in years)", default=5)
    pricer_parser.add_argument("--coupon", type=float, help="CDS coupon rate", default=0.01)
    pricer_parser.add_argument("--upfront", type=float, help="Upfront payment", default=0.0)
    pricer_parser.add_argument("--credit_spread", type=float, help="Credit spread", default=0.01)

    # Credit Spread Stripper
    stripper_parser = subparsers.add_parser("s", help="Credit Spread Stripper")
    stripper_parser.add_argument("--recovery_rate", type=float, help="Recovery rate", default=0.4)
    stripper_parser.add_argument("--rf_rate", type=float, help="Constant risk-free rate", default=0.04)
    stripper_parser.add_argument("--tenor", type=float, help="Time to maturity (in years)", default=5)
    stripper_parser.add_argument("--coupon", type=float, help="CDS coupon rate", default=0.01)
    stripper_parser.add_argument("--upfront", type=float, help="Upfront payment", default=0.0)

    args = parser.parse_args()

    if args.command == "p":
        print(f"Running CDS Pricer with: recovery_rate={args.recovery_rate}, rf_rate={args.rf_rate}, "
              f"tenor={args.tenor}, coupon={args.coupon}, "
              f"upfront={args.upfront}, credit_spread={args.credit_spread}")
        # Call the function to price CDS
        par_spread, cds_pv = cds_pricer(args.recovery_rate, args.rf_rate, args.tenor, args.coupon,
                                        args.upfront, args.credit_spread)
        print(f"Par Spread: {par_spread:.4f}")
        print(f"Present Value of CDS: {cds_pv:.4f}")
        # Plotting the Par Spread vs Recovery Rate
        plot_par_spread_vs_recovery_rate(
            rf_rate=args.rf_rate, tenor=args.tenor, coupon=args.coupon, upfront=args.upfront,
            credit_spread=args.credit_spread)

    elif args.command == "s":
        print(f"Running Credit Spread Stripper with: recovery_rate={args.recovery_rate}, "
              f"rf_rate={args.rf_rate}, tenor={args.tenor}, "
              f"coupon={args.coupon}, upfront={args.upfront}")
        # Call the function to strip credit curve
        fitted_credit_spread = strip_credit_spread(
            args.recovery_rate, args.rf_rate, args.tenor, args.coupon, args.upfront)
        print(f"Fitted Credit Spread: {10000 * fitted_credit_spread:.0f} bp")
    
    else:
        raise ValueError(f"Invalid command: {args.command}")


if __name__ == "__main__":
    main()
