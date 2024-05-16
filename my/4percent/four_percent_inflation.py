def calculate_balance_with_interest(initial_investment, inflation_rate, annual_return_rate, years, cost_every_year):
    """
    计算遵循4%法则并考虑投资复利增长及通货膨胀情况下的资金余额变化。

    参数:
    initial_investment (float): 初始投资额
    inflation_rate (float): 年通货膨胀率（例如4%应输入为0.04）
    annual_return_rate (float): 年化投资回报率（例如5%应输入为0.05）
    years (int): 模拟的年数
    cost_every_year: 每年花费金额

    返回:
    balances (list): 每年的结束余额列表
    """
    balance = initial_investment
    balances = [balance]
    withdrawal = 0.04


    for year in range(0, years):
        # 考虑通货膨胀调整提取额
        inflation_adjusted_withdrawal = cost_every_year * (1 + inflation_rate) ** year

        # 应用投资回报率前先扣除本年提取额
        balance -= inflation_adjusted_withdrawal

        # 剩余资金按年化收益率增长
        balance *= (1 + annual_return_rate)

        # 确保余额不会降至0以下
        balance = max(balance, 0)

        balances.append(balance)

        # 打印每年的信息（可选）
        print(f"Year {year}: Ending Balance = {balance:.2f}")

    return balances


# 示例：初始投资额100万，通货膨胀率3%，年化投资回报率6%，模拟50年
initial_investment = 1_000_000
inflation_rate = 0.04
annual_return_rate = 0.07
years = 30
# initial_investment * 0.04
cost_every_year = 40_000

balances = calculate_balance_with_interest(initial_investment, inflation_rate, annual_return_rate, years, cost_every_year)

# 打印最终结果
print(f"\nAfter {years} years, the ending balance is: {balances[-1]:.2f}")