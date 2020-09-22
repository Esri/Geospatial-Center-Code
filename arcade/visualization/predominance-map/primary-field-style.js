//create an array of all the fields you want to consider and sort 
// (this defaults to least to greatest)
var industryarray = Sort([
  $feature["Accommodation_and_Food_Services"],
  $feature["Administrative_and_Support_and_"],
  $feature["Agriculture__Forestry__Fishing_"],
  $feature["Arts__Entertainment__and_Recrea"],
  $feature.Constructio,
  $feature["Educational_Services"],
  $feature["Finance_and_Insurance"],
  $feature["Health_Care_and_Social_Assistan"],
  $feature.Informatio,
  $feature["Management_of_Companies_and_Ent"],
  $feature.Manufacturin,
  $feature.Minin,
  $feature["Not_Specified"],
  $feature["Other_Services__except_Public_A"],
  $feature["Professional__Scientific__and_T"],
  $feature["Public_Administration"],
  $feature["Real_Estate_Rental_and_Leasing"],
  $feature["Retail_Trade"],
  $feature["Transportation_and_Warehousing"],
  $feature.Utilitie,
  $feature["Wholesale_Trade"]
]);

//reverse the sorting to go from greatest to least, then get the first value
var topvalue = First(Reverse(industryarray));

// to get the name of the corresponding field, 
// compare the top value to all the fields in question, 
// and return the appropriate name
Decode(topvalue, 
  $feature["Agriculture__Forestry__Fishing_"],'Agriculture, Forestry, Fishing, and Hunting', 
  $feature.Mining,'Mining',
  $feature.Utilities,'Utilities',
  $feature.Construction,'Construction',
  $feature.Manufacturing,'Manufacturing',
  $feature["Wholesale_Trade"],'Wholesale Trade',
  $feature["Retail_Trade"],'Retail Trade',
  $feature["Transportation_and_Warehousing"],'Transportation and Warehousing',
  $feature.Information,'Information',
  $feature["Finance_and_Insurance"],'Finance and Insurance',
  $feature["Real_Estate_Rental_and_Leasing"],'Real Estate Rental and Leasing',
  $feature["Professional__Scientific__and_T"],'Professional, Scientific, and Technical Services',
  $feature["Management_of_Companies_and_Ent"],'Management of Companies and Enterprises',
  $feature["Administrative_and_Support_and_"],'Administrative and Support and Waste Management and Remediation Services',
  $feature["Educational_Services"],'Educational Services',
  $feature["Health_Care_and_Social_Assistan"],'Health Care and Social Assistance',
  $feature["Arts__Entertainment__and_Recrea"],'Arts, Entertainment, and Recreation',
  $feature["Accommodation_and_Food_Services"],'Accommodation and Food Services',
  $feature["Other_Services__except_Public_A"],'Other Services (except Public Administration)',
  $feature["Public_Administration"],'Public Administration','Not Specified');