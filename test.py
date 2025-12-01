from service import predict_drought_for_region

unq = ['Andaman & Nicobar Islands' ,'Arunachal Pradesh' ,'Assam & Meghalaya',
 'Naga Mani Mizo Tripura' ,'Sub Himalayan West Bengal & Sikkim',
 'Gangetic West Bengal' ,'Orissa' ,'Jharkhand' ,'Bihar' ,'East Uttar Pradesh',
 'West Uttar Pradesh' ,'Uttarakhand' ,'Haryana Delhi & Chandigarh' ,'Punjab'
 'Himachal Pradesh' ,'Jammu & Kashmir' ,'West Rajasthan' ,'East Rajasthan',
 'West Madhya Pradesh' ,'East Madhya Pradesh' ,'Gujarat Region',
 'Saurashtra & Kutch' ,'Konkan & Goa' ,'Madhya Maharashtra' ,'Matathwada',
 'Vidarbha' ,'Chhattisgarh' ,'Coastal Andhra Pradesh' ,'Telangana',
 'Rayalseema' ,'Tamil Nadu' ,'Coastal Karnataka' ,'North Interior Karnataka',
 'South Interior Karnataka' ,'Kerala' ,'Lakshadweep']

def main():
  print(unq)
  while True:
    region_nm = input("Enter area name(same as in list ): ")
    if region_nm not in unq:
        print("SUBDIVISION NOT FOUND. Please try again.")
    else:
        break
  print('SELECTED AREA', region_nm)
  while True:
    try:
      n = int(input("Enter number of months whose rainfall is known in this year (starting from JAN, max 12): "))
      if 1 <= n <= 12:
          break
      else:
          print("Please enter a number between 1 and 12.")
    except ValueError:
          print("Please enter a valid integer.")
  months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN","JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
  user_input={}
  for i in range (n):
    month = months[i]
    val = float(input(f"Enter rainfall for {month}: "))
    user_input[month] = val

  res = predict_drought_for_region(
  csv_path="C:\\Users\\deepa\\Desktop\\GAURI\\gitdemo\\DROUGHT_b1\\.venv\\Rainfall_Data_LL.csv",
  region_nm=region_nm,
  user_month_values=user_input)

  print(res["region"]+"\n"+ "Label: "+res["label"]+"\n"+"Dryness percentile "+ str(res["Dryness percentile"]) + "%")

main()