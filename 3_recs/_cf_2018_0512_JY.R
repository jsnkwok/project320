#####################################################
###     Recitation 11 - Collaborative Filtering   ###
#Basis: http://www.salemmarafi.com/code/collaborative-filtering-r/


# As always, we first set the working directory.

# Let's begin by loading the following package:
library(tidyverse)
library(stringr)
library(dplyr)
library(softImpute) #collaborative filtering. 
setwd("/Users/jasonkwok/Dropbox (MIT)/2018sp_analyticsedge_15_701/skincare/_cf")
source("functions_HW9.R")

### Load data
ratings <-read.csv("2018_0510_labeled.csv")
colnames(ratings) <- c("title","score_wrong","commentno","threadno","id","url","user","comment","comment_id","p_i","classification","score")
ratings = subset(ratings, select = c(user, p_i, score))
#ratings <-ratings[1:10000,] #1:10000 works. 1:10001 fails 1:12000 FAILS. 1:11000 fails. 1:10500 fails. 1:10300 fails. 10050 fails. 

ratings = ratings[ratings$user != "",]  #somehow, when i enact this, it errors out. 
ratings = ratings %>% 
  mutate(p_i = str_replace_all(p_i, " ", ""))  #remove strings


#nrow(ratings) #deleteme = user_key_unique[user_key_unique$user == "",] #... screwing analysis! too many lumped into blank. 
#ratings = ratings[ratings$p_i != "",] 
#ratings = ratings[ratings$score != "",]  

#Remove NAs in dataset
ratings <- ratings[complete.cases(ratings), ] #... remove NAs... same rows...15958 https://stackoverflow.com/questions/4862178/remove-rows-with-nas-missing-values-in-data-frame
ratings <- unique( ratings[ , ] )

ratings = na.omit(ratings) #any(is.na(ratings)) #NO NAs...

#Make ratings$score all all positive. 
ratings$score = ratings$score + abs(min(ratings$score)) +1
ratings$score = (ratings$score)^.5 #normalize it from 1-7. 
ratings$score = as.integer(ratings$score) #write.csv(ratings, "deleteme.csv", row.names=FALSE)

####################################
#CONVERT PRODUCT STRING TO UNIQUE NUMBER
l=unique(c(as.character(ratings$p_i), as.character(ratings$p_i)))
product_key <- data.frame(product_key=as.numeric(factor(ratings$p_i, levels=l)), number=as.numeric(factor(ratings$p_i, levels=l)), p_i=ratings$p_i)
product_key_unique<- unique( product_key[ , ] )
#ratings$p_i = as.integer(product_key$product_key) 

####################################
#CONVERT NAMES TO UNIQUE NUMBERS
#n=unique(c(as.character(ratings$user),as.character(ratings$user)))
#user_key <- data.frame(user_key=as.numeric(factor(ratings$user,levels=n)),number=as.numeric(factor(ratings$user,levels=n)),user=ratings$user)
#user_key_unique <- unique( user_key[,]) #nrow(user_key_unique) #1160 unique users. 
#ratings$user = as.integer(user_key$user_key)#ratings$user = as.integer(ratings$user)

ratings = ratings %>% 
  group_by(user, p_i) %>%  
  summarise(score = mean(score)) %>% 
  ungroup()  #make unique to that specific product. 
ratings$score = as.integer(ratings$score)

##### RANDOM NUMBERS (if others fail.) #Try random numbers. 
#count_unique_scores = length(unique( ratings$score[]))
#ratings$score <- sample(1:5,nrow(ratings),rep=TRUE)
#ratings$p_i <- sample(1:108,nrow(ratings),rep=TRUE)
#ratings$score <- sample(1:108,nrow(ratings),rep=TRUE)
#ratings$user <- sample(1:108,nrow(ratings),rep=TRUE)





###### User-Item Collab Filtering: 

############################
#  Item Based Similarity   #
############################   

library(reshape)
ratings.pivot <- cast(ratings, user ~ p_i, fill=0)
data.germany <- ratings.pivot
# Drop the user column and make a new data frame
data.germany.ibs <- (data.germany[,!(names(data.germany) %in% c("user"))])

# Create a helper function to calculate the cosine between two vectors
getCosine <- function(x,y) 
{
  this.cosine <- sum(x*y) / (sqrt(sum(x*x)) * sqrt(sum(y*y)))
  return(this.cosine)
}

# Create a placeholder dataframe listing item vs. item
holder <- matrix(NA, nrow=ncol(data.germany.ibs),ncol=ncol(data.germany.ibs),dimnames=list(colnames(data.germany.ibs),colnames(data.germany.ibs)))
data.germany.ibs.similarity <- as.data.frame(holder)

# Lets fill in those empty spaces with cosine similarities
for(i in 1:ncol(data.germany.ibs)) {
  for(j in 1:ncol(data.germany.ibs)) {
    data.germany.ibs.similarity[i,j]= getCosine(data.germany.ibs[i],data.germany.ibs[j])
  }
}

# Output similarity results to a file
write.csv(data.germany.ibs.similarity,file="final-germany-similarity.csv")

# Get the top 10 neighbours for each
data.germany.neighbours <- matrix(NA, nrow=ncol(data.germany.ibs.similarity),ncol=11,dimnames=list(colnames(data.germany.ibs.similarity)))
data.germany.neighbours.cosno <- matrix(NA, nrow=ncol(data.germany.ibs.similarity),ncol=11,dimnames=list(colnames(data.germany.ibs.similarity)))

for(i in 1:ncol(data.germany.ibs)) 
{
  data.germany.neighbours[i,] <- (t(head(n=11,rownames(data.germany.ibs.similarity[order(data.germany.ibs.similarity[,i],decreasing=TRUE),][i]))))
}

for(i in 1:ncol(data.germany.ibs)) 
{
  data.germany.neighbours.cosno[i,] <- (t(head(n=11,data.germany.ibs.similarity[order(data.germany.ibs.similarity[,i],decreasing=TRUE),][i])))
}

# Output neighbour results to a file  
write.csv(file="final-germany-item-neighbours.csv",x=data.germany.neighbours[,-1])
write.csv(file="final-germany-item-neighbours-cos.csv",x=data.germany.neighbours.cosno[,-1])

summary(data.germany.neighbours.cosno[,2])

mean(data.germany.neighbours.cosno[,2])

############################
# User Scores Matrix       #
############################    
# Process:
# Choose a product, see if the user purchased a product
# Get the similarities of that product's top 10 neighbours
# Get the purchase record of that user of the top 10 neighbours
# Do the formula: sumproduct(purchaseHistory, similarities)/sum(similarities)

# Lets make a helper function to calculate the scores
getScore <- function(history, similarities)
{
  x <- sum(history*similarities)/sum(similarities)
  x
}

# A placeholder matrix
holder <- matrix(NA, nrow=nrow(data.germany),ncol=ncol(data.germany)-1,dimnames=list((data.germany$user),colnames(data.germany[-1])))

# Loop through the users (rows)
for(i in 1:nrow(holder)) 
{
  # Loops through the products (columns)
  for(j in 1:ncol(holder)) 
  {
    # Get the user's name and th product's name
    # We do this not to conform with vectors sorted differently 
    user <- rownames(holder)[i]
    product <- colnames(holder)[j]
    
    # We do not want to recommend products you have already consumed
    # If you have already consumed it, we store an empty string # Jason deleted this. 
   
      
      # We first have to get a product's top 10 neighbours sorted by similarity
      topN<-((head(n=11,(data.germany.ibs.similarity[order(data.germany.ibs.similarity[,product],decreasing=TRUE),][product]))))
      topN.names <- as.character(rownames(topN))
      topN.similarities <- as.numeric(topN[,1])
      
      # Drop the first one because it will always be the same song
      topN.similarities<-topN.similarities[-1]
      topN.names<-topN.names[-1]
      
      # We then get the user's purchase history for those 10 items
      topN.purchases<- data.germany[,c("user",topN.names)]
      topN.userPurchases<-topN.purchases[topN.purchases$user==user,]
      topN.userPurchases <- as.numeric(topN.userPurchases[!(names(topN.userPurchases) %in% c("user"))])
      
      # We then calculate the score for that product and that user
      holder[i,j]<-getScore(similarities=topN.similarities,history=topN.userPurchases)
      
  } # end product for loop   
} # end user for loop

# Output the results to a file
data.germany.user.scores <- holder
write.csv(file="final-user-scores.csv",data.germany.user.scores)

# Lets make our recommendations pretty
data.germany.user.scores.holder <- matrix(NA, nrow=nrow(data.germany.user.scores),ncol=100,dimnames=list(rownames(data.germany.user.scores)))

###Jason added.
length(data.germany.user.scores.holder[1,]) #... this is length 100.
#However, seems like there are only 68 products! so lets truncate this to 68
#length(data.germany.user.scores[i,]) = 68

data.germany.user.scores.holder = data.germany.user.scores.holder[,1:68] #truncates rows to only 68 columns. 

for(i in 1:nrow(data.germany.user.scores)) 
{
  data.germany.user.scores.holder[i,] <- names(head(n=100,(data.germany.user.scores[,order(data.germany.user.scores[i,],decreasing=TRUE)])[i,]))
}

#Scores
data.germany.user.scores.holder.scores = data.germany.user.scores.holder[,1:68] #truncates rows to only 68 columns. 
for(i in 1:nrow(data.germany.user.scores)) 
{
  data.germany.user.scores.holder.scores[i,] <- head(n=100,(data.germany.user.scores[,order(data.germany.user.scores[i,],decreasing=TRUE)])[i,])
}
# Write output to file
write.csv(file="final-user-recommendations.csv",data.germany.user.scores.holder)
write.csv(file="final-user-recommendations-scores.csv",data.germany.user.scores.holder.scores)

##### Clustering
#clust.data = data.germany.user.scores.holder #[,:length(data.germany.user.scores.holder[1,])
#distance = na.omit(dist(clust.data,method="euclidean")) #Clust only by product-types.
# <- ratings[complete.cases(ratings), ]
# = na.omit(ratings) #any(is.na(ratings

