
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(42)

# Simulation settings
initial_price = 100
number_of_days = 252
number_of_simulations = 10000

# Annual model assumptions
annual_return = 0.08
annual_volatility = 0.20
dt = 1 / number_of_days

# Generate random shocks
Z = np.random.normal(
    loc=0,
    scale=1,
    size=(number_of_days, number_of_simulations)
)

# Create an array for stock prices
prices = np.zeros(
    (number_of_days + 1, number_of_simulations)
)
prices[0] = initial_price

# Simulate prices using GBM
for day in range(1, number_of_days + 1):
    prices[day] = prices[day - 1] * np.exp(
        (annual_return - 0.5 * annual_volatility**2) * dt
        + annual_volatility * np.sqrt(dt) * Z[day - 1]
    )

# Analyze final prices
final_prices = prices[-1]

loss_count = np.sum(final_prices < initial_price)
loss_probability = loss_count / number_of_simulations

price_at_var = np.percentile(final_prices, 5)
var_amount = initial_price - price_at_var

print("Model: Geometric Brownian Motion")
print("Number of simulations:", number_of_simulations)
print("Trading days:", number_of_days)
print("Initial price: ₹", initial_price)
print("Average final price: ₹", round(np.mean(final_prices), 2))
print("Minimum final price: ₹", round(np.min(final_prices), 2))
print("Maximum final price: ₹", round(np.max(final_prices), 2))
print("Probability of loss:", round(loss_probability * 100, 2), "%")
print("95% VaR price threshold: ₹", round(price_at_var, 2))
print("95% VaR loss amount: ₹", round(var_amount, 2))

plt.figure(figsize=(12, 6))

theoretical_price = initial_price * np.exp(annual_return)

print("Theoretical expected final price: ₹", round(theoretical_price, 2))

plt.plot(prices[:, :50], linewidth=0.8)

plt.axhline(
    y=initial_price,
    linestyle="--",
    label="Initial price"
)

plt.title("Monte Carlo Stock Price Simulation (GBM)")
plt.xlabel("Trading day")
plt.ylabel("Stock price (₹)")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("simulation.png", dpi=150)
plt.show()

