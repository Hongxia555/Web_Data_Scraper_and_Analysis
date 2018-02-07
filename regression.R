# load data and only read valid rows
raw_data = read.csv("processed_data.csv")
valid_data = subset(raw_data, row_valid_index == TRUE)

# run regression on all sectors
# fit <- lm(ytd ~ risk + discussion + market_risk + mean + median + max + min + std, data=valid_data)
fit <- lm(ytd ~ mean, data=valid_data)
summary(fit)

# run regression only on financials data
financial_data = subset(valid_data, sector == 'Financials')
fit2 <- lm(ytd ~ mean, data=financial_data)
summary(fit2)

# run regression only on materials data
material_data = subset(valid_data, sector == 'Materials')
fit3 <- lm(ytd ~ mean, data=material_data)
summary(fit3)