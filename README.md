# 🎮 Z世代游戏偏好与行为的统计测度及群体细分研究

## 📖 项目简介
本项目基于全国31省区948份有效问卷，旨在通过全链条统计建模，深入剖析Z世代的游戏偏好、行为模式及态度结构。项目包括且不限于复现了从数据清洗、熵权法赋权、K-Prototypes混合聚类到随机森林预测的完整科研流程。

## 🌟 核心亮点
*   **数据驱动**：基于948份一手调研数据，覆盖全国31个省级行政区。
![](https://github.com/ykiii5277-web/Z-Gen-Gaming-Analysis-2026/blob/7a8a783b487fa1fd72d649b00fc678f8b20785b2/Questionnaire/%E5%9C%B0%E5%9F%9F%E5%88%86%E5%B8%83%E5%9B%BE.png)
*   **方法创新**：采用 **K-Prototypes** 算法解决混合数据类型（数值+分类）的聚类难题。
*   **模型融合**：结合 **多元Logit回归** 的可解释性与 **随机森林** 的非线性预测能力。
*   ![](https://github.com/ykiii5277-web/Z-Gen-Gaming-Analysis-2026/blob/67a160d15c67a0417bed9b0bf6d7c35baf0790ad/Results/03_Figures/%E9%9A%8F%E6%9C%BA%E6%A3%AE%E6%9E%97/%E5%A4%9A%E5%85%83Logit%E4%B8%8E%E9%9A%8F%E6%9C%BA%E6%A3%AE%E6%9E%97%E7%9A%84%E5%AF%B9%E6%AF%94%E4%B8%8E%E4%BA%92%E8%A1%A5.png)
*   **洞察深刻**：识别出“多元付费型”、“低龄轻量型”、“大众休闲型”、“核心沉浸型”四类典型玩家画像。
![](https://github.com/ykiii5277-web/Z-Gen-Gaming-Analysis-2026/blob/889e8772b242c80c9b22e4a85c300d1dc6cd20de/Results/03_Figures/K-Prototypes%E8%81%9A%E7%B1%BB/%E5%9B%9B%E7%B1%BB%E7%8E%A9%E5%AE%B6%E7%BE%A4%E4%BD%93%E6%A0%B8%E5%BF%83%E7%94%BB%E5%83%8F.png)
## 📊 主要结论
1.  **群体画像**：将玩家划分为四类，其中大众休闲型占比最高(37.6%)，核心沉浸型最具潜力。
2.  **态度结构**：验证了游戏态度的二元结构（正面/负面独立并存）。
3.  **趋势预测**：未来3-5年玩家结构将向“高参与、高品质、高社交”方向演化。

## 🛠️ 技术栈
*   **语言**: Python (pandas,numpy,matplotlib,seaborn,scikit-learn,statsmodels,scipy
), R(readx)，SPSS
*   **模型**:熵权法，对应分析，多元线性回归，信效度分析，K-Prototypes聚类，多元Logit回归，随机森林
*   **工具**: SPSS, Jupyter Notebook,Excel，Rstudio,Pycharm

## 📂 目录结构
*   `/data`: 存放脱敏后的数据集及清洗或转化数据。
*   `/Docs`: 包含完整的参赛论文PDF及获奖证书。
*   `/Questionarire`: 包含调查问卷及变量说明表
*   `/Result`: 包含文本、表格、图集三种类型的输出结果。
*   `/Src`: 包含部分建模分析的完整代码。
>
> > **🏆 2026年第十二届全国大学生统计建模大赛 二等奖获奖作品**
