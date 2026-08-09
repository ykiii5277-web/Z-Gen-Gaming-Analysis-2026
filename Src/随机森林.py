import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix
)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#1.读取数据
df = pd.read_excel(
    "Data\02_processed\Data_transformed\随机森林.xlsx",
    sheet_name="随机森林"
)
df = df.dropna() #删除含缺失值的整行得到样本数=729
print("【1.样本信息】")
print("有效样本数：", len(df))
print("因变量类别分布：")
print(df['QK'].value_counts().sort_index())
#2.自变量X与因变量Y的设定
y = df['QK']
X = df.drop(columns=['QK'])
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
print("本次模型纳入的特征（变量）总数：", X.shape[1]) #查看自变量数量

#3.划分训练集/测试集（8:2，分层抽样，固定种子）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("\n【2.训练/测试集划分】")
print("训练集样本数：", len(X_train))
print("测试集样本数：", len(X_test))

#4.随机森林参数
model = RandomForestClassifier(
    n_estimators=100,
    criterion='gini',
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=5,
    bootstrap=True,
    oob_score=True,
    max_features='sqrt',
    random_state=42
)
model.fit(X_train, y_train)

#5.模型汇总
print("\n【3.模型参数汇总】")
print("树数量 n_estimators：", model.n_estimators)
print("分裂准则 criterion：", model.criterion)
print("最大深度 max_depth：", model.max_depth)
print("节点最小分裂样本 min_samples_split：", model.min_samples_split)
print("叶节点最小样本 min_samples_leaf：", model.min_samples_leaf)
print("袋外数据 OOB 准确率：", f"{model.oob_score_:.4f}")

#6.训练集评估
y_train_pred = model.predict(X_train)
acc_train = accuracy_score(y_train, y_train_pred)
print("\n【4.训练集评估】")
print(f"准确率（训练集）：{acc_train:.4f}")
print("训练集分类报告：")
print(classification_report(y_train, y_train_pred, digits=2))

#7.测试集评估
y_pred = model.predict(X_test)
acc_test = accuracy_score(y_test, y_pred)
print("\n【5.测试集评估（论文结果）】")
print(f"准确率（测试集）：{acc_test:.4f}")
print("测试集分类报告：")
print(classification_report(y_test, y_pred, digits=2))

#8.混淆矩阵
cm = confusion_matrix(y_test, y_pred)
labels = ['多元付费', '低龄轻量', '大众休闲', '核心沉浸']
print("\n【6.混淆矩阵】")
print(cm)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels, yticklabels=labels)
plt.title('混淆矩阵')
plt.xlabel('预测类别')
plt.ylabel('真实类别')
plt.tight_layout()
plt.show()

#9.特征重要性
importances = model.feature_importances_
feat_df = pd.DataFrame({
    '变量': X.columns,
    '重要性': importances
}).sort_values('重要性', ascending=False)
print("\n【7.特征重要性（前5）】")
print(feat_df.head(5))
plt.figure(figsize=(10, 6))
sns.barplot(x='重要性', y='变量', data=feat_df.head(5))
plt.title('随机森林特征重要性（Top5）')
plt.tight_layout()
plt.show()
