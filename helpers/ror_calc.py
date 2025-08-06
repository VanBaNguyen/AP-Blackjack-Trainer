import math

def risk_of_ruin(bankroll_units, edge=0.004, stddev=1.15):
    variance = stddev ** 2
    ror = math.exp(-2 * edge / variance * bankroll_units)
    return ror

bankroll = 10000
unit = 25
units = bankroll // unit

ror = risk_of_ruin(units)
print(f"Bankroll: ${bankroll}, Unit: ${unit}, Units: {units}, Risk of Ruin: {ror:.2%}")