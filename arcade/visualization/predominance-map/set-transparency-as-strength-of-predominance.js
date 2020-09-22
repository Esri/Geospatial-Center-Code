//start with the same sorted array
var industryarray = Sort([
  $feature["Accommodation_and_Food_Services"],
  $feature["Administrative_and_Support_and_"],
  $feature["Agriculture__Forestry__Fishing_"],
  $feature["Arts__Entertainment__and_Recrea"],
  $feature.Construction,
  $feature["Educational_Services"],
  $feature["Finance_and_Insurance"],
  $feature["Health_Care_and_Social_Assistan"],
  $feature.Information,
  $feature["Management_of_Companies_and_Ent"],
  $feature.Manufacturing,
  $feature.Mining,
  $feature["Not_Specified"],
  $feature["Other_Services__except_Public_A"],
  $feature["Professional__Scientific__and_T"],
  $feature["Public_Administration"],
  $feature["Real_Estate_Rental_and_Leasing"],
  $feature["Retail_Trade"],
  $feature["Transportation_and_Warehousing"],
  $feature.Utilities,
  $feature["Wholesale_Trade"]]);

//reverse the sorting, then get the top two values; assign each to a variable
var toptwo = Top(Reverse(industryarray),2);
var topvalue = First(toptwo);
var secondvalue = First(Reverse(toptwo));

 
//calculate how close the second value is to the top value as a percent, 
// then subtract to get the percent difference; 
// this output is used in setting the transparency
var pctdiff = (secondvalue / topvalue) * 100;
var transparencypct = Round(100 - pctdiff,2);
transparencypct;