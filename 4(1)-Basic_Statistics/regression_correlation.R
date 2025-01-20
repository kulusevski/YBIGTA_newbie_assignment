library(knitr)

### Advertising.csv를 불러와 데이터 로드하기!

advertising_data <- read.csv('/Users/joseph/Downloads/4회차/4회차) 기초 통계 과제/Advertising.csv')
summary(advertising_data, ncol=5)
head(advertising_data)

### Multiple Linear Regression을 수행해봅시다!
model <- lm(sales ~ TV+radio+newspaper, data = advertising_data)
summary_model <- summary(model)
coefficients <- as.data.frame(summary_model$coefficients)
kable(coefficients)


### Correlation Matrix를 만들어 출력해주세요!
correlation_mat <- cor(advertising_data[,c('TV', 'radio', 'newspaper', 'sales')])
correlation_mat <- as.data.frame(correlation_mat)
kable(correlation_mat)

