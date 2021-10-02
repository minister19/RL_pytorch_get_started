# Futures_ctp

### Futures_ctp Model

1. How comes feedback signal? 每个信号发生以后，还应持续观察从此以后的价差，用于判断之前的信号是否合理.
2. Important assumptions:

- Model is dependent on sig, sig's reward, sig's withdraw.
  - Sig's feedbacks (reward, withdraw) are independent of sig. Withdraw is nonnegative.
  - Sig's feedbacks are reset on each new reverse sig.
- Model is independent of fund, postion, margin.
  - Fund is calculated on each step.
  - Position and margin are calculated on each new action.

3. In production mode

- Immediate action according to withdraw signal, if kline finishes and action does not align with withdraw signal, close position.
- Evaluate strategy confidence by not holding positions all the time. Trusting epsilon introduced.

### Futures_ctp Roadmap

1. Margin

- Verified that margins are calculated correctly, using excel.
- Margin basing on avg_cost rather than margin_base, otherwise model would not work for general purpose.

2. Plot

- klines.
- fund_totals.
- actions as markers.
- train loss and test loss. Reason: too many data points to display, and often explodes.
- More Klines to train.
- Preprocess indicators.

3. Design algorithm to reduce action transitions

- action_penalty algorithm
  - improve trade_fee calculation from fixed to action\*vol
  - distinguish action_penalty (affects action transition) from trade_fee (affects fund_total)
- discretization_output algorithm

4. Model Input

- Do not train on position/margin, because position can be viewed as outcome/result only, and margin contributes to reward. Also, we can preprocess indic input，store into gpu for faster training process.

5. Model Action

- Consider action 'N', reward is small value wrt trade_fee. 优点：较小的回撤。缺点：收益变低。
- Consider action 'U', reward is small value wrt trade_fee.
- What if only long position or only short position? 优点：较小的回撤。缺点：收益变低。

6. Model Train

- Compare RMSprop and AdamW. Reason: continue using RMSprop, and AdamW behaves anti-optimization.
- Be aware if training more than enough times, model is overfitting (loss explodes or fluctuates).
- Policy net grad data clamp.
- Nematode bias disable.

### Archived ideas

1. 2020-08-18 Shawn: 仅当 reward 绝对值较大时保存 memory. Reason: 不能有幸存者偏差，走向局部优化。
2. 2021-08-29 Shawn: 'U' action means to hold on to previous action. Reason: saved by action_penalty algorithm.
3. 2021-08-31 Shawn: reward = 1 + margin, 1 for if margin >=0, 1 step forward. Reason: saved by action_penalty algorithm.
4. 2021-09-05 Shawn: If fixed number of actions are used up, the last action's state is calculated by last kline rather than next kline. Action 切换超过一定数量即结算 episode，用以约束 action 频繁切换. Reason: action_transits_quota algorithm. Warning, trainning data (klines) are also reduced, deteriorates learning progress, should be useful as part of risk management module.
5. 2021-09-05 Shawn: For every x steps, only y actions can be taken, if exceeds, done this episode. Reason: variant of action_transits_quota algorithm.
6. If action alignes with withdraw signal, action applies tick price instead of close price to simulate tick operations. Reason: production mode, if kline finishes and action does not align with withdraw signal, close position.
7. 由于资金有限，实际生产环境时，无法对所有监测交易品进行全时段持有，所以要根据信号可靠性进一步筛选，间断持有。但某些高度关注/用于科研的交易品可以设置为全时段持有。Reason: production mode.
8. Evaluate how (close) have our indicators revealed nature of money/fund flow in the market, given a fixed period. Reason: train loss and test loss reveals.
9. What signal should have feedback and what should not? Should margin and withdraw always present for a signal? Reason: let the network params (weight and bias) decide.
10. Update target_net/policy_net if reaches high score. Reason: gradient descent nature will optimize gradually.
11. accumulated_reward algorithm: only when action transits, assign accumulated reward to each action, and push to memory. 随 action 切换添加 memory，而不是随 each action 添加 memory. Reason: loss fluctuates, saved by actor critic model.
12. action_transits_quota algorithm: if action transits quota exhausted, episode is done, the last action's state is calculated by its next kline, action 'U' 给予 small margin. Reason: not working, try discretization_output algorithm.

### Futures_ctp to-research

1. 不同周期数据，通过插值合并到统一训练集内
2. 不同周期信号的 tick 比较重要，或者短窗口 tick，用于极端行情的风控
3. LSTM 模型做状态解析（利用它可以分析一段数据的特点），Zigzag 指标做数据库标记，训练出有监督状态-决策模型。
4. LSTM 模型做状态解析（利用它可以分析一段数据的特点），Q learning，训练出无监督状态-决策模型。Same idea on line: https://medium.com/@Lidinwise/trading-through-reinforcement-learning-using-lstm-neural-networks-6ffbb1f5e4a5

### TODO:

1. Sig sign 为 -1 时，withdraw 计算错误。
2. 打印 100 次训练时，整个 episode 对应的 model input，model output 值，进行数值分析，比如符号，大小，为 Single output node 做准备。
3. Sig 的符号是否应该与 Kline 趋势一致，即与收益正负符号一致。
4. Sig 的符号是否应该同向过零重置？Margin 重置，Withdraw 不重置。
5. Position margin 而不是 action margin，以及 withdraw，作为 model input？
6. Network 最后输出一个浮点数，作为开仓方向可信度？
7. Single output node，根据浮点输出分层，进行仓位操作。
8. Consider margin as stepped ones, rather than decimal ones.