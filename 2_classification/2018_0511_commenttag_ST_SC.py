

#Jason kwok... very simple script to tag comments to any of these words. 
import csv
import re

file_name = '2018_0510_redditdump.csv'

#reader = csv.reader(open('redditdump_2018_0404.csv', 'rb'))
#reader1 = csv.reader(open('output1.csv', 'rb'))
writer = csv.writer(open('2018_0511_labeled_stsc.csv', 'w'))



ingredients = ['hyaluronic Acid','niacinamide','retinol','azelaic acid','Argan','Jojoba','Grapeseed','Benzoyl Peroxide','Salicylic acid','BP','Aloe','Tretinoin','Rosehip seed','Vitamin A','Tea Tree','Lavender','Sandalwood','Etherical','AHA','Hemp seed','Squalane','tret','Vitamin E','Vitamin C','Azealaic Acid','Sulfer 10%','Rosehip']
#['Hyaluronic Acid','niacinamide','retinol','azelaic acid','Argan','Jojoba','Grapeseed','Benzoyl Peroxide','Salicylic acid','BP','Aloe','Tretinoin','Rosehip seed','Vitamin A','Tea Tree','Lavender','Sandalwood','Etherical','AHA','Hemp seed','Squalane','tret','Vitamin E','Vitamin C','Azealaic Acid','Sulfer 10%','Rosehip']
products = ['Clinical Vitamin C serum ','Neutrogena Hydro Boost serum','Alpha retinol .15','CeraVe PM moisturizer (niacinamide)','CeraVe hydrating face wash','Advanced Clinical Vitamin C Serum','Aveeno radiant moisturizer spf 15','Australian Gold botanical sunscreen spf 50','Simple\'s Hydrating Oil','Hada Labo','Neutrogena Stubborn Acne','Differin','Accutane','CeraVe hydrating cleanser','AHA','BHA','The Ordinary Granactive Retinoid 2%','The Ordinary Niacinamide 10%','Mizon Snail Repair Foam Cleanser','Thayers Witch Hazel with Cucumber','Citrix Vitamin C Antioxidant Sunscreen','Mizon Snail Repair Perfect Cream','Retin-A','Cetaphil daily gentle cleanser','Cetaphil daily moisturizer SPF 30 ','Ponds cream','Aztec Secret Clay Mask','Hada Labo light lotion','NIOD hyaluronic complex','Stratia liquid gold','La roche posay lipikar balm','La roche posay anthelios clear skin SPF 60','Leven rose jojoba oil','Mixa Micellar Water ','The Ordinary Niacinamide + Zinc','La Roche-Posay Toleriane Ultra','Heliocare ultra gel SPF 50+ ','Mixa Micellar Water','Lush Fresh Farmacy bar','Vitamin A serum','Toleriane cream','Clearasil ultra rapid action cream','Cerave PM','UV Skin Aqua Milk spf 50','Garnier Micellar Water','Philosophy Made Simple cleanser ','TO Niacinamide/Zinc','Cerave in the tub','TO niacinamide','TO peeling solution','Simple micellar water','TO Natural Moisturizing Factors + HA','Biore UV Water Essence SPF 50','Cetaphil Foaming Cleanser','TO Niacimamide','TO Advanced Retinoid Emulsion','TO Glycolic Acid Toner','CeraVe foaming facial cleanser','Duac gel','CeraVe AM moisturizer with sunscreen','CeraVe PM moisturizer','cosrx snail mucin essence ','TO niacinamide +zinc ','cosrx oil free hydrating lotion','Neutrogena sheer zinc spf 50 physical sunscreen','cosrx low ph cleanser','cosrx snail mucin essence','TO niacinamide +zinc','ceraVe hydration lotion','TO mandelic acid 10%','TO moisturizer +HA','Bija Trouble Spot Essence','My Beauty Diary Cactus Sheet','La Roche-Posay Toleriane Hydrating Gentle Face Cleanser','Cetaphil Daily Hydrating Lotion w/ Hyaluronic Acid','The Ordinary Caffeine Solution','Neutrogena Clear Face Sunscreen Lotion 55','La Roche-Posay Toleriane Hydrating Gentle Face Cleanser ','Pixi Glow Tonic','Uncle Harry\'s Clay Mask Bar','Mario Badescu Drying Lotion','Aquafor','Palmers Ultra Gentle Cleansing Oil','Sukin Rosehip Oil','Vaseline','La Mer the Eye Concentrate','Stridex Maximum Strength','Mecca Cosmetica To Save Face SPF 50','Cetaphil','CeraVe Foaming Cleanser','neutrogena ultra gentle foaming cleanser','Bioderma sebium hydra','Neutrogena Acne Light Therapy Mask','Cetaphil Daily Facial Cleanser','Skinceuticals CE Ferulic Serum','Earth\'s Recipe Energy Boosting Toner','TO Niacinamide + Zinc Serum','Skin Aqua UV Moisture milk','Illi Cleansing Oil','Makeup Alley DMAE cleanser',' TO Niacinamide + Zinc','Sulwhasoo Capsulized Ginseng Fortifying Serum','Holy Snails Shark Sauce','Cetaphil Gentle Skin Cleanser','Thayers Witch Hazel Rose Petal','Hada Labo Gokujin Lotion','Klairs Vitamin C Serum','Face Shop Oil Control Sunscreen SPF35','The Face Shop Light Rice Water Oil Cleanser','TO Glycolic Acid Toning Solution 7%','Cosrx 96 Snail Mucin Essence','Hada Labo Gokujin Hyaluronic Cream','TO Azealaic Acid','Citrix Vitamin C Antioxidant Sunscreen ','Pure Aloe','Tretinoin Cream','Isntree Hyaluronic Acid Toner','RMK W Treatment Oil','La Roche Posay Hydraphase Intense Light','La Roche Posay Anthelios XL SPF 50+ Fluid','Shiseido Perfect Cleansing Oil','Paula\'s Choice Skin Perfecting 2% BHA','Herbivore Lapis Oil','CeraVe Foaming Cleanser ','Paula\'s Choice Skin Balancing Pore Reducing Toner',' Australian Gold Botanical Tinted SPF 50','CeraVe Moisturizing Cream','PC\'s BHA 2% Skin Perfecting Liquid ','Aztec Secret Indian Healing Clay with Bragg\'s Organic Apple Cider Vinegar','The Ordinary\'s 30% AHA & 2% BHA peel','Majestic Pure Aloe Vera Gel','TO\'s 100% Squalane','TO\'s Salicylic Acid 2% serum','PC\'s Toner ','PC\'s BHA 2% ','PC\'s 2.5% BP ',' The Ordinary\'s Niacinamide + Zinc serum ','Equate Baby 100% Pure Petroleum','Simple Micellar Cleansing Water','Thayers Rose Petal Alcohol-Free Toner','TruSkin Vitamin C Serum','Simple Protecting Light Moisturizer SPF 15','CereVe Hydrating Facial Cleanser','The Ordinary Azelaic Acid Suspension 10%','Simple Skin Quench Sleeping Cream','Jack Black Lip Balm with Shea Butter & Vitamin E']
#['Clinical Vitamin C serum ','Neutrogena Hydro Boost serum','Alpha retinol .15','CeraVe PM moisturizer (niacinamide)','CeraVe hydrating face wash','Advanced Clinical Vitamin C Serum','Aveeno radiant moisturizer spf 15','Australian Gold botanical sunscreen spf 50','Simples Hydrating Oil','Hada Labo','Neutrogena Stubborn Acne','Differin','Accutane','CeraVe hydrating cleanser','AHA','BHA','The Ordinary Granactive Retinoid 2%','The Ordinary Niacinamide 10%','Mizon Snail Repair Foam Cleanser','Thayers Witch Hazel with Cucumber','Citrix Vitamin C Antioxidant Sunscreen','Mizon Snail Repair Perfect Cream','Retin-A','Cetaphil daily gentle cleanser','Cetaphil daily moisturizer SPF 30 ','Ponds cream','Aztec Secret Clay Mask','Hada Labo light lotion','NIOD hyaluronic complex','Stratia liquid gold','La roche posay lipikar balm','La roche posay anthelios clear skin SPF 60','Leven rose jojoba oil','Mixa Micellar Water ','The Ordinary Niacinamide + Zinc','La Roche-Posay Toleriane Ultra','Heliocare ultra gel SPF 50+ ','Mixa Micellar Water','Lush Fresh Farmacy bar','Vitamin A serum','Toleriane cream','Clearasil ultra rapid action cream','Cerave PM','UV Skin Aqua Milk spf 50','Garnier Micellar Water','Philosophy Made Simple cleanser ','TO Niacinamide/Zinc','Cerave in the tub','TO niacinamide','TO peeling solution','Simple micellar water','TO Natural Moisturizing Factors + HA','Biore UV Water Essence SPF 50','Cetaphil Foaming Cleanser','TO Niacimamide','TO Advanced Retinoid Emulsion','TO Glycolic Acid Toner','CeraVe foaming facial cleanser','Duac gel','CeraVe AM moisturizer with sunscreen','CeraVe PM moisturizer','cosrx snail mucin essence ','TO niacinamide +zinc ','cosrx oil free hydrating lotion','Neutrogena sheer zinc spf 50 physical sunscreen','cosrx low ph cleanser','cosrx snail mucin essence','TO niacinamide +zinc','ceraVe hydration lotion','TO mandelic acid 10%','TO moisturizer +HA','Bija Trouble Spot Essence','My Beauty Diary Cactus Sheet','La Roche-Posay Toleriane Hydrating Gentle Face Cleanser','Cetaphil Daily Hydrating Lotion w/ Hyaluronic Acid','The Ordinary Caffeine Solution','Neutrogena Clear Face Sunscreen Lotion 55','La Roche-Posay Toleriane Hydrating Gentle Face Cleanser ','Pixi Glow Tonic','Uncle Harrys Clay Mask Bar','Mario Badescu Drying Lotion','Aquafor','Palmers Ultra Gentle Cleansing Oil','Sukin Rosehip Oil','Vaseline','La Mer the Eye Concentrate','Stridex Maximum Strength','Mecca Cosmetica To Save Face SPF 50','Cetaphil','CeraVe Foaming Cleanser','neutrogena ultra gentle foaming cleanser','Bioderma sebium hydra','Neutrogena Acne Light Therapy Mask','Cetaphil Daily Facial Cleanser','Skinceuticals CE Ferulic Serum','Earths Recipe Energy Boosting Toner','TO Niacinamide + Zinc Serum','Skin Aqua UV Moisture milk','Illi Cleansing Oil','Makeup Alley DMAE cleanser',' TO Niacinamide + Zinc','Sulwhasoo Capsulized Ginseng Fortifying Serum','Holy Snails Shark Sauce','Cetaphil Gentle Skin Cleanser','Thayers Witch Hazel Rose Petal','Hada Labo Gokujin Lotion','TO Niacinamide','Cerave PM moisturizer','Klairs Vitamin C Serum','Face Shop Oil Control Sunscreen SPF35','The Face Shop Light Rice Water Oil Cleanser','TO Glycolic Acid Toning Solution 7%','Cosrx 96 Snail Mucin Essence','Hada Labo Gokujin Hyaluronic Cream','TO Azealaic Acid','Mizon Snail Repair Foam Cleanser','Thayers Witch Hazel with Cucumber','Mizon Snail Repair Perfect Cream','Citrix Vitamin C Antioxidant Sunscreen ','Mizon Snail Repair Foam Cleanser','Thayers Witch Hazel with Cucumber','Pure Aloe','Tretinoin Cream','Isntree Hyaluronic Acid Toner','CosRX Snail Mucin Essence','RMK W Treatment Oil','La Roche Posay Hydraphase Intense Light','La Roche Posay Anthelios XL SPF 50+ Fluid','Shiseido Perfect Cleansing Oil','Paulas Choice Skin Perfecting 2% BHA','Isntree Hyaluronic Acid Toner','CosRX Snail Mucin Essence','The Ordinary Granactive Retinoid 2%','RMK W Treatment Oil','Herbivore Lapis Oil','La Roche Posay Hydraphase Intense Light','CeraVe Foaming Cleanser ','Paulas Choice Skin Balancing Pore Reducing Toner',' Australian Gold Botanical Tinted SPF 50','CeraVe Moisturizing Cream',' PCs BHA 2% Skin Perfecting Liquid ',' CeraVe Foaming Cleanser ','Aztec Secret Indian Healing Clay with Braggs Organic Apple Cider Vinegar','The Ordinarys 30% AHA & 2% BHA peel','Majestic Pure Aloe Vera Gel','TOs 100% Squalane','TOs Salicylic Acid 2% serum',' PCs Toner ',' PCs BHA 2% ',' PCs 2.5% BP ',' The Ordinarys Niacinamide + Zinc serum ',' CeraVe Moisturizing Cream',' Differin gel once every 2-3 days ',' Equate Baby 100% Pure Petroleum']
skintype = ['Dry','Dehydrated','Oily','Sensitive','Damaged']
#old skintype ['Dry','Dehydrated','Oily','Sensitive','Combination','Normal','Damaged','Combo']
skinconcerns =  ['Hyperpigmentation','Congestion','Blackheads','Whiteheads','Acne','Pimples','Breakouts','Breaking out','PIE','redness','Rosacea','Eczema','Discoloration','Tone','Texture','PIH','Scars','Pimple','Scar','Irritation','Dry Spots','Dark Circles','Glow','Freaked out','Large pores','Congested','Hydration','Spot','Scarring']
#old skin concerns ['Hyperpigmentation','Congestion','Blackheads','Whiteheads','Acne','Pimples','Breakouts','Breaking out','PIE','redness','Rosacea','Eczema','Discoloration','Tone','Texture','PIH','Scars','Pimple','Scar','Irritation','Dry Spots','Dark Circles','Glow','Freaked out','Large pores','Congested','Hydration','Spot','Scarring']

threadtitle = ['Skin Concerns','B&A','Product question','routine help','Acne','Haul','shelfie','Skin Concern','Anti-aging','OCM','Suncare','Sun Care','Hair Removal','selfie','anti aging','B&A/selfie','before&after','NEW OR NEED HELP?']
## File names 

goodwords = ['amazing','great','really well','good','best','calm','clear','clearing','recommend','fine','fave','recommend','favorite','more tolerable' ,'changed my life']
badwords = ['bad','screwed up','poorly','did not work','drying','dried','break out','breaking out','hard time','don\'t','didn\'t','suffer']

goodwords_big  = open('_positive_words.txt', 'r')
goodwords_big_list = [line.replace('\n', '').replace('\'', '').split(',')[0] for line in goodwords_big]
goodwords = goodwords+goodwords_big_list

badwords_big  = open('_negative_words.txt', 'r')
badwords_big_list = [line.replace('\n', '').replace('\'', '').split(',')[0] for line in badwords_big]
badwords=badwords+badwords_big_list

#toParse = open(file_name, "r")

#pull thorugh an array of the data and write it into excel. 
def lookthrough_sc_st(csvrow,arrayofregex,nametowriteinexcel,comment_no):
  rowwrite = csvrow.copy() #write a copy. 
  st_sc = []
  rowwrite.append(comment_no) #append the comment nummber
  commentlower = csvrow[7].lower() ##CHANGE IF THE COLUMN GETS PUSHED OUT DIFFERENTLY 
  for word in arrayofregex:      
      wordlower = word.lower()
      if re.search(wordlower,commentlower):

        #rowwrite.append(wordlower)
        #rowwrite.append(nametowriteinexcel)
        #score = 0

        ####Sentiment Score Part
        #for word in goodwords:
        #  if re.search(word.lower(),commentlower):
        #    score += 1
        #    #print(score)
        #for wordb in badwords:
        #  try:
        #    if re.search(wordb.lower(),commentlower):
        #      score += -1
        #      #print(score)
        #  except:
        #    pass
        ####End Sentiment Score Part
        st_sc.append(wordlower)
        #append the score! 
        #writer.writerow(rowwrite)
      else:
        pass
  rowwrite.append(st_sc) #
  if st_sc == []:
    pass
  else:
    writer.writerow(rowwrite)
	#  


with open(file_name, 'r') as csvfile:
    #fieldnames = ['title', 'score','id','url','comment']
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    reader = csv.reader(csvfile, delimiter=',')

    #write output stuff 
    #fieldnames = ['title', 'score','id','url','comment']
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    #writer.writerow({'title': 'Baked', 'score': 'Beans','id': 'Beans','url': 'Beans','comment': 'Beans'})

    comment_no = 0
    for row in reader:

      #lookthrough(row,test,"test")
      #lookthrough(row,ingredients,"ingredients",comment_no)
      #lookthrough(row,products,"products",comment_no)
      
      lookthrough_sc_st(row,skintype,"skintype",comment_no)
      lookthrough_sc_st(row,skinconcerns,"skinconcerns",comment_no)
      comment_no +=1 
      print(comment_no)

#writer.writerow([row[0]],[row[1]])
#writer.writerow({'title': row[0]})#, 'score': submission.score,'id': submission.id,'url': submission.url,'comment': top_level_comment.body})