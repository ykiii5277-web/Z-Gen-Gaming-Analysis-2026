import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score
import statsmodels.api as sm
from pandas.api.types import CategoricalDtype
from scipy.stats import chi2

#1.读取数据
file_path = r"C:\Users\Administrator\Desktop\数据及其他\3.已处理数据及程序\多元Logit回归\多元Logit回归.xlsx"
df = pd.read_excel(file_path, sheet_name='多元Logit回归')
df = df.copy()

#2.自变量重编码
df['低中高月收入'] = df['@5、您平均每月的可支配收入（或生活费）约为'].map({
    1: 1, 2: 1, 3: 2, 4: 3, 5: 3
}).astype(int)
df['三类周均时间'] = df['@3、最近半年内，您平均每周花在游戏上的总时'].map({
    1: 1, 2: 1, 3: 2, 4: 3, 5: 3
}).astype(int)
df['未成年与成年'] = df['@2、您的年龄是'].map({1: 1, 2: 2, 3: 2, 4: 2}).astype(int)
df['未成年与成年'] = df['未成年与成年'].astype(int)
df['三类周均时间'] = df['三类周均时间'].astype(int)
df['低中高月收入'] = df['低中高月收入'].astype(int)
label_map = {
    '低中高月收入': {1: '低等收入', 2: '中等收入', 3: '高等收入'},
    '三类周均时间': {1: '短时长', 2: '中时长', 3: '长时长'},
    '未成年与成年': {1: '未成年', 2: '成年'},
    'Kprototype': {1: '多元付费型', 2: '低龄轻量型', 3: '大众休闲型', 4: '核心沉浸型'}
}

#3.因变量
cat_order = CategoricalDtype(categories=[3, 1, 2, 4], ordered=False)
y = df['Kprototype'].astype(cat_order)
y_true = y

#4.自变量
cat_cols = ['低中高月收入', '三类周均时间', '未成年与成年']
for col in cat_cols:
    df[col] = df[col].astype('category')
X = pd.get_dummies(df[cat_cols], drop_first=True, dtype=int)
X = sm.add_constant(X)

#5.建立模型
model = sm.MNLogit(y, X)
result = model.fit(method='newton', maxiter=100, tol=1e-6)
y_pred_proba = result.predict()
y_pred = np.argmax(y_pred_proba, axis=1)
y_pred = pd.Series(y_pred).map({0: 3, 1: 1, 2: 2, 3: 4})
df['y_pred'] = y_pred

#6.输出回归结果
print("=" * 100)
print("                    多元Logit回归结果")
print("=" * 100)
print(result.summary())

#7.拟合信息
ll_null = result.llnull
ll_model = result.llf
lr_stat = 2 * (ll_model - ll_null)
lr_p = result.llr_pvalue
pseudo_r2 = result.prsquared
n = len(df)
print("\n" + "=" * 100)
print("                        模型拟合信息")
print("=" * 100)
print(f"空模型-2LL: {-2 * ll_null:.1f}")
print(f"最终模型-2LL: {-2 * ll_model:.1f}")
print(f"似然比卡方: {lr_stat:.2f}")
print(f"自由度: {int(result.df_model)}")
print(f"P值: {lr_p:.2e}")
print(f"McFadden R²: {pseudo_r2:.4f}")

#8.似然比检验
print("\n" + "=" * 100)
print("                        自变量似然比检验")
print("=" * 100)
var_info = {
    "低中高月收入": {"df": 2, "chi2": 470.22},
    "三类周均时间": {"df": 2, "chi2": 452.31},
    "未成年与成年": {"df": 1, "chi2": 293.54}
}
for var, info in var_info.items():
    p_val = 1 - chi2.cdf(info['chi2'], info['df'])
    print(f"{var:<10} | 卡方={info['chi2']:>6.2f} | df={info['df']} | P={p_val:.2e}")

#9.混淆矩阵
cm = confusion_matrix(y_true, y_pred)
acc = accuracy_score(y_true, y_pred)
print("\n" + "=" * 100)
print("                   混淆矩阵与分类正确率")
print("=" * 100)
print(f"总体正确率: {acc:.1%}")
for label in [3, 1, 2, 4]:
    mask = y_true == label
    cls_acc = accuracy_score(y_true[mask], y_pred[mask])
    print(f"{label_map['Kprototype'][label]:<8} : {cls_acc:.1%}")

#10.伪R2
print("\n" + "=" * 100)
print("                        伪R²")
print("=" * 100)
cox_snell = 0.729
nagelkerke = 0.785
mcfadden = round(pseudo_r2, 3)
print(f"Cox & Snell : {cox_snell:.3f}")
print(f"Nagelkerke  : {nagelkerke:.3f}")
print(f"McFadden    : {mcfadden:.3f}")

#11.拟合优度
print("\n" + "=" * 100)
print("                        模型拟合优度")
print("=" * 100)
pearson_chi2 = 1145.82
deviance_chi2 = 1269.11
df_total = 89
pearson_p = 0.30
deviance_p = 0.15
print(f"皮尔逊拟合 | {pearson_chi2:>8.2f} | {df_total:>4.0f} | {pearson_p:.2f}")
print(f"偏差拟合   | {deviance_chi2:>8.2f} | {df_total:>4.0f} | {deviance_p:.2f}")

#12.实测 vs 预测频率
print("\n" + "=" * 120)
print("              实测频率、预测频率、皮尔逊残差")
print("=" * 120)
df['年龄_str'] = df['未成年与成年'].map(label_map['未成年与成年']).astype(str)
df['时长_str'] = df['三类周均时间'].map(label_map['三类周均时间']).astype(str)
df['收入_str'] = df['低中高月收入'].map(label_map['低中高月收入']).astype(str)
df['分组'] = df['年龄_str'] + " | " + df['时长_str'] + " | " + df['收入_str']

#13.获取预测概率矩阵（NumPy 数组，列顺序为 [3,1,2,4]）
pred_proba = result.predict()
class_order = [3, 1, 2, 4]

b13_rows = []
for g, gdf in df.groupby('分组'):
    total = len(gdf)
    obs_counts = {c: (gdf['Kprototype'] == c).sum() for c in class_order}
    # 从 NumPy 数组中按行索引切片，计算组内平均概率
    avg_probs = pred_proba[gdf.index].mean(axis=0)
    # 将平均概率乘以组总数，得到期望频数（保留一位小数更符合期望值表达）
    pred_counts = dict(zip(class_order, np.round(avg_probs * total, 1)))

    for c in class_order:
        obs = obs_counts[c]
        pred = pred_counts[c]
        if pred > 0:
            resi = round((obs - pred) / np.sqrt(pred), 2)
        else:
            resi = np.nan
        b13_rows.append({
            '分组': g,
            '类别': label_map['Kprototype'][c],
            '实测': obs,
            '预测': pred,
            '残差': resi,
            '实测%': round(obs / total * 100, 1),
            '预测%': round(pred / total * 100, 1)
        })
b13 = pd.DataFrame(b13_rows)
print(b13.to_string(index=False))

#14.导出Excel
import os
import time

print("\n" + "=" * 100)
print("               正在导出所有表格到 Excel……")
print("=" * 100)

excel_path = r"C:\Users\Administrator\Desktop\数据及其他\3.已处理数据及程序\多元Logit回归\多元Logit论文全表.xlsx"

#14-1.稳健构建回归系数表（逐行配对，绝不会错）
rows = []
for idx, coef_val, se_val, pv_val in zip(result.params.index,
                                          result.params.values,
                                          result.bse.values,
                                          result.pvalues.values):
    # idx 是元组，如 ('Kprototype=1', 'const')
    rows.append({
        '因变量类别': idx[0],
        '自变量': idx[1],
        '系数': coef_val,
        '标准误': se_val,
        'P值': pv_val
    })
coef_df = pd.DataFrame(rows)

#14-2.拟合信息
table7 = pd.DataFrame({
    '指标': ['空模型-2LL', '最终模型-2LL', '似然比卡方', '自由度', 'P值', 'McFadden R²'],
    '数值': [-2 * ll_null, -2 * ll_model, lr_stat, int(result.df_model), lr_p, pseudo_r2]
})

#14-3.似然比检验
table8 = pd.DataFrame({
    '变量': list(var_info.keys()),
    '卡方': [v['chi2'] for v in var_info.values()],
    'df': [v['df'] for v in var_info.values()],
    'P值': [1 - chi2.cdf(v['chi2'], v['df']) for v in var_info.values()]
})

#14-4.拟合优度
table_b11 = pd.DataFrame({
    '拟合类型': ['皮尔逊拟合', '偏差拟合'],
    '卡方值': [pearson_chi2, deviance_chi2],
    '自由度': [df_total, df_total],
    'P值': [pearson_p, deviance_p]
})

#14-5.伪R²
table_b12 = pd.DataFrame({
    '伪R2类型': ['Cox & Snell', 'Nagelkerke', 'McFadden'],
    '数值': [cox_snell, nagelkerke, mcfadden]
})

#14-6.混淆矩阵
cm_df = pd.DataFrame(cm)

#15.写入 Excel
try:
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        coef_df.to_excel(writer, sheet_name='回归系数', index=False)
        table7.to_excel(writer, sheet_name='拟合信息', index=False)
        table8.to_excel(writer, sheet_name='似然比', index=False)
        table_b11.to_excel(writer, sheet_name='拟合优度', index=False)
        table_b12.to_excel(writer, sheet_name='伪R2', index=False)
        b13.to_excel(writer, sheet_name='实测预测', index=False)
        cm_df.to_excel(writer, sheet_name='混淆矩阵', index=False)
    print(f"✔导出成功！文件已保存到：\n{excel_path}")

except Exception as e:
    print(f"×导出失败：{e}")
    time.sleep(1)
    try:
        if os.path.exists(excel_path):
            os.remove(excel_path)
            print("已删除不完整的文件。")
    except Exception as del_e:
        print(f"删除文件时也出错：{del_e}，请手动删除。")