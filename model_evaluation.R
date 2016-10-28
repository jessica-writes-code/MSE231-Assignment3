library(dplyr)
library(ggplot2)
library(ROCR)
library(scales)

## Function to make ROC curve & AUC
make_roc <- function(data, predictions,plot_loc) {
  df <- read.csv(data, sep = "\t", header=FALSE, quote="")
  labels <- ifelse(df$V1=="Trump",1,-1)
  vw_preds <- read.table(predictions)
  
  pred <- prediction(vw_preds, labels)
  perf <- performance(pred,"tpr","fpr")
 
  png(filename=paste0(plot_loc,".pdf"))
  plot(perf)
  dev.off()
  
  return(performance(pred, "auc")@y.values[[1]])
}

## Function to make calibration plots
make_calib <- function(data, predictions,plot_loc) {
  df <- read.csv(data, sep = "\t", header=FALSE, quote="")
  labels <- ifelse(df$V1=="Trump",1,0)
  vw_preds <- read.table(predictions)
  pred_bins <- round(1/(1+exp(-vw_preds)),1)
  
  pred_df <- data.frame(cbind(labels,pred_bins))
  names(pred_df) <- c("labels","prediction")
  
  pred_df_sum <- group_by(pred_df, prediction) %>%
    summarize(avg_trump=mean(labels), n = n())
  theme_set(theme_bw())
  ggplot(pred_df_sum, aes(x=prediction, y=avg_trump, size=n)) +
    geom_point(alpha=0.7) +
    labs(x="Model Prediction",y="Empirical Rate") +
    theme(legend.position="none") +
    scale_x_continuous(labels = scales::percent) +
    scale_y_continuous(labels = scales::percent) +
    geom_abline(slope=1, intercept=0, linetype=2)
  ggsave(paste0(plot_loc,".pdf"))
}

## Run Plots
# Remember to change this to not reference the data folder
make_roc("./data/test_tweets.tsv","./data/test_predictions.txt","./test_roc")
make_roc("./data/train_tweets.tsv","./data/training_predictions.txt","./train_roc")

make_calib("./data/test_tweets.tsv","./data/test_predictions.txt","./test_calib")
make_calib("./data/train_tweets.tsv","./data/training_predictions.txt","./train_calib")
