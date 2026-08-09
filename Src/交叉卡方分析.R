#1.加载包
library(readxl)

#2.设置Excel所在文件夹
setwd("Data\02_processed\Data_transformed\交叉卡方分析")

#3.设置结果保存文件夹
result_dir <- "
Results\交叉卡方分析"
if (!dir.exists(result_dir)) dir.create(result_dir) #如果文件夹不存在，自动创建

#4.获取所有 Excel 文件
files <- list.files(pattern = "*.xlsx")

#5.循环分析+保存结果
for (file in files) {
  cat("\n========================================\n")
  cat("正在处理文件：", file, "\n")
  cat("========================================\n")
  # 读取数据
  df <- read_excel(file)
  # 统一列名
  colnames(df) <- c("var1", "var2", "count")
  # 构建列联表
  table_df <- xtabs(count ~ var1 + var2, data = df)
  print("交叉列联表：")
  print(table_df)
  # 卡方检验
  chisq_result <- chisq.test(table_df)
  print("卡方检验结果：")
  print(chisq_result)
  #保存到指定的文件夹
  output_file <- file.path(result_dir, paste0("结果_", sub(".xlsx", ".txt", file)))
  sink(output_file)
  cat("文件：", file, "\n\n")
  print("交叉列联表：")
  print(table_df)
  cat("\n")
  print("卡方检验结果：")
  print(chisq_result)
  sink()
}