setwd("E:\\Final doc\\Final Doc")

#To read csv file
retail_data <- read.csv('dataset1.csv')
str(retail_data)


#Renaming columns
colnames(totalBillAmount)[1] <- "retailer_names"
colnames(totalBillAmount)[2] <- "Sum_of_bill_amount"

#Count of each retailer that how many times he purchased
freqOfPurchase <- aggregate(without_duplicates$bill_amount~without_duplicates$retailer_names, data=without_duplicates, FUN=function(x){NROW(x)}) 

#Renaming columns
colnames(freqOfPurchase)[1] <- "retailer_names"
colnames(freqOfPurchase)[2] <- "Frequency_of_Purchase"

#Convert into date(m/d/y) format
without_duplicates$created <- as.Date(as.character(without_duplicates$created), format = "%m/%d/%Y")

#Get recent date with maximum order
lastestTime = aggregate(without_duplicates$created,by=list(without_duplicates$retailer_names),max)


#Renaming columns
colnames(lastestTime)[1] <- "retailer_names"
colnames(lastestTime)[2] <- "Recent_date_of_purchase"

#Merging bill amount and frequency
final <- merge(totalBillAmount,freqOfPurchase)

#Merging latest time
final <- merge(final,lastestTime)

#Decreasing oder of columns
final <- final[order(final$Sum_of_bill_amount, decreasing = TRUE),]

#Threshold date
today <- as.Date('04/14/2018', format='%m/%d/%Y ')

#Get Recency
final$Recency<-as.numeric(difftime(today,final$Recent_date_of_purchase,units="days"))


library("dplyr")

#Average Order Value
final <- mutate(final, Average_Order_Value = final$Sum_of_bill_amount / final$Frequency_of_Purchase)

#Purchase Frequency
final <-  mutate(final, Purchase_Frequency = final$Frequency_of_Purchase / nrow(final))

#Customer Value 
final <-  mutate(final, Customer_Value = final$Average_Order_Value * final$Purchase_Frequency)

#Save file into csv
write.csv(final,file = "final_customer_scores.csv")
